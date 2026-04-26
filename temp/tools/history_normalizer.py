#!/usr/bin/env python3
"""
history_normalizer.py
修复 autonomous_reports/history.txt 的格式粘连问题。

问题：多条记录粘连在同一行，R标记无法被正则独立解析。
目标格式：每条 history 单行记录格式为
  RXX | 日期 | 类型 | 主题 | 结论
非单行记录（报告正文）独立保留，但与其他记录之间有空行分隔。

策略：
1. 读取原始内容
2. 按已知的 R标记模式分割，提取所有可识别的单行记录
3. 非结构化大块内容（报告正文）单独保留
4. 输出规范化版本（backup原始文件）
"""

import re
import os
import shutil
from datetime import datetime

HISTORY_PATH = r'E:\2026\x-fudan\new\GenericAgent\temp\autonomous_reports\history.txt'
BACKUP_PATH = HISTORY_PATH + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S')

def normalize_history():
    with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
        raw = f.read()

    print(f"原始文件大小: {len(raw)} 字符")

    # 备份原始文件
    shutil.copy2(HISTORY_PATH, BACKUP_PATH)
    print(f"备份至: {BACKUP_PATH}")

    # 策略：找到所有 [RXX] 或 RXX | 模式的起始位置，拆分内容块
    # 匹配模式：
    #   (1) [RXX] ... （单行agent日志）
    #   (2) RXX | 日期 | ... （标准history单行）
    #   (3) # R42 — ... （报告正文标题，独立块）
    #   (4) [Agent] ... （agent运行日志，单行）
    #   (5) [2026-...] ... （时间戳行）

    # 先按换行符分割已有的行
    lines = raw.split('\n')
    print(f"原始行数: {len(lines)}")

    # 对每一行，检查是否包含多个R记录粘连
    # 粘连特征：行内出现多个 [RXX] 或 RXX | 模式
    
    expanded_lines = []
    
    # 正则：匹配单行history记录的起始（用于拆分粘连）
    splitter = re.compile(
        r'(?='  # lookahead，不消耗
        r'(?:\[R\d+\]|R\d+\s*\||\# R\d+|'  # R标记
        r'\[Agent\]\s|'                       # Agent日志
        r'\[2\d{3}-\d{2}-\d{2}'             # 时间戳
        r'))'
    )

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            expanded_lines.append('')
            continue

        # 检测行内是否有多个标记（粘连）
        parts = splitter.split(line)
        parts = [p.strip() for p in parts if p.strip()]

        if len(parts) <= 1:
            expanded_lines.append(line)
        else:
            print(f"  行{i+1}: 检测到{len(parts)}个粘连块，拆分")
            for p in parts:
                expanded_lines.append(p)
            # 拆分后各块之间加空行
            expanded_lines.append('')

    # 去除多余空行（连续空行合并为一个）
    result_lines = []
    prev_empty = False
    for line in expanded_lines:
        if line == '':
            if not prev_empty:
                result_lines.append('')
            prev_empty = True
        else:
            result_lines.append(line)
            prev_empty = False

    # 去除开头结尾空行
    while result_lines and result_lines[0] == '':
        result_lines.pop(0)
    while result_lines and result_lines[-1] == '':
        result_lines.pop()

    result = '\n'.join(result_lines) + '\n'

    # 统计修复后的R标记数量
    r_marks_before = len(re.findall(r'\bR\d+\b', raw))
    r_marks_after = len(re.findall(r'\bR\d+\b', result))
    standalone_entries = re.findall(r'^R\d+\s*\|', result, re.MULTILINE)
    print(f"\n修复后行数: {len(result_lines)}")
    print(f"R标记数(修复前): {r_marks_before}")
    print(f"R标记数(修复后): {r_marks_after}")
    print(f"独立单行R条目数: {len(standalone_entries)}")
    print("独立条目列表:")
    for e in standalone_entries:
        print(f"  {e[:80]}")

    with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"\n✅ 规范化完成，写入 {HISTORY_PATH}")

    return len(standalone_entries)

if __name__ == '__main__':
    count = normalize_history()
    print(f"\n最终独立R条目数: {count}")