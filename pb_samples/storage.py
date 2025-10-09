# 导入json库
import json

# 读取json输入（例如：{"storage":"storage数据","global":"global数据","userID":1145141919810,"nickname":"昵称","from":"private"}）
json_input = input()
# 读取用户输入
try:
    stdin = input()
except:
    stdin = ''

# 转换json输入为字典
data_input = json.loads(json_input)

# 初始化输出用的字典
data_output = {}

# 修改用户数据+1
try:
    data_output['storage'] = str(int(data_input['storage']) + 1) + '\n123'
except:
    data_output['storage'] = str(1)

# 如果输入是'clear'，则清除用户存储数据
if stdin == 'clear':
    data_output['storage'] = ''

# 修改全局存储数据（此处例子：改为将上次执行用户的昵称）
data_output['global'] = data_input['nickname']

# 将输入内容放在'content'中（此处例子：输出上次存档信息）
# 注：`from`参数用于判断用户的执行环境，群聊group/私信private
data_output['content'] = '读取的存档信息：\nstorage: ' + data_input['storage'] + '\nglobal: ' + data_input['global'] + '\nuserID: ' + str(data_input['userID']) + '\nnickname: ' + data_input['nickname'] + '\nfrom: ' + str(data_input['from']) + '\n程序输入: ' + stdin

# 转换字典为json输出
json_output = json.dumps(data_output)

# 输出最终json字符串
print(json_output)
