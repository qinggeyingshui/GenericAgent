"""
autonomous_task.py - 自主行动任务管理API
放置: memory/autonomous_operation_sop/
用法: import autonomous_task (或 from autonomous_operation_sop import autonomous_task)

5个函数:
  get_todo()        → 返回TODO内容
  get_history(n)    → 返回最近n条历史
  complete_task()   → 移报告+编号+写history+从sop_files同步skill_tree+返回改TODO指令
  update_skill_tree() → 自动更新skill_tree（从TODO解析领域+AST扫描函数）
  record_skill_usage() → 记录SOP使用（日常任务中更新usage_count和last_used）
"""

import os
import re
import shutil
import json
import ast
from pathlib import Path
from datetime import datetime

# ── 路径计算（基于模块自身位置） ──
_MODULE_DIR = Path(__file__).resolve().parent          # memory/autonomous_operation_sop/
_MEMORY_DIR = _MODULE_DIR.parent                       # memory/
_AGENT_DIR = _MEMORY_DIR.parent                        # GenericAgent/
_TEMP_DIR = _AGENT_DIR / "temp"                        # GenericAgent/temp/
_REPORTS_DIR = _TEMP_DIR / "autonomous_reports"
_HISTORY_FILE = _REPORTS_DIR / "history.txt"
_TODO_FILE = _TEMP_DIR / "TODO.txt"


