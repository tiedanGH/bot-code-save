import re
from random import *
from math import *
from collections import Counter
import sys
# from timeout import *

first_, end_, time_ = True, False, 0

def check_num(num, mode):
    if mode == "int":
        try:
            return int(num)
        except:
            print(f"[错误] “{num}”不是一个整数", end = '')
    if mode == "float":
        try:
            return float(num)
        except:
            print(f"[错误] “{num}”不是一个数字", end = '')
    exit()
    
def check_range(start, end, n):
    if n >= 1 and n <= 20 and start < end and start >= -10**20 and end <= 10**20:
        return
    if n < 1:
        print("[错误] 骰子都被bot吃掉了：n必须大于0", end = '')
    if n > 20:
        print("[错误] 抽取失败：n不能大于20", end = '')
    if (n < 1 or n > 20) and (start >= end or start < -10**20 or end > 10**20):
        print()
    if start >= end:
        print("[错误] 上界必须大于下界", end = '')
    if start < -10 ** 20:
        print("[错误] 下界超过了最小限制：-10**20", end = '')
    if end > 10 ** 20:
        print("[错误] 上界超过了最大限制：10**20", end = '')
    exit()

def ban_functions(expression):
    ban_list = ["eval","exec","getattr","globals","builtins","locals","subprocess","shutil","import","os","open","class",
                "ctypes","sys","threading","functools","expression","result","dict"]
    ban_symbol = ["_","\\u","\\x","\\n","\\t"]
    for name in ban_list:
        if name in expression:
            raise PermissionError(name + "被禁用")
    for symbol in ban_symbol:
        if symbol in expression:
            raise PermissionError("符号“" + symbol.replace('\\', '\\\\') + "”被禁用")
    if len(re.findall(r'[a-zA-z]+\.[a-zA-z]+', expression)) > 0:
        raise PermissionError("符号“.”被限制使用，其两侧不能都为字母。math和random库已导入，可直接使用函数名")

# @timeout(1)
def dice(expression):
    if sys.platform != 'win32':
        sys.set_int_max_str_digits(1000000)
        sys.setrecursionlimit(1000)
    
    # operators = [("+", lambda x, y: x + y), ("-", lambda x, y: x - y), ("*", lambda x, y: x * y), ("/", lambda x, y: x / y)]
    
    segments = re.split(r'([\+\-\*\/\(\)\,\.\=\[\]])', expression)
    result, eval_result, expression_print, with_d= [], [], [], False

    for segment in segments:
        if segment in ['+','-','*','/','(',')',',','.','=','[',']']:
            expression_print.append(segment)
            result.append(segment)
            eval_result.append(segment)
        else:
            func_with_multiple_d = ["testdd"]
            try:
                if ('d' in segment or 'D' in segment) and segment not in func_with_multiple_d:
                    parts = re.split(r'd|D', segment)
                    if parts[0] == "":
                        x = 1
                        y = int(parts[1])
                    else:
                        x = int(parts[0])
                        y = int(parts[1])
                    if y < 1:
                        print("[错误] 骰子面数必须大于0", end = '')
                        exit()
                    random_numbers = [randint(1, y) for _ in range(x)]
                    result.append(f"({'+'.join(map(str, random_numbers))})")
                    eval_result.append(str(sum(random_numbers)))
                    if len(parts) > 2:
                        print("[表达式错误] d不能连用，格式例如：d5*(3d6+2)，已截断无效部分")
                        segment = f"{parts[0]}d{parts[1]}!!"
                    expression_print.append(segment)
                    with_d = True
                else:
                    # 合并非d部分
                    expression_print.append(segment)
                    result.append(segment)
                    eval_result.append(segment)
            except ValueError:
                # 合并含单个d但非骰子部分
                expression_print.append(segment)
                result.append(segment)
                eval_result.append(segment)

    final_expression = ''.join(result) + "="
    eval_expression = ''.join(eval_result)
    expression_print = ''.join(expression_print).replace('\\', '\\\\')
    
    try:
        # 移除代码中的mirai码和print，不影响大部分功能
        expression_print = re.sub(r'mirai:at', '', expression_print)
        eval_expression = re.sub(r'print|mirai:at', '', eval_expression)

        global first_, end_
        if first_:
            print("执行指令：")
            print(''.join(expression_print).replace('\\', '\\\\'))
            first_ = False
        
        ban_functions(eval_expression)
        final_result = eval(eval_expression)
        # 移除结果中的mirai码
        if isinstance(final_result, str):
            final_result = re.sub(r'mirai', '', final_result)
        # 输出过大转科学计数或截断
        if len(str(final_result)) > 300:
            if isinstance(final_result, str):
                if time_ > 1:
                    final_result = f"{str(final_result)[:100]}......\n[剩余{len(str(final_result))-100}字符被省略]"
                else:
                    final_result = f"{str(final_result)[:300]}......\n[剩余{len(str(final_result))-300}字符被省略]"
            else:
                final_result = f"{int(str(final_result)[:11])/10**10}e+{len(str(final_result))-1}"
        final_expression += "="
        if not with_d:
            final_expression = ""
            end_ = True
        result = f"{final_expression}{final_result}"
        if len(result) <= 500:
            return result
        else:
            return f"{eval_expression}={final_result}"
    except PermissionError as e:
        print("[禁止执行] 存在被限制执行的函数或符号:", e, end = '')
    except ZeroDivisionError as e:
        print("[数学错误] 不能除以0:", e, end = '')
    except OverflowError as e:
        print("[溢出错误] 数值运算超出最大限制:", e, end = '')
    except SyntaxError as e:
        if "d" in eval_expression or "D" in eval_expression:
            print("[语法错误] 存在无效骰子算式，请检查 d/D 右侧是否为整数:", e, end = '')
        else:
            print("[语法错误] 可能存在无法识别的字符/运算符、括号遗漏或其他无效语法:", e, end = '')
    except NameError as e:
        print("[语法错误] 存在无法识别的字母或函数:", e, end = '')
    except ValueError as e:
        print("[定义域错误] 算式不符合函数定义:", e, end = '')
    except TimeoutError as e:
        print("[运行超时] 程序运行超过时间限制，已被强制中断:", e, end = '')
    except Exception as e:
        print("[执行失败] 其他未知错误:", repr(e), end = '')
    end_ = True
    return None

