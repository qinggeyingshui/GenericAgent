import sys, os, json, re, time, subprocess
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'memory'))
_r = subprocess.run
def _d(b):
    if not b: return ''
    if isinstance(b, str): return b
    try: return b.decode()
    except: return b.decode('gbk', 'replace')
def _run(*a, **k):
    t = k.pop('text', 0) | k.pop('universal_newlines', 0)
    enc = k.pop('encoding', None)
    k.pop('errors', None)
    if enc: t = 1
    if t and isinstance(k.get('input'), str):
        k['input'] = k['input'].encode()
    r = _r(*a, **k)
    if t:
        if r.stdout is not None: r.stdout = _d(r.stdout)
        if r.stderr is not None: r.stderr = _d(r.stderr)
    return r
subprocess.run = _run
sys.excepthook = lambda t, v, tb: (sys.__excepthook__(t, v, tb), print(f"\n[Agent Hint]: NO GUESSING! You MUST probe first. If missing common package, pip.")) if issubclass(t, (ImportError, AttributeError)) else sys.__excepthook__(t, v, tb)

import psutil
import os

current_pid = os.getpid()
print(f"当前进程PID: {current_pid}")

killed = []
for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
    try:
        if proc.info['pid'] == current_pid:
            continue
        cmdline = proc.info['cmdline']
        if cmdline and 'python' in str(cmdline).lower():
            cmdline_str = ' '.join(cmdline) if cmdline else ''
            # 查找所有包含agentmain.py或GenericAgent路径的python进程
            if 'agentmain.py' in cmdline_str or 'GenericAgent' in cmdline_str:
                print(f"发现进程: PID={proc.info['pid']}, CMD={cmdline_str[:100]}")
                proc.kill()
                killed.append(proc.info['pid'])
    except:
        pass

print(f"\n已终止 {len(killed)} 个进程: {killed}")
