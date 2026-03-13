#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import re

pattern = re.compile(r"^(\d{4}-\d{2})-\d{2}\.log$")

# 按月份分组
month_files = defaultdict(list)

for path in Path(".").iterdir():
    if path.is_file():
        match = pattern.match(path.name)
        if match:
            month = match.group(1)
            month_files[month].append(path)

# 合并每个月的日志
for month, files in sorted(month_files.items()):
    output_file = Path(f"{month}.log")

    with output_file.open("w", encoding="utf-8") as outfile:
        for file in sorted(files):
            with file.open("r", encoding="utf-8") as infile:
                outfile.write(infile.read())

    print(f"已生成: {output_file}")