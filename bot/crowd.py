#!/usr/bin/env python3

import os
import sys
import json
from collections import defaultdict

# ========= 全部json的目录路径 =========
DATA_DIR = "../lgtbot-mirai/build/crowd_json_saves"
# ======================================


def compress_ranges(nums, prefix=""):
    if not nums:
        return []

    nums = sorted(nums)
    result = []
    start = prev = nums[0]

    for n in nums[1:]:
        if n == prev + 1:
            prev = n
        else:
            result.append(
                f"{prefix}{start}" if start == prev
                else f"{prefix}{start}-{prefix}{prev}"
            )
            start = prev = n

    result.append(
        f"{prefix}{start}" if start == prev
        else f"{prefix}{start}-{prefix}{prev}"
    )
    return result

def format_question_list(all_questions):
    normal = []
    t_nums = []

    for q in all_questions:
        if q.isdigit():
            normal.append(int(q))
        elif q.startswith("t") and q[1:].isdigit():
            t_nums.append(int(q[1:]))

    return compress_ranges(normal) + compress_ranges(t_nums, "t")


def load_all_json_files(directory):
    all_data = []

    if not os.path.isdir(directory):
        print(f"错误：数据目录不存在 -> {directory}")
        sys.exit(1)

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_data.append(data)
            except Exception as e:
                print(f"警告：读取文件失败 {filename} -> {e}")

    return all_data


def print_basic_statistics(all_data):
    total_files = len(all_data)

    # bot字段为空数组的文件数
    non_bot_files = sum(
        1 for data in all_data
        if isinstance(data.get("bot", None), list) and len(data.get("bot", [])) == 0
    )

    # 统计ques中不重复题目数量
    unique_questions = set()
    for data in all_data:
        for q in data.get("ques", []):
            unique_questions.add(q)

    print("《乌合之众》数据统计")
    print()
    print(f"统计对局总数：{total_files}")
    print(f"不含bot对局：{non_bot_files}")
    print(f"统计题目总数：{len(unique_questions)}")
    print()
    print("➡️ 乌合查询 <题号>")


def analyze_question(all_data, question_id):
    option_counter = defaultdict(int)
    total_count = 0
    found = False
    appear_count = 0

    # 收集所有可查询题号
    all_questions = set()
    for data in all_data:
        for q in data.get("ques", []):
            all_questions.add(q)

    for data in all_data:
        ques_list = data.get("ques", [])
        players = data.get("player", [])

        if question_id in ques_list:
            found = True
            appear_count += 1

            index = ques_list.index(question_id)

            for player in players:
                if index < len(player):
                    choice = player[index]
                    option_counter[choice] += 1
                    total_count += 1

    if not found:
        print("❌ 未找到对应题号")
        print()
        print("可查询题号如下：")
        print(", ".join(format_question_list(all_questions)))
        return

        print(f"题号 {question_id} 统计结果：")
        print(f"出现次数：{appear_count}")
        print()

    print(f"题号 [{question_id}] 统计结果：")
    print(f"出现次数：{appear_count}")
    print()

    if total_count == 0:
        print(f"⚠ 题号 {question_id} 未找到任何玩家数据统计")
        return

    max_option = max(option_counter.keys())
    for option in range(max_option + 1):
        count = option_counter.get(option, 0)
        percent = (count / total_count) * 100 if total_count else 0
        option_label = chr(ord('A') + option)
        print(f"{option_label}：{count} 次，{percent:.2f}%")
    print("（仅统计玩家数据）")


def main():
    all_data = load_all_json_files(DATA_DIR)

    # 无参数
    if len(sys.argv) == 1:
        print_basic_statistics(all_data)
        return
    # 有参数但为空字符串
    question_id = sys.argv[1].strip()
    if question_id == "":
        print_basic_statistics(all_data)
    else:
        analyze_question(all_data, question_id)


if __name__ == "__main__":
    main()