# @timeout(2)
def run_rd_cmds(l):
    if l[0] == "信息" or l[0] == "info":
        print("此程序使用本地python运行，用于在星星姬无法工作时使用")
        print("部分指令仿照星星姬命令格式，目前已实现的功能有：")
        print("XdY、c、r、rn、i、ic、ir、f")
        print("具体使用方法请查看帮助：#rd help", end = '')

    elif l[0] == "帮助" or lst[0] == "help":
        print("#rd info   程序简介")
        print("#rd <智能算式(长度至少为3)> <次数(<=5)>   支持执行丢骰子、math和random库全部函数的调用，格式例如：d5*(3d6+2)+sin(pi/2)")
        print("#rd   从1-100中抽取一个整数")
        print("#rd c <n> <元素列表>   抽取n个不重复的元素")
        print("#rd r <n> <元素列表>   抽取n个可重复的元素")
        print("#rd rn <n> <元素列表>   抽取n个可重复的元素（仅显示个数，n最大可为1000000）")
        print("#rd i [下界] <上界>   随机生成1个整数")
        print("#rd ic <n> [下界] <上界>   随机生成n个不重复的整数")
        print("#rd ir <n> [下界] <上界>   随机生成n个可重复的整数")
        print("#rd f <n> <下界> <上界> [小数位]    随机生成n个范围内的浮点数，默认3位小数")
        print()
        print("数字范围限制为 ±10**20，n最大为20", end = '')

    # 1-100
    elif l[0] == "":
        print("执行指令：")
        print("1~100中随机整数")
        return [randint(1, 100)]

    # 不重复元素 c
    elif l[0] == "c":
        if len(l) < 3:
            print("[错误] 参数不足")
            print("#rd c <n> <元素列表>   抽取n个不重复的元素", end = '')
            return []
        n = check_num(l[1], "int")
        check_range(1, 2, n)
        elements = l[2:]
        shuffle(elements)
        if n > len(elements):
            print("[错误] 抽取失败：元素数量不足", end = '')
            return []
        print("执行指令：")
        print(f"抽取{n}个不重复的元素")
        return elements[:n]
    
    # 可重复元素 r
    elif l[0] == "r":
        if len(l) < 3:
            print("[错误] 参数不足")
            print("#rd r <n> <元素列表>   抽取n个可重复的元素", end = '')
            return []
        n = check_num(l[1], "int")
        check_range(1, 2, n)
        elements = l[2:]
        print("执行指令：")
        print(f"抽取{n}个可重复的元素")
        return [choice(elements) for _ in range(n)]

    # 可重复元素（输出个数） rn
    elif l[0] == "rn":
        if len(l) < 3:
            print("[错误] 参数不足")
            print("#rd rn <n> <元素列表>   抽取n个可重复的元素（仅显示个数）", end = '')
            return []
        n = check_num(l[1], "int")
        check_range(1, 2, 20)
        elements = l[2:]
        if n > 10**6:
            print("[错误] 抽取失败：n不能大于1000000", end = '')
            return []
        if len(set(elements)) > 20:
            print("[错误] 抽取失败：rn抽取时不同的元素数量不能大于20个", end = '')
            return []
        print("执行指令：")
        print(f"抽取{n}个可重复的元素")
        counter = Counter([choice(elements) for _ in range(n)])
        return [f"{key} ×{value}" for key, value in sorted(counter.items())]

    # 1个整数 i
    elif l[0] == "i":
        if len(l) < 2:
            print("[错误] 参数不足")
            print("#rd i [下界] <上界>   随机生成1个整数", end = '')
            return []
        start = 1 if len(l) == 2 else check_num(l[1], "int")
        end = check_num(l[1], "int") if len(l) == 2 else check_num(l[2], "int")
        check_range(start, end, 1)
        print("执行指令：")
        print(f"{start}~{end}中随机整数")
        return [randint(start, end)]

    # n个不重复整数 ic
    elif l[0] == "ic":
        if len(l) < 3:
            print("[错误] 参数不足")
            print("#rd ic <n> [下界] <上界>   随机生成n个不重复的整数", end = '')
            return []
        n = check_num(l[1], "int")
        start = 1 if len(l) == 3 else check_num(l[2], "int")
        end = check_num(l[2], "int") if len(l) == 3 else check_num(l[3], "int")
        check_range(start, end, n)
        if n > end - start + 1:
            print("[错误] 抽取失败：范围内整数不足", end = '')
            return []
        print("执行指令：")
        print(f"{start}~{end}中随机{n}个不重复整数")
        nums = [i for i in range(start, end + 1)]
        shuffle(nums)
        return nums[:n]

    # n个可重复整数 ir
    elif l[0] == "ir":
        if len(l) < 3:
            print("[错误] 参数不足")
            print("#rd ir <n> [下界] <上界>   随机生成n个可重复的整数", end = '')
            return []
        n = check_num(l[1], "int")
        start = 1 if len(l) == 3 else check_num(l[2], "int")
        end = check_num(l[2], "int") if len(l) == 3 else check_num(l[3], "int")
        check_range(start, end, n)
        print("执行指令：")
        print(f"{start}~{end}中随机{n}个可重复整数")
        return [randint(start, end) for _ in range(n)]

    # n个浮点数 f
    elif l[0] == "f":
        if len(l) < 4:
            print("[错误] 参数不足")
            print("#rd f <n> <下界> <上界> [小数位]    随机生成n个范围内的浮点数", end = '')
            return []
        n = check_num(l[1], "int")
        start = check_num(l[2], "float")
        end = check_num(l[3], "float")
        decimal = 3 if len(l) == 4 else check_num(l[4], "int")
        if decimal > 20:
            print("[错误] 抽取失败：小数位数不能大于20", end="")
            return []
        check_range(start, end, n)
        print("执行指令：")
        print(f"{start}~{end}中随机{n}个{decimal}位浮点数")
        return [f"{randint(start*10**decimal, end*10**decimal)/10**decimal:.{decimal}f}" for _ in range(n)]

    # 多骰子求和 XdY
    elif len(l[0]) >= 3:
        try:
            global time_
            time_ = int(l[1])
            result = []
            if time_ > 30:
                time_ = 30
            if time_ == 0:
                raise ValueError
            for _ in range(0, time_):
                result.append(dice(l[0]))
                if end_:
                    break
            return result
        except:
            if len(l) >= 2:
                print("[警告] 次数必须为正整数")
        result = dice(l[0])
        return [] if result is None else [result]

    else:
        print("不支持的参数：" + l[0])
        print("请使用「#rd help」查看指令帮助，或「#rd info」查看程序简介", end = '')
    return []

lst = list(input().split())
if len(lst) == 0:
    lst = [""]
try:
    result = run_rd_cmds(lst)
except Exception as e:
    print("\n[执行失败] 发生了意料之外的错误，请联系铁蛋修复:", repr(e), end = '')
    result = []
if len(result) > 0 and result[0] != []:
    if len(lst[0]) < 3:
        print("随机结果：")
        for i in range(len(result)):
            print(result[0] if i == 0 else f"\n{result[i]}", end = '')
    else:
        for i in range(len(result)):
            print("运算结果：" if len(result) == 1 else f"运算结果[1]：" if i == 0 else f"\n运算结果[{i+1}]：")
            print(result[0] if i == 0 else result[i], end = '')
        
