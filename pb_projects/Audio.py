# 使用 Audio 格式输出
import json

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def print_text(msg):
    obj = {
        "format": "text",
        "content": msg
    }
    print(json.dumps(obj))

def main():
    data_input = json.loads(input())
    try:
        args = input().split()
    except:
        args = []
    if len(args) == 0 or args[0] == "help" or args[0] == "帮助":
        HELP_TEXT = f""" · 文字转语音工具
程序输入为 5 项，分别为：
person speed pitch volume content
 - person：音库，目前仅支持：
  · 0：度小美-成熟女声(基础音库)
  · 106：度博文-情感男声(精品音库)
  · 4100：度小雯-成熟女声(臻品音库)
  · 4106：度博文-情感男声(臻品音库)
 - speed：语速（支持范围 0-15）
 - pitch：音调（支持范围 0-15）
 - volume：音量（支持范围 0-15）
 - content：要播放的文本内容

*参数不足或转换错误时自动使用默认配置（当前为：{data_input.get("global")}），且仅读取程序输出的第一项进行转换"""
        print_text(HELP_TEXT)
        return
    if args[0] == "default" or args[0] == "默认":
        global_save = ' '.join(args[1:5])
        if all(is_number(x) for x in args[1:5]):
            obj = {
                "format": "text",
                "content": f"修改默认配置为：{global_save}",
                "global": global_save
            }
            print(json.dumps(obj))
        else:
            print_text(f"[错误] 修改失败：配置中包含非数字项 {global_save}")
        return

    try:
        person_str, speed_str, pitch_str, volume_str, content = args[0], args[1], args[2], args[3], ' '.join(args[4:])
        person = int(person_str)
        speed = int(speed_str)
        pitch = int(pitch_str)
        volume = int(volume_str)
    except:
        obj = { "content": ' '.join(args) }
        configs_str = data_input.get("global")
        if configs_str:
            configs = configs_str.split()
            fields = ["person", "speed", "pitch", "volume"]
            for i in range(min(len(configs), len(fields))):
                obj[fields[i]] = int(configs[i])
        print(json.dumps(obj))
        return

    obj = {
        "person": person,
        "speed": speed,
        "pitch": pitch,
        "volume": volume,
        "content": content
    }
    print(json.dumps(obj))

if __name__ == "__main__":
    main()
