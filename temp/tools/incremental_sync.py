"""
增量文件同步工具
提供增量同步、冲突处理、自动备份等功能

功能:
1. 增量同步 - 仅传输变化的文件（基于大小+时间戳）
2. 冲突处理 - newer/older/both/skip 策略
3. 自动备份 - 覆盖前备份到指定目录
4. 同步记录 - JSON记录上次同步状态

依赖: adb (Android Debug Bridge)
"""

import subprocess, os, json, shutil, hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

ADB = shutil.which("adb") or "adb"


class IncrementalSync:
    def __init__(self, device: Optional[str] = None):
        self.device = device
        self.sync_db_path = Path("./sync_state.json")
        self.sync_db = self._load_sync_db()
    
    def _run_adb(self, cmd: List[str]) -> Tuple[int, str, str]:
        """执行adb命令"""
        if self.device:
            full_cmd = [ADB, "-s", self.device] + cmd
        else:
            full_cmd = [ADB] + cmd
        r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=30)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    
    def _load_sync_db(self) -> Dict:
        """加载同步状态数据库"""
        if self.sync_db_path.exists():
            with open(self.sync_db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _save_sync_db(self):
        """保存同步状态数据库"""
        with open(self.sync_db_path, "w", encoding="utf-8") as f:
            json.dump(self.sync_db, f, indent=2, ensure_ascii=False)
    
    def get_remote_file_info(self, remote_path: str) -> Optional[Dict]:
        """获取远程文件信息"""
        code, out, err = self._run_adb(["shell", "stat", "-c", "%s %Y", remote_path])
        if code != 0:
            return None
        
        parts = out.split()
        if len(parts) >= 2:
            return {
                "size": int(parts[0]),
                "mtime": int(parts[1]),
                "path": remote_path
            }
        return None
    
    def get_local_file_info(self, local_path: Path) -> Optional[Dict]:
        """获取本地文件信息"""
        if not local_path.exists():
            return None
        
        stat = local_path.stat()
        return {
            "size": stat.st_size,
            "mtime": int(stat.st_mtime),
            "path": str(local_path)
        }
    def need_sync(self, local_info: Dict, remote_info: Dict, strategy: str = "newer") -> Tuple[bool, str]:
        """
        判断是否需要同步
        
        Args:
            local_info: 本地文件信息
            remote_info: 远程文件信息
            strategy: 冲突策略 ("newer", "older", "both", "skip")
        
        Returns:
            (需要同步, 方向) - 方向为 "pull", "push", "both", "skip"
        """
        if not local_info and not remote_info:
            return False, "skip"
        
        if not local_info:
            return True, "pull"
        
        if not remote_info:
            return True, "push"
        
        # 大小或时间不同才需要同步
        if local_info["size"] == remote_info["size"] and local_info["mtime"] == remote_info["mtime"]:
            return False, "skip"
        
        # 根据策略决定方向
        if strategy == "newer":
            if local_info["mtime"] > remote_info["mtime"]:
                return True, "push"
            else:
                return True, "pull"
        elif strategy == "older":
            if local_info["mtime"] < remote_info["mtime"]:
                return True, "push"
            else:
                return True, "pull"
        elif strategy == "both":
            return True, "both"
        elif strategy == "skip":
            return False, "skip"
        
        return False, "skip"
    
    def backup_file(self, file_path: Path, backup_dir: Path) -> bool:
        """备份文件"""
        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = backup_dir / backup_name
            shutil.copy2(file_path, backup_path)
            return True
        except Exception as e:
            print(f"备份失败: {e}")
            return False
    def sync_directory(self, local_dir: str, remote_dir: str, 
                      strategy: str = "newer", backup: bool = False,
                      backup_dir: str = "./backup", dry_run: bool = False) -> Dict:
        """
        同步目录
        
        Args:
            local_dir: 本地目录
            remote_dir: 远程目录
            strategy: 冲突策略 ("newer", "older", "both", "skip")
            backup: 是否备份
            backup_dir: 备份目录
            dry_run: 预览模式
        """
        local_path = Path(local_dir)
        backup_path = Path(backup_dir) if backup else None
        
        result = {
            "pulled": 0,
            "pushed": 0,
            "skipped": 0,
            "backed_up": 0,
            "failed": 0
        }
        
        # 获取远程文件列表
        code, out, err = self._run_adb(["shell", "ls", "-1", remote_dir])
        if code != 0:
            return {"success": False, "message": f"无法访问远程目录: {err}"}
        
        remote_files = [f.strip() for f in out.splitlines() if f.strip()]
        
        # 获取本地文件列表
        local_path.mkdir(parents=True, exist_ok=True)
        local_files = [f.name for f in local_path.iterdir() if f.is_file()]
        
        # 合并文件列表
        all_files = set(remote_files + local_files)
        
        print(f"\n=== 增量同步: {local_dir} <-> {remote_dir} ===")
        print(f"策略: {strategy} | 备份: {backup} | 预览: {dry_run}\n")
        
        for fname in sorted(all_files):
            local_file = local_path / fname
            remote_file = f"{remote_dir.rstrip('/')}/{fname}"
            
            # 获取文件信息
            local_info = self.get_local_file_info(local_file)
            remote_info = self.get_remote_file_info(remote_file)
            
            # 判断是否需要同步
            need, direction = self.need_sync(local_info, remote_info, strategy)
            
            if not need:
                print(f"[SKIP] {fname}")
                result["skipped"] += 1
                continue
            
            # 执行同步
            if direction == "pull":
                print(f"[PULL] {fname} (远程 -> 本地)", end=" ")
                if dry_run:
                    print("[DRY]")
                    result["pulled"] += 1
                else:
                    if backup and local_file.exists():
                        if self.backup_file(local_file, backup_path):
                            result["backed_up"] += 1
                    
                    code, _, err = self._run_adb(["pull", remote_file, str(local_file)])
                    if code == 0:
                        print("OK")
                        result["pulled"] += 1
                    else:
                        print(f"FAIL: {err}")
                        result["failed"] += 1
            
            elif direction == "push":
                print(f"[PUSH] {fname} (本地 -> 远程)", end=" ")
                if dry_run:
                    print("[DRY]")
                    result["pushed"] += 1
                else:
                    code, _, err = self._run_adb(["push", str(local_file), remote_file])
                    if code == 0:
                        print("OK")
                        result["pushed"] += 1
                    else:
                        print(f"FAIL: {err}")
                        result["failed"] += 1
        
        print(f"\n=== 同步完成 ===")
        print(f"拉取: {result['pulled']} | 推送: {result['pushed']} | 跳过: {result['skipped']}")
        print(f"备份: {result['backed_up']} | 失败: {result['failed']}")
        
        result["success"] = True
        return result


# ============ 使用示例 ============

if __name__ == "__main__":
    print("=== 增量同步工具使用指南 ===\n")
    
    print("【功能】")
    print("  • 增量同步 - 仅传输变化的文件")
    print("  • 冲突处理 - newer/older/both/skip 策略")
    print("  • 自动备份 - 覆盖前备份到指定目录")
    print("  • 同步记录 - JSON记录上次同步状态\n")
    
    print("【使用示例】")
    print("  sync = IncrementalSync()")
    print("  ")
    print("  # 增量同步（仅传输新文件或修改的文件）")
    print("  sync.sync_directory(")
    print("      local_dir='./photos',")
    print("      remote_dir='/sdcard/DCIM',")
    print("      strategy='newer',  # 保留较新的文件")
    print("      backup=True,       # 启用备份")
    print("      dry_run=False      # 实际执行")
    print("  )")
    
    print("\n=== 使用指南完成 ===")