"""
auto_commit.py — GenericAgent 关键产出一键快照工具
用法: python auto_commit.py [message]
      不提供message时自动生成时间戳commit信息
"""
import subprocess, sys, os
from datetime import datetime

AGENT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 需要强制追踪的文件（在.gitignore目录下）
FORCE_ADD = [
    "temp/ppt_com_toolkit.py",
    "temp/word_toolkit.py",
    "temp/word_toolkit.py",
]

# 正常追踪的路径
NORMAL_ADD = [
    "gnn_papers/",
    "local_skills/",
    "memory/",
]


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=AGENT_ROOT, **kw)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def auto_commit(message=None):
    if not message:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        message = f"snapshot: agent key outputs @ {ts}"

    print(f"[auto_commit] message: {message}")

    # 强制add（绕过.gitignore）
    for f in FORCE_ADD:
        p = os.path.join(AGENT_ROOT, f)
        if os.path.exists(p):
            code, out, err = run(["git", "add", "-f", f])
            print(f"  force-add {f}: {"OK" if code==0 else err}")

    # 正常add
    for f in NORMAL_ADD:
        p = os.path.join(AGENT_ROOT, f)
        if os.path.exists(p):
            code, out, err = run(["git", "add", f])
            print(f"  add {f}: {"OK" if code==0 else err}")

    # 检查是否有变更
    code, out, err = run(["git", "diff", "--cached", "--quiet"])
    if code == 0:
        print("[auto_commit] 无变更，跳过commit")
        return

    # commit
    code, out, err = run(["git", "commit", "-m", message])
    if code == 0:
        print(f"[auto_commit] 成功: {out.splitlines()[0] if out else OK}")
    else:
        print(f"[auto_commit] 失败: {err}")

    # 显示最新log
    _, log, _ = run(["git", "log", "--oneline", "-3"])
    print(f"[auto_commit] 最新3条:\n{log}")


if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    auto_commit(msg)
