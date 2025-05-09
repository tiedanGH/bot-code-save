import json

json_input = input()
data_input = json.loads(json_input)
images = data_input["images"]

markdown = ""
for image in images:
    markdown += f"链接：{image['url']}<br>\n"
    if not image["error"]:
        markdown += f"![base64image]({image['base64']})<br>\n"
    else:
        markdown += image["error"] + "<br>\n"
print(markdown)
