"""
环境管家 - 磁盘大文件扫描工具
用法: python disk_manager.py [scan|analyze|report]
"""
import os
import json
from pathlib import Path
from datetime import datetime
import sys

MIN_SIZE_MB = 100

# 用户画像
USER_PROFILE = {
    "research": ["VQA", "Graph ML", "GNN", "Topology Pretraining"],
    "projects": ["GenericAgent", "VQA", "topo_pretrain_base", "KDD", "SITP"],
    "tools": ["Python", "MATLAB", "Node", "Docker", "VMware"]
}

# 扫描目标（分批扫描避免超时）
SCAN_BATCHES = [
    {
        "name": "用户下载和临时文件",
        "paths": [
            "C:\\Users\\qgys\\Downloads",
            "C:\\Users\\qgys\\AppData\\Local\\Temp",
            "C:\\Users\\qgys\\Desktop"
        ]
    },
    {
        "name": "用户AppData",
        "paths": ["C:\\Users\\qgys\\AppData\\Local"],
        "max_depth": 3  # 限制递归深度
    },
    {
        "name": "Anaconda环境",
        "paths": ["E:\\Anaconda_envs"],
        "max_depth": 4
    },
    {
        "name": "工作项目",
        "paths": ["E:\\2026"],
        "max_depth": 5
    },
    {
        "name": "开发工具",
        "paths": ["D:\\anaconda3", "D:\\vmware", "D:\\MySQL"],
        "max_depth": 3
    }
]

def get_category(file_path, ext):
    """文件分类"""
    p = str(file_path).lower()
    e = ext.lower() if ext else ''
    
    if any(k in p for k in ['cache', 'temp', 'tmp']):
        return 'cache'
    if any(k in p for k in ['anaconda', 'conda', 'node_modules', '.venv', 'site-packages']):
        return 'dev_tool'
    if e in ['.vmdk', '.vdi', '.vhd', '.iso'] or 'vmware' in p:
        return 'vm_image'
    if any(k in p for k in ['dataset', 'data\\']) or e in ['.csv', '.json', '.h5', '.pkl']:
        return 'dataset'
    if e in ['.pth', '.pt', '.ckpt', '.onnx'] or 'model' in p:
        return 'model'
    if e in ['.pdf', '.docx', '.pptx', '.xlsx']:
        return 'document'
    if e in ['.mp4', '.avi', '.mkv', '.mp3', '.wav']:
        return 'media'
    if e in ['.zip', '.rar', '.7z', '.tar', '.gz']:
        return 'archive'
    return 'other'

def assess_redundancy(file_path, category, size_mb):
    """评估冗余性"""
    p = str(file_path).lower()
    
    if category == 'cache':
        return 9, "临时缓存，可安全删除"
    if category == 'dev_tool':
        if 'node_modules' in p:
            return 6, "Node依赖，可npm install恢复"
        return 3, "开发工具依赖"
    if category == 'vm_image':
        return 8 if size_mb > 5000 else 5, "虚拟机镜像"
    if category == 'dataset':
        if any(k in p for k in ['gnn', 'graph', 'vqa', 'topology']):
            return 2, "研究数据集，建议保留"
        return 6, "非研究数据集"
    if category == 'model':
        if any(k in p for k in ['genericagent', 'vqa', 'kdd']):
            return 2, "项目模型，建议保留"
        return 5, "旧模型文件"
    if category == 'document':
        return 1, "文档，建议保留"
    if category == 'media':
        return 7 if 'download' in p else 3, "媒体文件"
    if category == 'archive':
        return 8 if 'download' in p else 4, "压缩包"
    return 5, "未分类文件"

def scan_batch(batch, output_file):
    """扫描一个批次"""
    print(f"\n=== 扫描: {batch['name']} ===")
    files = []
    
    for path_str in batch['paths']:
        if not os.path.exists(path_str):
            print(f"  跳过不存在: {path_str}")
            continue
        
        print(f"  扫描 {path_str} ...")
        max_depth = batch.get('max_depth', 999)
        
        try:
            for root, dirs, filenames in os.walk(path_str):
                # 控制递归深度
                depth = root[len(path_str):].count(os.sep)
                if depth >= max_depth:
                    dirs.clear()
                
                for filename in filenames:
                    try:
                        file_path = Path(root) / filename
                        size_bytes = file_path.stat().st_size
                        size_mb = size_bytes / (1024 * 1024)
                        
                        if size_mb >= MIN_SIZE_MB:
                            files.append({
                                'path': str(file_path),
                                'size_mb': round(size_mb, 2),
                                'size_gb': round(size_mb / 1024, 2),
                                'extension': file_path.suffix
                            })
                    except (PermissionError, OSError):
                        continue
        except Exception as e:
            print(f"  错误: {e}")
    
    print(f"  找到 {len(files)} 个大文件")
    
    # 追加到输出文件
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    else:
        existing = []
    
    existing.extend(files)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    
    return len(files)

