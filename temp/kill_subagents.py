#!/usr/bin/env python3
"""
Kill all subagent processes (agentmain.py with --task/--reflect/reflection flags)
自动排除当前进程，安全清理所有subagent
"""
import subprocess
import psutil
import os

def kill_subagents():
    """Kill all subagent processes except current process"""
    current_pid = os.getpid()
    pids = []
    
    # 使用psutil获取所有python进程（普通权限可用）
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            # 匹配agentmain.py进程
            if 'python' in proc.info['name'].lower() and 'agentmain.py' in cmdline:
                # 排除当前进程
                if proc.info['pid'] != current_pid:
                    pids.append(str(proc.info['pid']))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if pids:
        # 正确构造taskkill命令：每个参数独立
        cmd = ['taskkill', '/F']
        for pid in pids:
            cmd.extend(['/PID', pid])
        
        print(f"正在终止 {len(pids)} 个subagent进程...")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='gbk')
        print(result.stdout)
        
        # 验证结果
        remaining = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if 'python' in proc.info['name'].lower() and 'agentmain.py' in cmdline:
                    if proc.info['pid'] != current_pid:
                        remaining.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if remaining:
            print(f"⚠️ 还有 {len(remaining)} 个进程未清理: {remaining}")
        else:
            print(f"✅ 所有 {len(pids)} 个subagent进程已清理完毕")
    else:
        print("✅ 没有找到subagent进程")

if __name__ == '__main__':
    kill_subagents()
