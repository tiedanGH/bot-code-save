import htmlTools
import numpy as np
lst = input().split()
try:
    if len(lst) < 2:
        raise
    height = int(lst[0])
    width = int(lst[1])
except:
    print("请先输入表格长度和高度，再输入内容")
    exit()
if width <= 0 or height <= 0:
    print("表格的长度和高度必须大于0")
    exit()
if len(lst) - 2 < width * height:
    lst = lst + ["　"] * (width * height - len(lst) + 2)
if len(lst) - 2 > width * height:
    lst = lst[:width * height + 2]
pos = np.array(lst[2:]).reshape(width, height)
table = htmlTools.Table(width, height)
for i in range(width):
    for j in range(height):
        table.get(i, j).set_content(pos[i][j])
print(table.to_string())