def _next_report_number() -> int:
    """扫 history.txt 第一行提取最大 RXX 编号，返回下一个"""
    if not _HISTORY_FILE.exists():
        return 1
    with open(_HISTORY_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    # 匹配所有 R 后跟数字的模式
    nums = [int(m) for m in re.findall(r'R(\d+)', content)]
    if not nums:
        return 1
    return max(nums) + 1


def get_todo() -> str:
    """返回 TODO.txt 的内容。若文件不存在返回提示。"""
    if not _TODO_FILE.exists():
        return f"[autonomous_task] TODO.txt 不存在，路径: {_TODO_FILE}"
    with open(_TODO_FILE, "r", encoding="utf-8") as f:
        return f.read()


def get_history(n: int = 20) -> str:
    """返回 history.txt 的前 n 行（最新在前）。"""
    if not _HISTORY_FILE.exists():
        return f"[autonomous_task] history.txt 不存在，路径: {_HISTORY_FILE}"
    with open(_HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return "".join(lines[:n])


def _parse_skill_mapping_from_sop(sop_path):
    """从SOP文件解析[skill_mapping]标签（支持新格式）"""
    try:
        with open(sop_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '[skill_mapping]' not in content:
            return None
        
        start = content.find('[skill_mapping]')
        end = content.find('[/skill_mapping]', start)
        if end == -1:
            return None
        
        block = content[start:end].strip()
        lines = [l.strip() for l in block.split('\n') if l.strip() and not l.strip().startswith('[')]
        
        result = {}
        for line in lines:
            if ':' in line:
                key, val = line.split(':', 1)
                result[key.strip()] = val.strip()
        
        if 'category' in result and 'skill' in result:
            tools_str = result.get('tools', '')
            tools = [t.strip() for t in tools_str.split(',') if t.strip()] if tools_str else []
            return {
                'category': result['category'],
                'skill': result['skill'],
                'tools': tools,
                'sop': sop_path.name
            }
        return None
    except Exception:
        return None


def set_todo(*args, **kwargs) -> str:
    """返回 TODO.txt 的真实绝对路径，供 agent/子agent 自行读写。"""
    return f'路径: {str(_TODO_FILE)}'


def complete_task(taskname: str, historyline: str, report_path: str, sop_files: list = None) -> str:
    """
    完成任务的原子操作：
    1. 移动 report_path → autonomous_reports/R{XX}_{taskname}.md（自动编号）
    2. prepend historyline 到 history.txt（校验必须单行）
    3. 从sop_files同步[skill_mapping]到skill_tree.json
    4. 返回字符串指示 agent 自己去改 TODO

    Args:
        taskname: 任务简短名称（用于报告文件名，如 "晨间简报"）
        historyline: 历史记录内容（必须单行，日期自动添加，如 "工程 | 晨间简报 | 完成7模块聚合"）
        report_path: agent 已写好的报告文件路径（绝对或相对于cwd）
        sop_files: 本次使用的SOP文件列表，如 ["ppt_com_sop.md"]，用于更新skill_tree

    Returns:
        成功消息 + 改TODO指令，或错误消息
    """
    errors = []

    # ── 校验 ──
    if "\n" in historyline.strip():
        return "[ERROR] historyline 必须是单行，不能包含换行符"

    report = Path(report_path).resolve()
    if not report.exists():
        return f"[ERROR] 报告文件不存在: {report_path}"

    if not _REPORTS_DIR.exists():
        _REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # ── 1. 移动报告 ──
    rnum = _next_report_number()
    # 清理 taskname 中的非法文件名字符
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', taskname).strip()
    dest_name = f"R{rnum}_{safe_name}.md"
    dest_path = _REPORTS_DIR / dest_name

    try:
        shutil.move(str(report), str(dest_path))
    except Exception as e:
        return f"[ERROR] 移动报告失败: {e}"

    # ── 2. prepend history ──
    # 自动加编号 + 日期（剥离 agent 可能已写的编号/日期，统一重建）
    line = historyline.strip()
    line = re.sub(r'^R\d+\s*\|\s*', '', line)           # 剥离 R 编号
    line = re.sub(r'^\d{4}-\d{2}-\d{2}\s*\|\s*', '', line)  # 剥离日期
    today = datetime.now().strftime('%Y-%m-%d')
    line = f"R{rnum} | {today} | {line}"

    try:
        existing = ""
        if _HISTORY_FILE.exists():
            with open(_HISTORY_FILE, "r", encoding="utf-8") as f:
                existing = f.read()
        with open(_HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write(line + "\n" + existing)
    except Exception as e:
        # 回滚：把报告移回去
        try:
            shutil.move(str(dest_path), str(report))
        except:
            pass
        return f"[ERROR] 写入 history 失败: {e}（报告已回滚）"

    # ── 3. 从sop_files同步[skill_mapping]到skill_tree ──
    skill_info = ""
    if sop_files is None or len(sop_files) == 0:
        skill_info = (
            "\n⚠️ 警告：未提供sop_files参数，skill_tree未更新！\n"
            "如果本次任务使用了SOP，请重新调用：\n"
            f"  complete_task('{taskname}', '{historyline}', '{report_path}', sop_files=['xxx_sop.md'])"
        )
    else:
        try:
            tree_path = _MODULE_DIR / "skill_tree.json"
            with open(tree_path, 'r', encoding='utf-8') as f:
                tree_data = json.load(f)
            
            updated_sops = []
            sop_errors = []
            
            for sop_file in sop_files:
                sop_path = _MEMORY_DIR / sop_file
                if not sop_path.exists():
                    sop_errors.append(f"文件不存在: {sop_file}")
                    continue
                
                mapping = _parse_skill_mapping_from_sop(sop_path)
                if not mapping:
                    sop_errors.append(f"缺少[skill_mapping]: {sop_file}")
                    continue
                
                cat = mapping['category']
                skill = mapping['skill']
                tools = mapping.get('tools', [])
                
                # 确保category存在
                if cat not in tree_data['skill_categories']:
                    tree_data['skill_categories'][cat] = {}
                
                # 更新或创建skill
                if skill not in tree_data['skill_categories'][cat]:
                    tree_data['skill_categories'][cat][skill] = {
                        'sop': sop_file,
                        'tools': tools,
                        'functions': [],
                        'usage_count': 1,
                        'last_used': datetime.now().strftime("%Y-%m-%d")
                    }
                else:
                    skill_data = tree_data['skill_categories'][cat][skill]
                    skill_data['usage_count'] += 1
                    skill_data['last_used'] = datetime.now().strftime("%Y-%m-%d")
                    skill_data['sop'] = sop_file
                    skill_data['tools'] = tools  # 与SOP保持一致
                
                # 扫描.py工具提取functions
                for tool in tools:
                    if not tool.endswith('.py'):
                        continue
                    tool_path = None
                    for base in [_TEMP_DIR / "tools", _TEMP_DIR, _MEMORY_DIR]:
                        candidate = base / tool
                        if candidate.exists():
                            tool_path = candidate
                            break
                    if tool_path and tool_path.exists():
                        try:
                            with open(tool_path, 'r', encoding='utf-8') as f:
                                tree = ast.parse(f.read())
                            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                            skill_data = tree_data['skill_categories'][cat][skill]
                            skill_data['functions'] = sorted(list(set(skill_data.get('functions', []) + functions)))
                        except Exception:
                            pass
                
                updated_sops.append(sop_file)
            
            tree_data['last_updated'] = datetime.now().strftime("%Y-%m-%d")
            with open(tree_path, 'w', encoding='utf-8') as f:
                json.dump(tree_data, f, indent=2, ensure_ascii=False)
            
            if updated_sops:
                skill_info = f"\n✅ 已更新skill_tree: {', '.join(updated_sops)}"
            if sop_errors:
                skill_info += f"\n⚠️ 部分SOP处理失败: {'; '.join(sop_errors)}"
        except Exception as e:
            skill_info = f"\n⚠️ skill_tree更新失败: {e}"
    
    # ── 4. 验证history.txt更新成功 ──
    try:
        with open(_HISTORY_FILE, 'r', encoding='utf-8') as f:
            history_content = f.read()
        if f"R{rnum}" not in history_content:
            return f"⚠️ 警告：报告已保存但history.txt未包含R{rnum}记录！\n报告路径: {dest_name}\n请手动检查history.txt"
    except Exception as e:
        return f"⚠️ 警告：无法验证history.txt更新状态: {e}\n报告路径: {dest_name}"
    
    # ── 5. 返回改 TODO 指令 ──
    return (
        f"✅ 完成！报告已保存: {dest_name}\n"
        f"历史已记录: {line}"
        f"{skill_info}\n"
        f"👉 请在 {_TODO_FILE} 中将对应任务标记为 [x] R{rnum}"
    )


def update_skill_tree(task_title: str, tool_file: str = None) -> str:
    """
    自动更新skill_tree.json
    1. 从TODO解析任务的领域（category）
    2. 从tool_file用AST提取函数列表
    3. 更新skill_tree.json的tools和functions
    
    Args:
        task_title: 任务标题（用于从TODO匹配）
        tool_file: 工具文件路径（相对于temp/tools/或绝对路径）
    
    Returns:
        更新结果信息
    """
    try:
        # 1. 从TODO解析category
        todo_content = get_todo()
        category = None
        
        for line in todo_content.split('\n'):
            if task_title in line and '[ ]' in line:
                match = re.search(r'\[\s*\]\s*(\w+)\s*\|', line)
                if match:
                    category = match.group(1)
                    break
        
        if not category:
            return f"⚠️ 无法从TODO解析领域信息（任务：{task_title}）"
        
        # 2. 定位工具文件
        if not tool_file:
            return "⚠️ 未指定工具文件"
        
        tool_path = Path(tool_file)
        if not tool_path.is_absolute():
            # 尝试在temp/和temp/tools/中查找
            for base in [_TEMP_DIR, _TEMP_DIR / "tools"]:
                candidate = base / tool_file
                if candidate.exists():
                    tool_path = candidate
                    break
        
        if not tool_path.exists():
            return f"⚠️ 工具文件不存在: {tool_path}"
        
        # 3. 用AST提取函数列表
        with open(tool_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_'):  # 排除私有函数
                    functions.append(node.name)
        
        if not functions:
            return f"⚠️ 未在{tool_path.name}中找到公开函数"
        
        # 4. 推断skill名称（从工具文件名或任务标题）
        skill_name = tool_path.stem.replace('_toolkit', '').replace('_tool', '')
        
        # 5. 更新skill_tree.json
        tree_path = _MODULE_DIR / "skill_tree.json"
        with open(tree_path, 'r', encoding='utf-8') as f:
            tree_data = json.load(f)
        
        # 确保category存在
        if 'skill_categories' not in tree_data:
            tree_data['skill_categories'] = {}
        if category not in tree_data['skill_categories']:
            tree_data['skill_categories'][category] = {}
        
        # 确保skill存在
        if skill_name not in tree_data['skill_categories'][category]:
            tree_data['skill_categories'][category][skill_name] = {
                'tools': [],
                'functions': [],
                'usage_count': 0,
                'last_used': None
            }
        
        skill_data = tree_data['skill_categories'][category][skill_name]
        
        # 添加工具（去重）
        if tool_path.name not in skill_data['tools']:
            skill_data['tools'].append(tool_path.name)
        
        # 添加函数（去重并排序）
        skill_data['functions'] = sorted(list(set(skill_data.get('functions', []) + functions)))
        
        # 保存
        with open(tree_path, 'w', encoding='utf-8') as f:
            json.dump(tree_data, f, indent=2, ensure_ascii=False)
        
        return (
            f"✓ 更新skill_tree: {category}.{skill_name}\n"
            f"  - 工具: {tool_path.name}\n"
            f"  - 函数: {', '.join(functions)}"
        )
        
    except Exception as e:
        import traceback
        return f"⚠️ 更新skill_tree失败: {e}\n{traceback.format_exc()}"


def record_skill_usage(sop_file: str) -> str:
    """
    记录SOP使用情况，更新skill_tree的usage_count和last_used
    用于日常任务中追踪SOP使用频率
    
    Args:
        sop_file: SOP文件名，如 "ppt_com_sop.md"
    
    Returns:
        更新结果信息
    """
    try:
        sop_path = _MEMORY_DIR / sop_file
        if not sop_path.exists():
            return f"⚠️ SOP文件不存在: {sop_file}"
        
        # 读取SOP的[skill_mapping]
        mapping = _parse_skill_mapping_from_sop(sop_path)
        if not mapping:
            return f"⚠️ SOP缺少[skill_mapping]: {sop_file}"
        
        # 读取skill_tree
        tree_path = _MODULE_DIR / "skill_tree.json"
        if not tree_path.exists():
            return f"⚠️ skill_tree.json不存在"
        
        with open(tree_path, 'r', encoding='utf-8') as f:
            tree_data = json.load(f)
        
        cat = mapping['category']
        skill = mapping['skill']
        
        # 确保category存在
        if cat not in tree_data.get('skill_categories', {}):
            tree_data.setdefault('skill_categories', {})[cat] = {}
        
        # 更新或创建skill
        if skill in tree_data['skill_categories'][cat]:
            skill_data = tree_data['skill_categories'][cat][skill]
            skill_data['usage_count'] += 1
            skill_data['last_used'] = datetime.now().strftime("%Y-%m-%d")
            skill_data['sop'] = sop_file
            skill_data['tools'] = mapping.get('tools', [])
        else:
            tree_data['skill_categories'][cat][skill] = {
                'sop': sop_file,
                'tools': mapping.get('tools', []),
                'functions': [],
                'usage_count': 1,
                'last_used': datetime.now().strftime("%Y-%m-%d")
            }
        
        tree_data['last_updated'] = datetime.now().strftime("%Y-%m-%d")
        
        with open(tree_path, 'w', encoding='utf-8') as f:
            json.dump(tree_data, f, indent=2, ensure_ascii=False)
        
        return f"✅ 已记录: {cat}.{skill} (usage_count: {tree_data['skill_categories'][cat][skill]['usage_count']})"
        
    except Exception as e:
        return f"⚠️ 记录失败: {e}"




def get_skill_stats() -> dict:
    """
    读取skill_tree.json，返回统计信息。
    返回: {
        'total': int,
        'categories': {cat: count},
        'high_usage': [(name, usage, category), ...],  # usage>=5
        'all_skills': [(name, usage, category, last_used), ...]
    }
    """
    skill_tree_path = _MODULE_DIR / "skill_tree.json"
    if not skill_tree_path.exists():
        return {'total': 0, 'categories': {}, 'high_usage': [], 'all_skills': []}
    
    with open(skill_tree_path, 'r', encoding='utf-8') as f:
        tree = json.load(f)
    
    categories = {}
    all_skills = []
    high_usage = []
    
    # 遍历嵌套结构: skill_categories -> category -> skill_name -> {usage_count, last_used, ...}
    for cat, skills in tree.get('skill_categories', {}).items():
        skill_count = 0
        for skill_name, info in skills.items():
            if isinstance(info, dict):
                usage = info.get('usage_count', 0)
                last_used = info.get('last_used', '')
                all_skills.append((skill_name, usage, cat, last_used))
                if usage >= 5:
                    high_usage.append((skill_name, usage, cat))
                skill_count += 1
        categories[cat] = skill_count
    
    # 按usage降序排序
    high_usage.sort(key=lambda x: -x[1])
    all_skills.sort(key=lambda x: -x[1])
    
    return {
        'total': len(all_skills),
        'categories': categories,
        'high_usage': high_usage,
        'all_skills': all_skills
    }

# ── 快速自检 ──
if __name__ == "__main__":
    print(f"TEMP_DIR:    {_TEMP_DIR}")
    print(f"REPORTS_DIR: {_REPORTS_DIR}")
    print(f"HISTORY:     {_HISTORY_FILE}")
    print(f"TODO:        {_TODO_FILE}")
    print(f"Next R#:     R{_next_report_number()}")
    print(f"\n--- TODO ---\n{get_todo()[:200]}")
    print(f"\n--- History (5) ---\n{get_history(5)}")