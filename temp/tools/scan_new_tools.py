"""
scan_new_tools.py - 定期扫描temp/tools新增工具并更新skill_tree

功能：
1. 扫描temp/tools目录，识别未在skill_tree中的工具
2. 使用LLM推断工具的类别和技能归属
3. 自动添加到skill_tree.json
4. 生成扫描报告

使用：
- 自主探索时自动调用
- 或手动执行：python scan_new_tools.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'skill_tree'))
from skill_tree_api import SkillTree

def scan_new_tools(tools_dir='./tools', dry_run=False):
    """
    扫描新工具
    
    Args:
        tools_dir: 工具目录路径
        dry_run: 仅扫描不更新
    
    Returns:
        扫描报告字典
    """
    st = SkillTree('./skill_tree/skill_tree.json')
    
    # 1. 获取skill_tree中已有的工具
    with open('./skill_tree/skill_tree.json', 'r', encoding='utf-8') as f:
        tree = json.load(f)
    
    existing_tools = set()
    for cat_skills in tree['skill_categories'].values():
        for skill_data in cat_skills.values():
            existing_tools.update(skill_data['tools'])
    
    # 2. 扫描tools目录
    if not os.path.exists(tools_dir):
        return {'error': f'目录不存在: {tools_dir}'}
    
    tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.py')]
    
    # 3. 识别新工具（排除测试/示例文件）
    new_tools = []
    for tool in tool_files:
        # 跳过测试和示例文件
        if tool.startswith('test_') or 'example' in tool.lower():
            continue
        
        if tool not in existing_tools:
            # 读取文件头部注释判断用途
            tool_path = os.path.join(tools_dir, tool)
            with open(tool_path, 'r', encoding='utf-8') as f:
                first_lines = ''.join(f.readlines()[:20])
            
            new_tools.append({
                'filename': tool,
                'preview': first_lines[:200]
            })
    
    # 4. 生成报告
    report = {
        'scan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_files': len(tool_files),
        'existing_count': len(existing_tools),
        'new_tools_count': len(new_tools),
        'new_tools': new_tools,
        'dry_run': dry_run
    }
    
    # 5. 如果不是dry_run，需要LLM推断类别（这里先返回报告，由调用者决定）
    if not dry_run and new_tools:
        report['action_required'] = 'LLM需要推断这些工具的类别和技能归属'
    
    return report


def infer_tool_category(tool_name, preview_text):
    """
    根据工具名和预览文本推断类别（简单规则，复杂情况需要LLM）
    
    Returns:
        (category, skill) 或 None
    """
    # 简单规则映射
    rules = {
        'video': ('video_editing', 'video_processing'),
        'audio': ('video_editing', 'audio_processing'),
        'image': ('media_processing', 'image_processing'),
        'email': ('communication', 'wechat_bot'),  # 暂时放这里，后续可能需要新技能
        'wechat': ('communication', 'wechat_bot'),
        'adb': ('mobile_control', 'android_ui'),
        'ios': ('mobile_control', 'android_ui'),  # 暂时放这里
        'chart': ('document_generation', 'ppt_creation'),  # 图表相关
        'plot': ('document_generation', 'ppt_creation'),
        'web': ('web_automation', 'web_scraping'),
        'scraping': ('web_automation', 'web_scraping'),
        'bilibili': ('web_automation', 'content_extraction'),
        'disk': ('system_management', 'disk_management'),
        'schedule': ('task_orchestration', 'scheduled_tasks'),
    }
    
    tool_lower = tool_name.lower()
    preview_lower = preview_text.lower()
    
    for keyword, (cat, skill) in rules.items():
        if keyword in tool_lower or keyword in preview_lower:
            return (cat, skill)
    
    return None


def add_new_tools_auto(new_tools_list):
    """
    自动添加新工具到skill_tree
    
    Args:
        new_tools_list: scan_new_tools返回的new_tools列表
    
    Returns:
        添加结果
    """
    st = SkillTree('./skill_tree/skill_tree.json')
    results = []
    
    for tool_info in new_tools_list:
        filename = tool_info['filename']
        preview = tool_info['preview']
        
        # 推断类别
        inferred = infer_tool_category(filename, preview)
        
        if inferred:
            cat, skill = inferred
            success = st.add_tool(cat, skill, filename)
            results.append({
                'tool': filename,
                'category': cat,
                'skill': skill,
                'success': success
            })
        else:
            results.append({
                'tool': filename,
                'category': None,
                'skill': None,
                'success': False,
                'reason': '无法推断类别，需要手动分类'
            })
    
    return results


if __name__ == '__main__':
    # 执行扫描
    report = scan_new_tools(dry_run=False)
    
    print("=== 工具扫描报告 ===")
    print(f"扫描时间: {report['scan_time']}")
    print(f"总文件数: {report['total_files']}")
    print(f"已在skill_tree: {report['existing_count']}")
    print(f"新发现工具: {report['new_tools_count']}")
    
    if report['new_tools']:
        print("\n新工具列表:")
        for tool in report['new_tools']:
            print(f"  - {tool['filename']}")
        
        # 自动添加
        print("\n正在自动添加...")
        results = add_new_tools_auto(report['new_tools'])
        
        print("\n添加结果:")
        for r in results:
            if r['success']:
                print(f"  [OK] {r['tool']} -> {r['category']}.{r['skill']}")
            else:
                print(f"  [FAIL] {r['tool']} - {r.get('reason', '添加失败')}")
    else:
        print("\n✓ 无新工具")
