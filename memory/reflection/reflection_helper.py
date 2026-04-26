import os
import sys
import subprocess
import re
from datetime import datetime

MAX_META_PATTERNS = 15  # 抽象规律上限

def spawn_reflection_agent(target_pid=None, conversation_content=None):
    """自动触发reflection agent分析错误
    
    Args:
        target_pid: 目标进程PID，如果不传则使用当前进程或查找最近修改的历史文件
        conversation_content: 直接传入的对话内容，如果提供则不从文件读取
    """
    try:
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        temp_dir = os.path.join(script_dir, 'temp')
        
        # 读取最近一个task的对话历史
        if conversation_content:
            # 直接使用传入的对话内容
            recent_history = conversation_content
        else:
            # 从文件读取
            if target_pid is None:
                pid = os.getpid()
            else:
                pid = target_pid
            history_file = os.path.join(temp_dir, 'model_responses', f'model_responses_{pid}.txt')
            
            # 如果文件不存在且没有指定PID，查找最新的历史文件
            if not os.path.exists(history_file) and target_pid is None:
                model_responses_dir = os.path.join(temp_dir, 'model_responses')
                if os.path.exists(model_responses_dir):
                    files = [f for f in os.listdir(model_responses_dir) if f.startswith('model_responses_') and f.endswith('.txt')]
                    if files:
                        files_sorted = sorted(files, key=lambda x: os.path.getmtime(os.path.join(model_responses_dir, x)), reverse=True)
                        # 排除reflection任务的历史文件
                        for f in files_sorted:
                            candidate = os.path.join(model_responses_dir, f)
                            try:
                                with open(candidate, 'r', encoding='utf-8') as check_f:
                                    content = check_f.read()
                                    if '# 自动触发的Reflection任务' not in content:
                                        history_file = candidate
                                        break
                            except:
                                continue
            
            if os.path.exists(history_file):
                import re
                content = open(history_file, 'r', encoding='utf-8').read()
                
                # 查找最后一个TASK_START标记
                task_start_pattern = r'=== TASK_START ==='
                matches = list(re.finditer(task_start_pattern, content))
                
                if matches:
                    # 从最后一个TASK_START提取到文件末尾（当前任务的完整对话）
                    last_task_start = matches[-1].start()
                    recent_history = content[last_task_start:]
                    
                    # 检查是否包含reflection标记（避免嵌套）
                    if '# 自动触发的Reflection任务' in recent_history:
                        return False  # 直接返回，避免启动subagent
                else:
                    # 没有TASK_START标记，使用旧逻辑（向后兼容）
                    prompt_pattern = r'=== Prompt === (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
                    prompts = list(re.finditer(prompt_pattern, content))
                    
                    if prompts:
                        # 取最近10轮
                        start_idx = max(0, len(prompts) - 10)
                        start_pos = prompts[start_idx].start()
                        recent_history = content[start_pos:]
                    else:
                        recent_history = content
            else:
                recent_history = "历史文件不存在"
        
        # 创建reflection任务
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_name = f"reflection_{timestamp}"
        task_dir = os.path.join(temp_dir, task_name)
        os.makedirs(task_dir, exist_ok=True)
        
        # 截断长输出
        import re
        def truncate_outputs(text):
            pattern = r'("content":\s*")((?:[^"\\]|\\.)*)(")'
            def replacer(m):
                content = m.group(2)
                if len(content) > 1000:
                    return f'{m.group(1)}{content[:1000]}...[截断]{m.group(3)}'
                return m.group(0)
            return re.sub(pattern, replacer, text)
        
        recent_history = truncate_outputs(recent_history)
        
        # 写入input.txt
        with open(os.path.join(task_dir, "input.txt"), 'w', encoding='utf-8') as f:
            f.write(f"""# 自动触发的Reflection任务

## 检测到错误
系统自动检测到工具调用失败或错误信息。

## 对话历史
{recent_history}

## 任务
1. 分析错误根本原因，区分：工具本身缺陷/环境配置问题/使用方式错误
2. 提出2-3个假设并验证
3. 更新抽象规律必须用: `from memory.reflection.reflection_helper import update_meta_pattern; update_meta_pattern(rule, trigger, action)`
4. 在output.txt末尾写摘要
""")
        
        # Spawn subagent
        venv_python = os.path.join(script_dir, '.venv', 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(script_dir, '.venv', 'bin', 'python')
        cmd = [venv_python, os.path.join(script_dir, 'agentmain.py'), "--task", task_name, "--bg"]
        
        kwargs = {'cwd': script_dir, 'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL}
        if os.name == 'nt': kwargs['creationflags'] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        else: kwargs['start_new_session'] = True
        
        subprocess.Popen(cmd, **kwargs)
        print(f"[INFO] Reflection agent auto-spawned: {task_name}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to spawn reflection agent: {e}")
        return False



def get_meta_patterns() -> str:
    """提取抽象规律表，用于注入working memory（~500 tokens）"""
    path = os.path.join(os.path.dirname(__file__), 'self_improvement.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'## 0\. 抽象规律.*?\n(\|.*?\|)\n\n', content, re.DOTALL)
    return match.group(1) if match else ""

def update_meta_pattern(rule: str, trigger: str, action: str) -> str:
    """安全更新抽象规律，自动去重+限制数量
    
    Returns: 成功信息或拒绝原因
    """
    path = os.path.join(os.path.dirname(__file__), 'self_improvement.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取现有规律（仅从抽象规律表格）
    section_match = re.search(r'## 0\. 抽象规律.*?\n(.*?)\n\n## 1\.', content, re.DOTALL)
    if not section_match:
        return "[错误] 未找到抽象规律表格"
    section = section_match.group(1)
    pattern = r'\| ([^|]+) \| ([^|]+) \| ([^|]+) \|'
    matches = re.findall(pattern, section)
    existing = [m[0].strip() for m in matches if m[0].strip() not in [':---', '规律']]
    
    # 检查相似性（关键词重叠>50%视为相似）
    rule_words = set(rule.lower().split())
    for e in existing:
        e_words = set(e.lower().split())
        overlap = len(rule_words & e_words) / max(len(rule_words), 1)
        if overlap > 0.5:
            return f"[跳过] 已有类似规律: {e}"
    
    # 检查数量上限
    if len(existing) >= MAX_META_PATTERNS:
        return f"[拒绝] 已达上限{MAX_META_PATTERNS}条，需先合并或删除旧规律"
    
    # 插入新规律（在表格末尾）
    new_row = f"| {rule} | {trigger} | {action} |"
    # 找到抽象规律表格的最后一行
    table_end = content.find('\n\n## 1.')
    if table_end == -1:
        return "[错误] 未找到插入位置"
    
    content = content[:table_end] + '\n' + new_row + content[table_end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return f"[成功] 新增规律: {rule} (当前{len(existing)+1}/{MAX_META_PATTERNS}条)"
