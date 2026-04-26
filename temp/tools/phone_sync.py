#!/usr/bin/env python3
"""
phone_sync.py — PC↔手机文件批量同步CLI工具
基于adb命令封装，支持list/pull/push三种操作

用法:
  python phone_sync.py list <phone_dir>              # 列出手机目录文件
  python phone_sync.py pull <phone_dir> <local_dir>  # 手机→本地
  python phone_sync.py push <local_dir> <phone_dir>  # 本地→手机

选项:
  --ext jpg,png,mp4    # 仅同步指定扩展名（逗号分隔）
  --dry                # 预览模式，不实际传输
  --device SERIAL      # 指定设备序列号（多设备时使用）
"""
import subprocess, argparse, os, sys, shutil
from pathlib import Path

ADB = shutil.which("adb") or "adb"


def _run(cmd, device=None):
    """执行adb命令，返回(code, stdout, stderr)"""
    if device:
        full_cmd = [ADB, "-s", device] + cmd
    else:
        full_cmd = [ADB] + cmd
    r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=30)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def check_adb(device=None):
    """检查adb可用性和设备连接"""
    code, out, err = _run(["devices"], device=None)
    if code != 0:
        print(f"[ERROR] adb不可用: {err}")
        return False
    lines = [l for l in out.splitlines() if "\t" in l and "offline" not in l]
    if not lines:
        print("[ERROR] 未检测到已连接的Android设备")
        print("请确认: 1)手机已连接USB 2)已开启USB调试 3)已授权本机")
        return False
    print(f"[adb] 已连接设备: {len(lines)}个")
    for l in lines:
        print(f"  {l}")
    return True


def cmd_list(phone_dir, ext_filter=None, device=None):
    """列出手机目录文件"""
    print(f"[list] 手机目录: {phone_dir}")
    code, out, err = _run(["shell", "ls", "-la", phone_dir], device=device)
    if code != 0:
        print(f"[ERROR] {err or out}")
        return []
    files = []
    for line in out.splitlines():
        parts = line.split()
        if not parts:
            continue
        name = parts[-1]
        if name in (".", ".."): continue
        if ext_filter:
            exts = [e.lower().lstrip(".") for e in ext_filter.split(",")]
            if not any(name.lower().endswith("." + e) for e in exts):
                continue
        files.append(name)
        print(f"  {line}")
    print(f"共 {len(files)} 个文件")
    return files


def cmd_pull(phone_dir, local_dir, ext_filter=None, dry=False, device=None):
    """从手机pull文件到本地"""
    local_path = Path(local_dir)
    local_path.mkdir(parents=True, exist_ok=True)

    # 先列出文件
    files = cmd_list(phone_dir, ext_filter=ext_filter, device=device)
    if not files:
        print("[pull] 无可同步文件")
        return 0

    ok, fail = 0, 0
    for fname in files:
        src = phone_dir.rstrip("/") + "/" + fname
        dst = str(local_path / fname)
        print(f"  pull {src} -> {dst}", end=" ")
        if dry:
            print("[DRY]")
            ok += 1
            continue
        code, out, err = _run(["pull", src, dst], device=device)
        if code == 0:
            print("OK")
            ok += 1
        else:
            print(f"FAIL: {err}")
            fail += 1
    print(f"[pull] 完成: {ok}成功 {fail}失败")
    return ok


def cmd_push(local_dir, phone_dir, ext_filter=None, dry=False, device=None):
    """从本地push文件到手机"""
    local_path = Path(local_dir)
    if not local_path.exists():
        print(f"[ERROR] 本地目录不存在: {local_dir}")
        return 0

    # 收集本地文件
    if ext_filter:
        exts = tuple("." + e.lower().lstrip(".") for e in ext_filter.split(","))
        files = [f for f in local_path.iterdir() if f.is_file() and f.suffix.lower() in exts]
    else:
        files = [f for f in local_path.iterdir() if f.is_file()]

    print(f"[push] 本地: {local_dir} -> 手机: {phone_dir} ({len(files)}个文件)")

    ok, fail = 0, 0
    for f in files:
        dst = phone_dir.rstrip("/") + "/" + f.name
        print(f"  push {f} -> {dst}", end=" ")
        if dry:
            print("[DRY]")
            ok += 1
            continue
        code, out, err = _run(["push", str(f), dst], device=device)
        if code == 0:
            print("OK")
            ok += 1
        else:
            print(f"FAIL: {err}")
            fail += 1
    print(f"[push] 完成: {ok}成功 {fail}失败")
    return ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PC↔手机文件同步工具")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="列出手机目录文件")
    p_list.add_argument("phone_dir")
    p_list.add_argument("--ext", default=None)
    p_list.add_argument("--device", default=None)

    p_pull = sub.add_parser("pull", help="手机→本地")
    p_pull.add_argument("phone_dir")
    p_pull.add_argument("local_dir")
    p_pull.add_argument("--ext", default=None)
    p_pull.add_argument("--dry", action="store_true")
    p_pull.add_argument("--device", default=None)

    p_push = sub.add_parser("push", help="本地→手机")
    p_push.add_argument("local_dir")
    p_push.add_argument("phone_dir")
    p_push.add_argument("--ext", default=None)
    p_push.add_argument("--dry", action="store_true")
    p_push.add_argument("--device", default=None)

    args = parser.parse_args()

    if not check_adb():
        sys.exit(1)

    if args.cmd == "list":
        cmd_list(args.phone_dir, ext_filter=args.ext, device=args.device)
    elif args.cmd == "pull":
        cmd_pull(args.phone_dir, args.local_dir, ext_filter=args.ext,
                 dry=args.dry, device=args.device)
    elif args.cmd == "push":
        cmd_push(args.local_dir, args.phone_dir, ext_filter=args.ext,
                 dry=args.dry, device=args.device)
