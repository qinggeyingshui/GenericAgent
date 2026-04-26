import sys
import re
import os

# 动态计算skill_tree_api路径，避免cwd依赖
_this_dir = os.path.dirname(os.path.abspath(__file__))
_skill_tree_dir = os.path.join(_this_dir, '../../memory/autonomous_operation_sop')
sys.path.insert(0, _skill_tree_dir)
from skill_tree_api import SkillTree

def track_sop_usage(sop_content):
    match = re.search(r'\[skill_mapping\]\s+([\w.]+)', sop_content)
    if match:
        mapping = match.group(1)
        category, skill = mapping.split('.')
        api = SkillTree()
        api.record_usage(category, skill)
        return f"✓ 已记录: {mapping}"
    return "⚠ 未找到skill_mapping标签"

def read_and_track(sop_path):
    with open(sop_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return track_sop_usage(content)
