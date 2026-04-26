"""
环境管家 - 磁盘清理工具
基于disk_scan_report.json实现安全清理
特性：
1. 仅清理cache类别且冗余评分>=8的文件
2. dry-run模式预览
3. 清理前生成备份清单
4. 清理后生成cleanup_report.json
"""
import json
import os
from datetime import datetime
from pathlib import Path

def load_cleanable_files():
    """加载可清理文件列表"""
    with open("cleanable_files.json", "r", encoding="utf-8") as f:
        return json.load(f)

def preview_cleanup():
    """预览清理操作（dry-run模式）"""
    data = load_cleanable_files()
    print("=== 清理预览 (DRY-RUN) ===")
    print(f"扫描时间: {data['scan_time']}")
    print(f"可清理文件数: {data['total_cleanable_files']}")
    print(f"可释放空间: {data['total_cleanable_size_mb']:.0f} MB")
    print("\n将要删除的文件:")
    for i, f in enumerate(data['files'], 1):
        print(f"{i}. [{f['redundancy_score']}分] {f['size_mb']:.0f}MB")
        print(f"   {f['path']}")
    return data

def create_backup_list(data):
    """生成备份清单"""
    backup = {
        "backup_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_files": data["total_cleanable_files"],
        "total_size_mb": data["total_cleanable_size_mb"],
        "files": [
            {
                "path": f["path"],
                "size_mb": f["size_mb"],
                "category": f["category"],
                "redundancy_score": f["redundancy_score"]
            }
            for f in data["files"]
        ]
    }
    with open("cleanup_backup_list.json", "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=2)
    print("✓ 备份清单已生成: cleanup_backup_list.json")
    return backup

def perform_cleanup(dry_run=True):
    """执行清理操作"""
    data = load_cleanable_files()
    
    if dry_run:
        print("\n=== DRY-RUN 模式 ===")
        print("仅预览，不会实际删除文件")
        preview_cleanup()
        return None
    
    # 创建备份清单
    backup = create_backup_list(data)
    
    # 执行清理
    print("\n=== 开始清理 ===")
    cleaned_files = []
    failed_files = []
    total_freed_mb = 0
    
    for i, f in enumerate(data["files"], 1):
        path = Path(f["path"])
        try:
            if path.exists():
                size_mb = f["size_mb"]
                os.remove(path)
                cleaned_files.append(f)
                total_freed_mb += size_mb
                print(f"✓ [{i}/{len(data['files'])}] 已删除: {size_mb:.0f}MB - {path.name}")
            else:
                print(f"⚠ [{i}/{len(data['files'])}] 文件不存在: {path.name}")
                failed_files.append({"path": str(path), "reason": "文件不存在"})
        except Exception as e:
            print(f"✗ [{i}/{len(data['files'])}] 删除失败: {path.name} - {e}")
            failed_files.append({"path": str(path), "reason": str(e)})
    
    # 生成清理报告
    report = {
        "cleanup_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total_files": len(data["files"]),
            "cleaned_files": len(cleaned_files),
            "failed_files": len(failed_files),
            "total_freed_mb": total_freed_mb,
            "total_freed_gb": total_freed_mb / 1024
        },
        "before": {
            "scan_time": data["scan_time"],
            "total_cleanable_files": data["total_cleanable_files"],
            "total_cleanable_size_mb": data["total_cleanable_size_mb"]
        },
        "after": {
            "cleaned_files": cleaned_files,
            "failed_files": failed_files
        }
    }
    
    with open("cleanup_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== 清理完成 ===")
    print(f"✓ 已清理: {len(cleaned_files)}/{len(data['files'])} 个文件")
    print(f"✓ 释放空间: {total_freed_mb:.0f} MB ({total_freed_mb/1024:.2f} GB)")
    if failed_files:
        print(f"⚠ 失败: {len(failed_files)} 个文件")
    print(f"✓ 清理报告已生成: cleanup_report.json")
    
    return report

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        print("⚠ 警告: 即将执行实际清理操作！")
        confirm = input("确认删除文件？(yes/no): ")
        if confirm.lower() == "yes":
            perform_cleanup(dry_run=False)
        else:
            print("已取消清理操作")
    else:
        print("默认运行 DRY-RUN 模式")
        print("如需实际清理，请运行: python disk_cleaner.py --execute")
        print()
        perform_cleanup(dry_run=True)
