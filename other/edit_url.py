import re

input_file = 'input.txt'
output_file = 'output.txt'

count = 0
results = []

# 读取并处理每一行
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # 替换图片名
        modified = re.sub(r'(\w+)\.(jpe?g|png)$', r'\1.md.\2', line, flags=re.IGNORECASE)
        results.append(modified)
        if modified != line:
            count += 1

# 写入结果
with open(output_file, 'w', encoding='utf-8') as f:
    for item in results:
        f.write(item + '\n')

print(f'修改了 {count} 条图片数据')
