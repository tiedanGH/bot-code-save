import json

data_output = {}
data_output["format"] = "MultipleMessage"
data_output["at"] = False

data_output["messageList"] = [{"content": message} for message in input().split()]

json_output = json.dumps(data_output)
print(json_output)