def analyze_files(input_file, output_file):
    """分析文件并生成报告"""
    print("\n=== 分析文件 ===")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_files = json.load(f)
    
    analyzed = []
    stats = {
        'total_count': len(raw_files),
        'total_size_gb': 0,
        'by_category': {},
        'high_redundancy': []
    }
    
    for file_info in raw_files:
        path = file_info['path']
        size_mb = file_info['size_mb']
        size_gb = file_info['size_gb']
        ext = file_info['extension']
        
        category = get_category(path, ext)
        redundancy, suggestion = assess_redundancy(path, category, size_mb)
        
        analyzed_file = {
            **file_info,
            'category': category,
            'redundancy_score': redundancy,
            'suggestion': suggestion
        }
        
        analyzed.append(analyzed_file)
        stats['total_size_gb'] += size_gb
        
        if category not in stats['by_category']:
            stats['by_category'][category] = {'count': 0, 'size_gb': 0}
        stats['by_category'][category]['count'] += 1
        stats['by_category'][category]['size_gb'] += size_gb
        
        if redundancy >= 7:
            stats['high_redundancy'].append(analyzed_file)
    
    report = {
        'scan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'statistics': stats,
        'files': analyzed,
        'user_profile': USER_PROFILE
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] 分析完成")
    print(f"  文件总数: {stats['total_count']}")
    print(f"  总大小: {stats['total_size_gb']:.2f} GB")
    print(f"  高冗余文件: {len(stats['high_redundancy'])} 个")
    print(f"\n[OK] 报告已保存: {output_file}")

def print_report(report_file):
    """打印报告摘要"""
    with open(report_file, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    stats = report['statistics']
    
    print("\n=== 磁盘扫描报告 ===")
    print(f"扫描时间: {report['scan_time']}")
    print(f"文件总数: {stats['total_count']}")
    print(f"总大小: {stats['total_size_gb']:.2f} GB")
    
    print("\n按类别统计:")
    for cat, data in sorted(stats['by_category'].items(), key=lambda x: x[1]['size_gb'], reverse=True):
        print(f"  {cat:12s}: {data['count']:3d} 个, {data['size_gb']:6.2f} GB")
    
    print(f"\n高冗余文件 (>=7分): {len(stats['high_redundancy'])} 个")
    if stats['high_redundancy']:
        print("\nTOP 10 高冗余文件:")
        for i, f in enumerate(sorted(stats['high_redundancy'], key=lambda x: x['size_gb'], reverse=True)[:10], 1):
            print(f"  {i:2d}. [{f['redundancy_score']}分] {f['size_gb']:.2f}GB - {f['suggestion']}")
            print(f"      {f['path']}")

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'scan'
    
    raw_file = 'disk_scan_raw.json'
    report_file = 'disk_scan_report.json'
    
    if cmd == 'scan':
        print("开始分批扫描...")
        total = 0
        for batch in SCAN_BATCHES:
            count = scan_batch(batch, raw_file)
            total += count
        print(f"\n[OK] 扫描完成，共 {total} 个大文件")
        print(f"\n下一步: python disk_manager.py analyze")
    
    elif cmd == 'analyze':
        if not os.path.exists(raw_file):
            print(f"错误: 未找到 {raw_file}，请先运行 scan")
            sys.exit(1)
        analyze_files(raw_file, report_file)
        print(f"\n下一步: python disk_manager.py report")
    
    elif cmd == 'report':
        if not os.path.exists(report_file):
            print(f"错误: 未找到 {report_file}，请先运行 analyze")
            sys.exit(1)
        print_report(report_file)
    
    else:
        print("用法: python disk_manager.py [scan|analyze|report]")

