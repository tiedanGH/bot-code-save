import hashlib
import random
import re

def generate_color(input_str):
    # 特斯拉彩蛋检测
    if str(input_str).lower() in ["tesla", "特斯拉"]:
        return "#FFFFFF"

    # 判断是否是合法颜色代码
    if isinstance(input_str, str) and re.fullmatch(r"#([0-9A-Fa-f]{6})", input_str):
        return input_str.upper()

    if input_str == "":
        # 种子为空纯随机
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"#{r:02X}{g:02X}{b:02X}"
    else:
        # 使用输入作为种子，生成随机颜色
        seed = str(input_str)
        random.seed(seed)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"#{r:02X}{g:02X}{b:02X}"

def get_contrast_color(hex_color):
    # 解析RGB
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    
    # 计算亮度 YIQ
    yiq = (r*299 + g*587 + b*114) / 1000
    return "#000000" if yiq >= 128 else "#FFFFFF"

def generate_html(input_str):
    color = generate_color(input_str)
    contrast = get_contrast_color(color)
    html = f'''<style>body {{ border: 0; padding: 0; margin: 0; }} </style>
<div style="width:200px; height:200px; background-color:{color}; display:flex; align-items:center; justify-content:center; font-family:sans-serif; font-size:32px; color:{contrast};">{color}</div>'''
    return html

# 获取用户输入并输出 HTML
if __name__ == "__main__":
    try:
        user_input = input().strip()
    except Exception as e:
        user_input = ""
    print(generate_html(user_input))
