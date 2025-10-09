import sys
import json
import re

HELP_MESSAGE = '''“传话筒”用于跨群聊传递消息，即使您不在对应的群聊也可通过此工具发送消息
※使用此功能即表示您同意在合理范围内使用，请勿用于任何刷屏或骚扰，机器人后台可查询一切行为记录

    · 指令帮助：
- #run 传话筒 list
    查询完整通讯录列表
- #run 传话筒 <群昵称/群号> 【消息内容】
    向指定群聊发送消息，目标群聊需要在通讯录里才能发送
- #run 传话筒 add <群昵称> <群号>
    添加新群聊至通讯录，请确保bot在目标群聊！
- #run 传话筒 del <群昵称/群号>
    从通讯录删除群聊，仅能删除自己添加的群'''

admins = [2295824927]

def groupID(string):
    if string == 'private':
        return -1
    return int(re.findall(r'\((.*?)\)', string)[-1])

class Error(Exception):
    pass

def process_args(stdin):
    global storage
    lst = stdin.split()
    # 帮助
    if len(lst) == 0 or lst[0] == "帮助" or lst[0] == "help":
        data_output["content"] = HELP_MESSAGE

    # 查询列表
    elif len(lst) == 1 and (lst[0] == "列表" or lst[0] == "list" or lst[0] == "通讯录"):
        data_output["content"] = "  通讯录列表："
        for k, v in data["contacts"].items():
            data_output["content"] += f"\n{k}({v})"

    # 添加通讯录
    elif len(lst) == 3 and (lst[0] == "添加" or lst[0] == "add"):
        name = lst[1]
        if lst[2].isdigit() and int(lst[2]) > 0:
            group = int(lst[2])
        else:
            data_output["content"] = "[数值错误] 群号只能为正整数"
            raise Error()
        if group in data["contacts"].values():
            data_output["content"] = f"[添加失败] 通讯录中已存在此群聊：{group}"
        elif name in data["contacts"]:
            data_output["content"] = f"[添加失败] 通讯录中已存在此称呼：{name}({data['contacts'][name]})"
        elif name in data["contacts"].values():
            data_output["content"] = f"[添加失败] 不能将通讯录中已存在的群号设为名称"
        else:
            user_groups = storage.split("\n")
            result_group = [item for item in user_groups if item in map(str, data["contacts"].values())]
            storage = "\n".join(result_group)
            # 添加
            data["contacts"][name] = group
            data["contacts"] = dict(sorted(data["contacts"].items(), key=lambda item: item[1]))
            data_output["global"] = json.dumps(data)
            data_output["storage"] = storage
            if storage != "":
                data_output["storage"] += "\n"
            data_output["storage"] += str(group)
            data_output["content"] = f"添加 {name}({group}) 成功"

    # 删除通讯录
    elif len(lst) == 2 and (lst[0] == "删除" or lst[0] == "del" or lst[0] == "移除" or lst[0] == "delete"):
        delete = lst[1]
        if (not delete.isdigit() and delete not in data["contacts"]) or (delete.isdigit() and int(delete) not in data["contacts"].values()):
            data_output["content"] = "[操作失败] 通讯录中不包含此群聊的相关信息"
            raise Error()
        user_groups = storage.split("\n")
        if data_input['userID'] not in admins:
            if delete not in user_groups and (delete.isdigit() and data["contacts"][int(delete)] not in user_groups):
                data_output["content"] = "[操作失败] 当前通讯录并非由您创建"
                raise Error()
        # 删除
        for k, v in data["contacts"].items():
            if k == delete or v == delete:
                group_info = f"{k}({v})"
                del data["contacts"][k]
                break
        result_group = [item for item in user_groups if item in map(str, data["contacts"].values())]
        data_output["global"] = json.dumps(data)
        data_output["storage"] = "\n".join(result_group)
        data_output["content"] = f"删除 {group_info} 成功"

    # 发送消息
    elif len(lst) >= 2:
        to = lst[0]
        if to in data["contacts"]:
            group = data["contacts"][to]
        elif to.isdigit() and int(to) in data["contacts"].values():
            group = int(to)
        else:
            data_output["content"] = "[发送失败] 通讯录中不包含此群聊的相关信息，仅能向列表中的群聊发送消息。使用「#run 传话筒 list」查看通讯录列表"
            raise Error()
        current = groupID(data_input["from"])
        if current == group:
            data_output["content"] = "原地TP还需要什么传话筒\n(～￣▽￣)～"
            raise Error()
        message = " ".join(item.replace("[图片]", "") for item in lst[1:] if item != "[图片]")
        if message:
            message = "\n" + message
        data_output["active"] = [{
            "groupID": group,
            "message": {
                "format": "MessageChain",
                "messageList": []
            }
        }]
        msg_list = data_output["active"][0]["message"]["messageList"]
        # 文本消息
        if data_input["from"] == "private":
            content = f"{data_input['nickname']}({data_input['userID']})发送了一条消息：{message}"
        else:
            content = f"来自群 {data_input['from']} 的消息：{message}"
        msg_list.append({"content": content})
        # 图片消息
        for img in data_input.get("images", []):
            msg_list.append({
                "format": "base64",
                "content": img["base64"]
            })
        # 程序原始输出
        data_output["content"] = "[操作成功] 如果报错，可能是通讯录信息错误或bot未加入此群聊"
    
    # 参数不匹配
    else:
        data_output["content"] = "[参数不匹配] 请查看下方指令帮助：\n\n" + HELP_MESSAGE

# ----------main----------
json_input = sys.stdin.readline().strip()
stdin = sys.stdin.read().strip()

data_input = json.loads(json_input)
data_output = {}
storage = data_input["storage"]
if data_input["global"] != "":
    data = json.loads(data_input["global"])
else:
    data = {"contacts": {}}
try:
    process_args(stdin)
except (Error) as e:
    pass
print(json.dumps(data_output))
