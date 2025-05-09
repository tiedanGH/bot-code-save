import json

json_input = input()

data_input = json.loads(json_input)
data_output = {}
data_output['storage'] = "激活存储"
data_output['content'] = f"global数据大小：{len(data_input['global'])}"

print(json.dumps(data_output))
