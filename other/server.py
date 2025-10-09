#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import logging
import os
import sys
import datetime
import ipaddress

BLACKLIST_FILE = "blacklist.txt"   # Blacklist file (one IP or CIDR per line)
SERVE_DIR = "server"               # Root directory to serve
LOGS_DIR = "logs"                  # Logs directory (stored in current folder)

# ---------- Logging Handler ----------
class DateFileHandler(logging.Handler):
    def __init__(self, logs_dir=LOGS_DIR, encoding='utf-8'):
        super().__init__()
        self.logs_dir = logs_dir
        self.encoding = encoding
        os.makedirs(self.logs_dir, exist_ok=True)
        self.current_date = datetime.date.today()
        self._open_file()

    def _open_file(self):
        path = os.path.join(self.logs_dir, f"{self.current_date.isoformat()}.log")
        self.stream = open(path, 'a', encoding=self.encoding)

    def emit(self, record):
        try:
            now = datetime.date.today()
            if now != self.current_date:
                try:
                    self.stream.close()
                except Exception:
                    pass
                self.current_date = now
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
file_h = DateFileHandler(LOGS_DIR)
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

# ---------- Custom TCPServer with IP blacklist ----------
class BlacklistTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

    def verify_request(self, request, client_address):
        """
        Called before processing a request.
        Return False to drop the connection immediately.
        """
        client_ip = client_address[0]
        blacklist = load_blacklist(BLACKLIST_FILE)
        if ip_is_blocked(client_ip, blacklist):
            logger.info(f"Rejected connection from {client_ip}")
            return False
        return True

# ---------- HTTP Handler ----------
class LoggingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=SERVE_DIR, **kwargs):
        os.makedirs(directory, exist_ok=True)
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format, *args):
        real_ip = self.headers.get("X-Real-IP") or self.client_address[0]
        logger.info("%s - - %s" % (real_ip, format % args))

# ---------- Start Server ----------
if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler_class = LoggingHTTPRequestHandler
    with BlacklistTCPServer(("", port), handler_class) as httpd:
        logger.info(f"Serving HTTP on 0.0.0.0 port {port} (http://0.0.0.0:{port}/) serving directory '{SERVE_DIR}' ...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received, exiting.")
            httpd.server_close()
