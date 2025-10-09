# 导入额外文件（此文件会在配置辅助文件为“htmlTools.py”时一起上传至glot。源代码请查看：https://pastebin.ubuntu.com/p/3K3Ct6hdJd/）
import htmlTools

# 创建新的Table对象（2*3）
table = htmlTools.Table(2, 3)

# 设置内容和样式（具体例子见下方）
'''
- class Box中的方法
set_content(content) -> Box   设置单元格内容
get_content() -> str   获取单元格内容
set_color() -> Box   设置单元格背景颜色
set_style() -> Box   设置单元格样式
is_visible() -> bool   单元格是否有效（如果被其他单元格merge合并，则返回False）

- class Table中的方法
to_string() -> str   将表格转换至HTML字符串
get(row, column) -> Box   获取对应位置的单元格对象（row和column从0开始编号，不能超出初始化时的大小）
merge_down(row, column, num)   在第row行第column列进行向下合并单元格，合并长度为num（合并后下方的num个单元格均不可用）
merge_right(row, column, num)   在第row行第column列进行向右合并单元格，合并长度为num（合并后右边的num个单元格均不可用）
set_table_style(style)   设置表格样式
set_row_style(style)   设置单元格样式（会被box的样式覆盖）
resize_row(row)   重置表格行数为row行，不足row行会自动补足单元格
'''
table.set_table_style(' align="center" border="2px solid black" ')      # 设置表格样式
box = table.get(0, 0)       # 获取第0行第0列的单元格对象
box.set_content("0行0列内容").set_color("yellow")       # 设置box的内容和背景颜色
table.get(0, 1).set_content("0行1列内容").set_style(' align="left" ')       # 设置第0行第1列的单元格的内容和样式
table.get(0, 2).set_content("0行2列内容")        # 设置第0行第2列的单元格的内容
table.get(1, 1).set_content("1行1列内容").set_style(' align="center" ')        # 设置第1行第1列的单元格的内容和样式
table.merge_right(1, 1, 2)       # 合并第1行第1列向右总共2个单元格

# 使用to_string()方法转换表格至HTML字符串
print(table.to_string())