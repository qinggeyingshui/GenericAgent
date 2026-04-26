"""
cleanup_executor.py — 临时文件清理执行器
基于 disk_analyzer.py 的 is_temp_file 识别逻辑
安全策略：仅删除 .pyc/.pyo 及 __pycache__ 目录内文件（无需回收站，可重新生成）
日志输出：cleanup_log_YYYYMMDD_HHMMSS.txt
"""
import os, sys, time
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ── 安全删除范围（仅编译缓存，可重新生成，无需备份）──
SAFE_EXTS = {'.pyc', '.pyo'}
SAFE_DIRS = {'__pycache__', '.pytest_cache', '.mypy_cache', '.tox'}

SCAN_ROOT = r'E:\2026\x-fudan\new\GenericAgent\temp'
LOG_PATH = os.path.join(SCAN_ROOT, f'cleanup_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

def fmt_size(b):
    for u in ['B','KB','MB','GB']:
        if abs(b) < 1024: return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} TB"

def collect_safe_targets(root):
    targets = []
    for dirpath, dirnames, filenames in os.walk(root):
        parts = set(Path(dirpath).parts)
        in_safe_dir = bool(parts & SAFE_DIRS)
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            ext = os.path.splitext(fname)[1].lower()
            if ext in SAFE_EXTS or in_safe_dir:
                try:
                    fsize = os.path.getsize(fpath)
                    targets.append((fpath, fsize))
                except OSError:
                    pass
    return targets

def delete_targets(targets, log_lines):
    deleted = []
    failed = []
    for fpath, fsize in targets:
        try:
            os.remove(fpath)
            deleted.append((fpath, fsize))
            log_lines.append(f"DELETED  {fmt_size(fsize):>10}  {fpath}")
        except Exception as e:
            failed.append((fpath, str(e)))
            log_lines.append(f"FAILED   {fpath}  -- {e}")
    return deleted, failed

def remove_empty_pycache(root, log_lines):
    removed_dirs = 0
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if os.path.basename(dirpath) in SAFE_DIRS:
            try:
                os.rmdir(dirpath)
                removed_dirs += 1
                log_lines.append(f"RMDIR    {dirpath}")
            except OSError:
                pass
    return removed_dirs

def main():
    print(f"扫描目录: {SCAN_ROOT}")
    print("收集安全删除候选（.pyc/.pyo/__pycache__）...")
    targets = collect_safe_targets(SCAN_ROOT)
    total_size = sum(s for _, s in targets)
    print(f"找到 {len(targets)} 个文件，共 {fmt_size(total_size)}")

    if len(targets) == 0:
        print("无候选文件，退出。")
        return

    log_lines = [
        f"cleanup_executor.py 运行日志",
        f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"扫描目录: {SCAN_ROOT}",
        f"候选文件: {len(targets)} 个, {fmt_size(total_size)}",
        "=" * 60,
    ]

    print(f"\n开始删除...")
    deleted, failed = delete_targets(targets, log_lines)
    removed_dirs = remove_empty_pycache(SCAN_ROOT, log_lines)

    deleted_size = sum(s for _, s in deleted)
    log_lines += [
        "=" * 60,
        f"已删除: {len(deleted)} 个文件, {fmt_size(deleted_size)}",
        f"删除空目录: {removed_dirs} 个",
        f"失败: {len(failed)} 个",
    ]

    # 写日志
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))

    print(f"\n✅ 完成！")
    print(f"   删除文件: {len(deleted)} 个 ({fmt_size(deleted_size)})")
    print(f"   删除空目录: {removed_dirs} 个")
    print(f"   失败: {len(failed)} 个")
    print(f"   日志: {LOG_PATH}")

    # 按扩展名统计
    ext_stat = defaultdict(lambda: [0, 0])
    for fpath, fsize in deleted:
        ext = os.path.splitext(fpath)[1].lower() or '(无)'
        ext_stat[ext][0] += 1
        ext_stat[ext][1] += fsize
    print("\n按扩展名:")
    for ext, (cnt, sz) in sorted(ext_stat.items(), key=lambda x: -x[1][1]):
        print(f"  {ext:12s} {cnt:4d} 个  {fmt_size(sz)}")

    return len(deleted), deleted_size, LOG_PATH

if __name__ == '__main__':
    main()