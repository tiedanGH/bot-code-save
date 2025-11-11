import sys
import json
import requests
from datetime import datetime, timezone, timedelta
import html
import ssl
import certifi
import websocket
import threading
import time

ADMINS = [2295824927]

def get_help_text():
    """返回帮助文本"""
    help_content = '''【YaGame工具】

使用说明：
- help/帮助：查看此帮助
- room/房间：查询游戏房间
- commit/提交：获取最新提交信息
- about/关于：关于YaGame'''
    return {
        "content": help_content
    }

def get_about_text():
    """返回关于文本"""
    about_content = """【YaGame】
作者：Ya
GitHub：https://github.com/imalydimalyd/yagame
欢迎入群体验（QQ 群）：1049207106

YaGame是一个支持自建服务器、自制游戏规则的下一代游戏平台。
- 游戏大厅：可以在线玩多人游戏，支持自己创建服务器
- 聊天室：可以和小葵、茉茉聊天
- Quint：可以玩有趣的抽卡游戏"""
    return {
        "content": about_content
    }

def fetch_github_commits():
    """从GitHub API获取最新的10条commit信息"""
    url = "https://api.github.com/repos/imalydimalyd/yagame/commits?per_page=10"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        commits = response.json()
        
        if not isinstance(commits, list):
            commits = {"content": "[错误] 获取commit信息失败，API返回格式异常"}
            
    except requests.exceptions.RequestException as e:
        commits = {"content": f"[错误] 网络请求失败: {str(e)}"}
    except json.JSONDecodeError:
        commits = {"content": "[错误] 解析GitHub API响应失败"}

    # 如果是错误信息，直接返回
    if isinstance(commits, dict) and "content" in commits:
        return commits
    
    # 使用兼容性更好的CSS样式
    style = """<style>
    .commit-container {
        font-family: Arial, sans-serif;
        max-width: 800px;
        margin: 0 auto;
    }
    .commit-item {
        padding: 12px 0;
        border-bottom: 1px solid #e1e4e8;
        overflow: hidden;
    }
    .commit-avatar {
        float: left;
        margin-right: 12px;
    }
    .commit-avatar img {
        width: 32px;
        height: 32px;
        border-radius: 50%;
    }
    .commit-content {
        overflow: hidden;
    }
    .commit-message {
        font-weight: bold;
        color: #24292e;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .commit-meta {
        font-size: 12px;
        color: #586069;
    }
    .commit-sha {
        background: #f6f8fa;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: Consolas, monospace;
    }
    .commit-footer {
        margin-top: 16px;
        padding-top: 12px;
        border-top: 1px solid #e1e4e8;
        font-size: 12px;
        color: #6a737d;
        text-align: center;
    }
    .room-container {
        font-family: Arial, sans-serif;
        max-width: 600px;
        margin: 0 auto;
    }
    .room-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #e1e4e8;
        text-align: center;
    }
    .room-item {
        padding: 12px 0;
        border-bottom: 1px solid #e1e4e8;
    }
    .room-header {
        font-weight: bold;
        margin-bottom: 6px;
    }
    .room-id {
        color: #586069;
        font-size: 12px;
    }
    .room-status {
        display: inline-block;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 12px;
        margin-left: 8px;
    }
    .status-waiting {
        background-color: #d4edda;
        color: #155724;
    }
    .status-playing {
        background-color: #fff3cd;
        color: #856404;
    }
    .status-ended {
        background-color: #f8d7da;
        color: #721c24;
    }
    .room-players {
        font-size: 12px;
        color: #586069;
        margin-top: 4px;
    }
    .no-rooms {
        text-align: center;
        padding: 40px 20px;
        color: #586069;
        font-size: 14px;
    }
    </style>"""
    
    html_content = style + '<div class="commit-container">'
    
    for commit in commits:
        if not isinstance(commit, dict):
            continue
            
        # 提取commit信息
        sha = commit.get('sha', '')[:7]
        commit_data = commit.get('commit', {})
        message = commit_data.get('message', '').split('\n')[0]  # 只取第一行
        author_info = commit_data.get('author', {})
        date_str = author_info.get('date', '')
        
        # 格式化日期并转换为北京时间 (UTC+8)
        try:
            # 解析UTC时间
            utc_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            # 转换为北京时间 (UTC+8)
            beijing_date = utc_date.astimezone(timezone(timedelta(hours=8)))
            formatted_date = beijing_date.strftime("%Y年%m月%d日 %H:%M")
        except:
            formatted_date = date_str
        
        # 获取作者信息
        author = commit.get('author', {})
        avatar_url = author.get('avatar_url', '')
        login = author.get('login', '')
        
        # 转义HTML特殊字符
        message = html.escape(message)
        login = html.escape(login if login else author_info.get('name', ''))
        
        # 限制消息长度
        if len(message) > 100:
            message = message[:97] + "..."
        
        html_content += f"""
        <div class="commit-item">
            <div class="commit-avatar">
                <img src="{avatar_url}" alt="{login}" />
            </div>
            <div class="commit-content">
                <div class="commit-message">
                    {message}
                </div>
                <div class="commit-meta">
                    <span style="font-weight: bold;">{login}</span>
                    <span> 提交于 </span>
                    <span>{formatted_date}</span>
                    <span> · </span>
                    <code class="commit-sha">
                        {sha}
                    </code>
                </div>
            </div>
        </div>"""
    
    # 添加底部提示
    html_content += """
    <div class="commit-footer">
        仅展示最新的 10 条 commit 信息
    </div>
    """
    
    html_content += "</div>"
    
    return {
        "format": "markdown",
        "width": 800,
        "content": html_content
    }

