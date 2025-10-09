import json
try:
    mode, string = input().split(' ', 1)
except:
    print('【字符串&json转换工具】')
    print('模式列表：')
    print('1-将字符串编码成json字符串(dumps)')
    print('2-将json解码成字符串(loads)')
    print()
    print('#run 字符串工具 <模式> <输入>', end = '')
    exit()

if mode == '1':
    print(json.dumps(string))
elif mode == '2':
    if not (string.startswith('"') and string.endswith('"')):
        string = f'"{string}"'
    print(json.loads(string))
else:
    print('[错误] 不支持的模式', end = '')
