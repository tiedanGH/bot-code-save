import re
import math

HELP_MESSAGE = '''此工具用于《开放蜂巢》游戏计算分数变化（开启连线奖励）

输入蜂巢连线算式，有3种输入格式：
·算式：8*3
表示数字8，长度3，得分为 31(24+7)
·算式：8
视作8*1，得分为 8
·算式：9*5-8*3+6
表示连线9*5、断开8*3、连线6*1，得分为 63(45+18)-31(24+7)+6=38

输入时请注意格式正确，错误的格式会被当作无效数据排除'''

def preprocess_expr(expr):
    expr = expr.replace(" ", "")
    if expr:
        first_char = expr[0]
        rest = expr[1:]
        rest = re.sub(r'[^0-9+\-\*]', '', rest)
        expr = first_char + rest
    expr = re.sub(r'(?<!\*)\b(\d+)\b(?!\*)', r'\1*1', expr)
    return expr

def calculate_scores(expr):
    expr = preprocess_expr(expr)
    pattern = re.compile(r'([+-]?)(\d+)\*(\d+)')
    
    total_score = 0
    total_extra = 0
    expression = ""
    expression2 = ""
    
    for m in pattern.finditer(expr):
        sign_str = m.group(1)
        sign = -1 if sign_str == '-' else 1
        num = int(m.group(2))
        length = int(m.group(3))

        if length < 3:
            multiple = 0
        elif length == 3:
            multiple = 0.3
        elif length in (4, 5):
            multiple = 0.4
        elif length in (6, 7):
            multiple= 0.5
        elif length in (8, 9):
            multiple = 0.6
        else:
            multiple = 0
        
        term_score = num * length
        term_extra = math.floor(term_score * multiple)
        term_total = term_score + term_extra
        
        total_score += sign * term_score
        total_extra += sign * term_extra

        expression += f"{sign_str}{num}*{length}"
        if length < 3:
            expression2 += f"{sign_str}{term_total}"
        elif length <= 9:
            expression2 += f"{sign_str}{term_total}({term_score}+{term_extra})"
        else:
            expression2 += f"{sign_str}{term_total}({term_score}+[0])"

    return total_score, total_extra, expression, expression2

expr = input()
if expr == "帮助" or expr == "help":
    print(HELP_MESSAGE)
    raise SystemExit(0)
score, extra_score, expression, expression2 = calculate_scores(expr)
print(f"初始算式：\n{expression}")
print(f"分数算式：\n{expression2}")
print("总分数：", score+extra_score)
print("基础分数：", score)
print("连线奖励：", extra_score)