def fetch_rooms_info(storage_data):
    """获取房间信息"""
    # 从global存储中获取服务器地址和房间ID
    try:
        global_data = json.loads(storage_data.get("global", "{}"))
        server_address = global_data.get("server_address", "")
        room_id = global_data.get("room_id", "")
        
        if not server_address:
            return {"content": "[错误] 未设置服务器地址，请使用 admin server <address> 设置"}
        if not room_id:
            return {"content": "[错误] 未设置YaGameHall ID，请使用 admin room <id> 设置"}
    except:
        return {"content": "[错误] 存储数据格式错误"}
    
    # 存储WebSocket响应和状态
    ws_responses = []
    ws_error = None
    ws_open_received = False
    ws_connection = None

    def on_message(ws, message):
        nonlocal ws_open_received
        try:
            data = json.loads(message)
            ws_responses.append(data)
            
            # 检查是否收到open消息
            if data.get("type") == "open":
                ws_open_received = True
                # 发送rooms请求
                ws.send(json.dumps({"type": "rooms"}))
        except json.JSONDecodeError:
            pass

    def on_error(ws, error):
        nonlocal ws_error
        ws_error = str(error)

    def on_close(ws, close_status_code, close_msg):
        pass

    def on_open(ws):
        nonlocal ws_connection
        ws_connection = ws
        # 发送初始连接请求
        ws.send(json.dumps({"id": room_id, "keyID": "VISITOR"}))

    # 连接WebSocket
    try:
        # 使用 websocket-client 库创建连接
        ws = websocket.WebSocketApp(server_address,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        
        # 在单独的线程中运行WebSocket，并设置超时
        def run_ws():
            ws.run_forever(
                sslopt={
                    "ca_certs": certifi.where(),
                    "cert_reqs": ssl.CERT_REQUIRED
                }
            )
        
        thread = threading.Thread(target=run_ws)
        thread.daemon = True
        thread.start()
        
        # 等待响应或超时
        timeout = 10  # 10秒超时
        start_time = time.time()
        while time.time() - start_time < timeout:
            if ws_error:
                if ws_connection:
                    ws_connection.close()
                return {"content": f"[错误] WebSocket连接失败: {ws_error}"}
            
            # 检查是否收到rooms响应
            for response in ws_responses:
                if response.get("type") == "ok" and response.get("msg", {}).get("type") == "rooms":
                    if ws_connection:
                        ws_connection.close()
                    return process_rooms_response(response)
            
            time.sleep(0.1)
        
        if ws_connection:
            ws_connection.close()
        return {"content": "[错误] 请求超时，未收到房间信息"}
    
    except Exception as e:
        if ws_connection:
            ws_connection.close()
        return {"content": f"[错误] WebSocket异常: {str(e)}"}

def process_rooms_response(response):
    """处理房间响应数据"""
    rooms_data = response.get("msg", {}).get("rooms", [])
    
    # 过滤公开房间
    public_rooms = [room for room in rooms_data if room.get("isPublic", False)]
    
    style = """<style>
    .room-container {
        font-family: Arial, sans-serif;
        max-width: 600px;
        margin: 0 auto;
    }
    .room-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #e1e4e8;
        text-align: center;
    }
    .room-item {
        padding: 12px 0;
        border-bottom: 1px solid #e1e4e8;
    }
    .room-header {
        font-weight: bold;
        margin-bottom: 6px;
    }
    .room-id {
        color: #586069;
        font-size: 12px;
    }
    .room-status {
        display: inline-block;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 12px;
        margin-left: 8px;
    }
    .status-waiting {
        background-color: #d4edda;
        color: #155724;
    }
    .status-playing {
        background-color: #fff3cd;
        color: #856404;
    }
    .status-ended {
        background-color: #f8d7da;
        color: #721c24;
    }
    .room-players {
        font-size: 12px;
        color: #586069;
        margin-top: 4px;
    }
    .no-rooms {
        text-align: center;
        padding: 40px 20px;
        color: #586069;
        font-size: 15px;
    }
    </style>"""
    
    html_content = style + '<div class="room-container">'
    html_content += '<div class="room-title">游戏大厅房间列表</div>'
    
    if not public_rooms:
        html_content += '<div class="no-rooms">当前没有可加入的游戏房间</div>'
    else:
        for room in public_rooms:
            room_id = room.get("id", "")
            room_name = room.get("name", "[未知游戏]")
            players = room.get("players", [])
            player_count = len(players)
            player_names = [player.get("user", "") for player in players]
            
            # 确定房间状态
            if room.get("ended", False):
                status = "已结束"
                status_class = "status-ended"
            elif room.get("started", False):
                status = "进行中"
                status_class = "status-playing"
            else:
                status = "等待中"
                status_class = "status-waiting"
            
            html_content += f"""
            <div class="room-item">
                <div class="room-header">
                    {html.escape(room_name)}
                    <span class="room-status {status_class}">{status}</span>
                </div>
                <div class="room-id">房间ID: {room_id}</div>
                <div class="room-players">
                    玩家 ({player_count}人): {', '.join([html.escape(name) for name in player_names])}
                </div>
            </div>"""
    
    html_content += "</div>"
    
    return {
        "format": "markdown",
        "width": 400,
        "content": html_content
    }

def update_global_storage(storage_data, key, value):
    """更新全局存储数据"""
    try:
        global_data = json.loads(storage_data.get("global", "{}"))
    except:
        global_data = {}
    
    global_data[key] = value
    
    # 返回更新后的存储数据
    return {
        "global": json.dumps(global_data),
        "content": f"[成功] 已更新 {key}: {value}"
    }

def main():
    # 读取输入
    input_lines = sys.stdin.read().splitlines()
    
    if not input_lines:
        # 如果没有输入，输出错误信息
        output = {"content": "错误：未接收到输入"}
        print(json.dumps(output, ensure_ascii=False))
        return
    
    # 解析第一行的存储数据
    try:
        storage_data = json.loads(input_lines[0])
    except json.JSONDecodeError:
        storage_data = {"storage": "", "global": "", 'userID': -1, 'nickname': '未知', 'from': 'private'}
    
    # 获取用户输入（从第二行开始）
    user_input = "\n".join(input_lines[1:]).strip() if len(input_lines) > 1 else ""
    user_input_lower = user_input.lower()
    
    # 处理用户输入
    if user_input_lower in ['help', 'h', '帮助']:
        output = get_help_text()
    elif user_input_lower in ['room', 'rooms', '房间']:
        output = fetch_rooms_info(storage_data)
    elif user_input_lower in ['commit', '提交']:
        output = fetch_github_commits()
    elif user_input_lower in ['about', '关于']:
        output = get_about_text()
    elif user_input.startswith('admin server ') and storage_data['userID'] in ADMINS:
        # 更新服务器地址
        address = user_input[13:].strip()
        if address:
            output = update_global_storage(storage_data, "server_address", address)
        else:
            output = {"content": "[错误] 服务器地址不能为空"}
    elif user_input.startswith('admin room ') and storage_data['userID'] in ADMINS:
        # 更新房间ID
        room_id = user_input[11:].strip()
        if room_id:
            output = update_global_storage(storage_data, "room_id", room_id)
        else:
            output = {"content": "[错误] YaGameHall ID 不能为空"}
    else:
        output = {"content": "[错误] 未知指令，请使用「help」查看指令帮助"}
    
    # 输出结果
    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()