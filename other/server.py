#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import logging
import os
import sys
import datetime
import ipaddress
import json
import subprocess

CONFIG_FILE = "config.json"         # Config file (projects config)
BLACKLIST_FILE = "blacklist.txt"    # Blacklist file (one IP or CIDR per line)
SERVE_DIR = "server"                # Root directory to serve
LOGS_DIR = "logs"                   # Logs directory (stored in current folder)

# ---------- Config Loader ----------
def load_config(path=CONFIG_FILE):
    """Load config.json, create if not exists."""
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"projects": []}, f, indent=4)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_project_by_name(cfg, name):
    for p in cfg.get("projects", []):
        if p.get("name") == name:
            return p
    return None

# ---------- Logging Handler ----------
class MonthFileHandler(logging.Handler):
    def __init__(self, logs_dir=LOGS_DIR, encoding='utf-8'):
        super().__init__()
        self.logs_dir = logs_dir
        self.encoding = encoding
        os.makedirs(self.logs_dir, exist_ok=True)
        self.current_month = datetime.date.today().strftime("%Y-%m")
        self._open_file()

    def _open_file(self):
        path = os.path.join(self.logs_dir, f"{self.current_month}.log")
        self.stream = open(path, 'a', encoding=self.encoding)

    def emit(self, record):
        try:
            now_month = datetime.date.today().strftime("%Y-%m")
            if now_month != self.current_month:
                try:
                    self.stream.close()
                except Exception:
                    pass
                self.current_month = now_month
                self._open_file()

            msg = self.format(record)
            self.stream.write(msg + '\n')
            self.stream.flush()
        except Exception:
            self.handleError(record)

    def close(self):
        try:
            if hasattr(self, 'stream'):
                self.stream.close()
        finally:
            super().close()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s  %(levelname)s  %(message)s', '%Y-%m-%d %H:%M:%S')

stream_h = logging.StreamHandler(sys.stdout)
stream_h.setFormatter(fmt)
file_h = MonthFileHandler(LOGS_DIR)
file_h.setFormatter(fmt)

if not logger.handlers:
    logger.addHandler(stream_h)
    logger.addHandler(file_h)
else:
    handler_types = {type(h) for h in logger.handlers}
    if logging.StreamHandler not in handler_types:
        logger.addHandler(stream_h)
    logger.addHandler(file_h)

# ---------- Blacklist Loader ----------
def load_blacklist(path=BLACKLIST_FILE):
    """
    Load blacklist from file.
    Supports both single IP addresses and CIDR ranges.
    """
    nets = []
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write("# Add one IP or CIDR per line, for example:\n")
            f.write("# 192.168.1.100\n")
            f.write("# 10.0.0.0/8\n")
            f.write("# 2001:db8::/32\n")
        return nets

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            try:
                if '/' in line:
                    nets.append(ipaddress.ip_network(line, strict=False))
                else:
                    nets.append(ipaddress.ip_address(line))
            except Exception as e:
                logger.warning(f"Invalid blacklist entry: {line} -> {e}")
    return nets

def ip_is_blocked(client_ip, blacklist):
    """
    Check if client_ip is in blacklist.
    """
    try:
        ipobj = ipaddress.ip_address(client_ip)
    except Exception:
        return False
    for item in blacklist:
        if isinstance(item, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
            if ipobj in item:
                return True
        else:
            if ipobj == item:
                return True
    return False

def respond_json(handler, status, data):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)

# ---------- HTTP Handler ----------
class LoggingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    _blacklist_cache = None
    _blacklist_mtime = 0

    def __init__(self, *args, directory=SERVE_DIR, **kwargs):
        os.makedirs(directory, exist_ok=True)
        super().__init__(*args, directory=directory, **kwargs)

    @classmethod
    def _load_blacklist_if_updated(cls):
        try:
            current_mtime = os.path.getmtime(BLACKLIST_FILE)
            if (cls._blacklist_cache is None or current_mtime != cls._blacklist_mtime):
                cls._blacklist_cache = load_blacklist(BLACKLIST_FILE)
                cls._blacklist_mtime = current_mtime
                logger.info(f"Reloaded blacklist, {len(cls._blacklist_cache)} entries")
                return True
            return False
        except OSError as e:
            if cls._blacklist_cache is None:
                cls._blacklist_cache = []
                logger.warning(f"Blacklist file not found: {BLACKLIST_FILE}")
            return False

    def check_ip_blacklist(self):
        self._load_blacklist_if_updated()
        real_ip = self.headers.get("X-Real-IP") or self.client_address[0]
        if ip_is_blocked(real_ip, self._blacklist_cache):
            logger.warning(f"Rejected HTTP request from {real_ip}")
            self.send_error(403, "Forbidden")
            return False
        return True

    def do_GET(self):
        if not self.check_ip_blacklist():
            return
        super().do_GET()

    def do_HEAD(self):
        if not self.check_ip_blacklist():
            return
        super().do_HEAD()

    def do_POST(self):
        if not self.check_ip_blacklist():
            return

        if self.path != "/api/pull":
            return respond_json(self, 400, {"error": "Invalid POST Request", "code": 400})

        # git pull API
        cfg = load_config()

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            data = json.loads(body)
        except Exception:
            return respond_json(self, 400, {"error": "Invalid POST Request", "code": 400})

        if "name" not in data:
            return respond_json(self, 400, {"error": "Invalid POST Request", "code": 400})

        project = find_project_by_name(cfg, data["name"])
        if not project:
            return respond_json(self, 404, {"error": "Project Not Found", "code": 404})

        if self.headers.get("token") != project.get("token"):
            return respond_json(self, 401, {"error": "Invalid Token", "code": 401})

        repo_path = project.get("path")
        if not os.path.isdir(repo_path):
            return respond_json(self, 500, {"error": "Internal Server Error: invalid repository path", "code": 500})

        try:
            proc = subprocess.Popen(
                ["git", "pull"],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            stdout, _ = proc.communicate()
            exit_code = proc.returncode
            if exit_code != 0:
                return respond_json(self, 500, {"error": "git pull FAILED", "exit_code": exit_code, "message": stdout.strip()})
        except Exception as e:
            return respond_json(self, 500, {"error": f"git pull ERROR", "code": 500, "message": e})

        # success
        return respond_json(self, 200, {"message": stdout.strip()})

    def do_PUT(self):
        self.send_error(405, "Method Not Allowed")

    def do_PATCH(self):
        self.send_error(405, "Method Not Allowed")

    def do_DELETE(self):
        self.send_error(405, "Method Not Allowed")

    def do_OPTIONS(self):
        self.send_error(405, "Method Not Allowed")
    
    def guess_type(self, path):
        if path.endswith(".ico"):
            return "image/x-icon"
        return super().guess_type(path)

    def log_message(self, format, *args):
        real_ip = self.headers.get("X-Real-IP") or self.client_address[0]
        logger.info("%s - - %s" % (real_ip, format % args))

# ---------- Custom TCPServer ----------
class CustomTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

# ---------- Start Server ----------
if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler_class = LoggingHTTPRequestHandler
    with CustomTCPServer(("", port), handler_class) as httpd:
        logger.info(f"Serving HTTP on 0.0.0.0 port {port} (http://0.0.0.0:{port}/) serving directory '{SERVE_DIR}' ...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received, exiting.")
            httpd.server_close()
