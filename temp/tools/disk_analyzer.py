#!/usr/bin/env python3
"""
disk_analyzer.py — 磁盘空间分析器
功能: 扫描指定盘符/目录，生成HTML可视化报告
  - Top N 最大文件
  - 各目录占用饼图(SVG)
  - 重复文件检测(基于size+hash)
  - 临时文件/缓存清理建议
用法: python disk_analyzer.py D: [--output report.html] [--top 50]
"""

import os, sys, argparse, hashlib, time, math, html as html_mod
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# ── 常量 ──
TEMP_PATTERNS_EXT = {'.tmp', '.temp', '.log', '.bak', '.old', '.swp', '.swo',
                     '.pyc', '.pyo', '.cache', '.dmp', '.crash'}
TEMP_PATTERNS_DIR = {'__pycache__', '.cache', 'cache', 'tmp', 'temp', 'logs',
                     '.tmp', 'node_modules', '.tox', '.pytest_cache', '.mypy_cache'}
TEMP_PREFIXES = ('~$', '~', '.~')

PIE_COLORS = [
    '#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F',
    '#EDC948', '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC',
    '#86BCB6', '#D4A6C8', '#8CD17D', '#B6992D', '#499894',
    '#E49444', '#D37295', '#A0CBE8', '#FFBE7D', '#8B8B8B',
]


def fmt_size(size_bytes):
    if size_bytes < 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def partial_hash(filepath, chunk_size=8192):
    try:
        fsize = os.path.getsize(filepath)
        h = hashlib.md5()
        with open(filepath, 'rb') as f:
            h.update(f.read(chunk_size))
            if fsize > chunk_size * 2:
                f.seek(-chunk_size, 2)
                h.update(f.read(chunk_size))
        return h.hexdigest()
    except (OSError, PermissionError):
        return None


def is_temp_file(filepath):
    name = os.path.basename(filepath).lower()
    ext = os.path.splitext(name)[1].lower()
    parts = set(p.lower() for p in Path(filepath).parts)
    if ext in TEMP_PATTERNS_EXT:
        return True
    if parts & TEMP_PATTERNS_DIR:
        return True
    for prefix in TEMP_PREFIXES:
        if name.startswith(prefix):
            return True
    return False


def scan_directory(root_path, progress_interval=5000):
    files = []
    errors = []
    dir_sizes = defaultdict(int)
    total_size = 0
    count = 0
    t0 = time.time()
    root_path = os.path.abspath(root_path)

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        dirnames[:] = [d for d in dirnames if not d.startswith('$')
                       and d.lower() not in ('system volume information',)]
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            try:
                stat = os.stat(fpath)
                fsize = stat.st_size
                mtime = stat.st_mtime
                files.append((fpath, fsize, mtime))
                total_size += fsize

                rel = os.path.relpath(fpath, root_path)
                top_dir = rel.split(os.sep)[0]
                if os.path.isfile(os.path.join(root_path, top_dir)):
                    top_dir = '<根目录文件>'
                dir_sizes[top_dir] += fsize

                count += 1
                if count % progress_interval == 0:
                    elapsed = time.time() - t0
                    print(f"  已扫描 {count:,} 个文件 ({fmt_size(total_size)}) [{elapsed:.1f}s]")
            except (OSError, PermissionError) as e:
                errors.append(str(e))

    elapsed = time.time() - t0
    print(f"  扫描完成: {count:,} 个文件, {fmt_size(total_size)}, {elapsed:.1f}s, {len(errors)} 个错误")
    return files, dict(dir_sizes), total_size, errors


def find_duplicates(files, min_size=102400):
    print(f"  检测重复文件 (>= {fmt_size(min_size)})...")
    size_groups = defaultdict(list)
    for fpath, fsize, mtime in files:
        if fsize >= min_size:
            size_groups[fsize].append(fpath)

    candidates = {sz: paths for sz, paths in size_groups.items() if len(paths) >= 2}
    print(f"  {len(candidates)} 个大小组有潜在重复")

    duplicates = []
    for fsize, paths in candidates.items():
        hash_groups = defaultdict(list)
        for p in paths:
            h = partial_hash(p)
            if h:
                hash_groups[h].append(p)
        for h, group in hash_groups.items():
            if len(group) >= 2:
                duplicates.append((fsize, group))

    duplicates.sort(key=lambda x: x[0] * (len(x[1]) - 1), reverse=True)
    print(f"  发现 {len(duplicates)} 组重复文件")
    return duplicates[:100]


def find_temp_files(files):
    temp_files = []
    for fpath, fsize, mtime in files:
        if is_temp_file(fpath):
            temp_files.append((fpath, fsize, mtime))
    temp_files.sort(key=lambda x: x[1], reverse=True)
    total = sum(f[1] for f in temp_files)
    print(f"  发现 {len(temp_files)} 个临时/缓存文件, 共 {fmt_size(total)}")
    return temp_files, total


def generate_svg_pie(dir_sizes, total_size, width=500, height=500):
    if not dir_sizes or total_size == 0:
        return '<p>无数据</p>'

    sorted_dirs = sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True)
    main_dirs = sorted_dirs[:15]
    other_size = sum(s for _, s in sorted_dirs[15:])
    if other_size > 0:
        main_dirs.append(('其他', other_size))

    cx, cy, r = width // 2, height // 2, min(width, height) // 2 - 60
    svg_parts = []
    svg_parts.append(f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="max-width:{width}px; font-family:sans-serif;">')

    start_angle = 0
    legend_items = []

    for i, (dirname, size) in enumerate(main_dirs):
        pct = size / total_size
        angle = pct * 360
        end_angle = start_angle + angle
        large_arc = 1 if angle > 180 else 0
        x1 = cx + r * math.cos(math.radians(start_angle - 90))
        y1 = cy + r * math.sin(math.radians(start_angle - 90))
        x2 = cx + r * math.cos(math.radians(end_angle - 90))
        y2 = cy + r * math.sin(math.radians(end_angle - 90))
        color = PIE_COLORS[i % len(PIE_COLORS)]

        dn_esc = html_mod.escape(dirname)
        if pct > 0.999:
            svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="white" stroke-width="1"/>')
        elif pct > 0.001:
            path_d = f'M {cx},{cy} L {x1:.2f},{y1:.2f} A {r},{r} 0 {large_arc},1 {x2:.2f},{y2:.2f} Z'
            svg_parts.append(f'<path d="{path_d}" fill="{color}" stroke="white" stroke-width="1.5"><title>{dn_esc}: {fmt_size(size)} ({pct*100:.1f}%)</title></path>')

        legend_items.append((color, dirname, size, pct))
        start_angle = end_angle

    svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{int(r*0.35)}" fill="white"/>')
    svg_parts.append(f'<text x="{cx}" y="{cy-8}" text-anchor="middle" font-size="14" font-weight="bold">总计</text>')
    svg_parts.append(f'<text x="{cx}" y="{cy+14}" text-anchor="middle" font-size="13">{fmt_size(total_size)}</text>')
    svg_parts.append('</svg>')

    legend_html = '<div class="legend"><table>'
    for color, dirname, size, pct in legend_items:
        dn = html_mod.escape(dirname[:40])
        legend_html += f'<tr><td><span class="dot" style="background:{color}"></span></td><td>{dn}</td><td class="r">{fmt_size(size)}</td><td class="r">{pct*100:.1f}%</td></tr>'
    legend_html += '</table></div>'

    return '\n'.join(svg_parts) + legend_html


def build_html(root_path, files, dir_sizes, total_size,
               top_files, duplicates, temp_files, temp_total, errors, scan_time):
    """Build the complete HTML report string."""
    import shutil

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    esc = html_mod.escape

    # Drive info card
    drive_card = ''
    try:
        usage = shutil.disk_usage(root_path[:3])
        pct = usage.used / usage.total * 100
        drive_card = f'''<div class="card warn">
<h3>💾 磁盘概况 ({esc(root_path[:3])})</h3>
<div class="stats">
<div><span class="big">{fmt_size(usage.total)}</span><br>总容量</div>
<div><span class="big">{fmt_size(usage.used)}</span><br>已使用</div>
<div><span class="big">{fmt_size(usage.free)}</span><br>可用</div>
<div><span class="big">{pct:.1f}%</span><br>使用率</div>
</div></div>'''
    except Exception:
        pass

    pie_svg = generate_svg_pie(dir_sizes, total_size)

    # Top files rows
    top_rows = []
    for i, (fpath, fsize, mtime) in enumerate(top_files, 1):
        ext = os.path.splitext(fpath)[1].lower()
        dt = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        fp = esc(fpath)
        top_rows.append(f'<tr><td>{i}</td><td class="path" title="{fp}">{fp}</td><td class="r">{fmt_size(fsize)}</td><td>{ext}</td><td>{dt}</td></tr>')
    top_rows_html = '\n'.join(top_rows)

    # Duplicate rows
    dup_rows = []
    dup_total_waste = 0
    for i, (fsize, group) in enumerate(duplicates[:30], 1):
        waste = fsize * (len(group) - 1)
        dup_total_waste += waste
        paths_html = '<br>'.join(esc(p) for p in group)
        dup_rows.append(f'<tr><td>{i}</td><td class="path">{paths_html}</td><td class="r">{fmt_size(fsize)}</td><td>{len(group)}</td><td class="r">{fmt_size(waste)}</td></tr>')
    dup_rows_html = '\n'.join(dup_rows) if dup_rows else '<tr><td colspan="5">未发现重复文件</td></tr>'

    # Temp by extension
    temp_by_ext = defaultdict(lambda: [0, 0])
    for fpath, fsize, mtime in temp_files:
        ext = os.path.splitext(fpath)[1].lower() or '(无扩展名)'
        temp_by_ext[ext][0] += 1
        temp_by_ext[ext][1] += fsize
    temp_ext_sorted = sorted(temp_by_ext.items(), key=lambda x: x[1][1], reverse=True)

    temp_ext_rows = []
    for ext, (cnt, sz) in temp_ext_sorted[:20]:
        temp_ext_rows.append(f'<tr><td>{esc(ext)}</td><td class="r">{cnt:,}</td><td class="r">{fmt_size(sz)}</td></tr>')
    temp_ext_html = '\n'.join(temp_ext_rows)

    temp_top_rows = []
    for i, (fpath, fsize, mtime) in enumerate(temp_files[:20], 1):
        fp = esc(fpath)
        temp_top_rows.append(f'<tr><td>{i}</td><td class="path" title="{fp}">{fp}</td><td class="r">{fmt_size(fsize)}</td></tr>')
    temp_top_html = '\n'.join(temp_top_rows) if temp_top_rows else '<tr><td colspan="3">无临时文件</td></tr>'

    error_card = ''
    if errors:
        error_card = f'<div class="card"><h3>⚠️ 扫描错误 ({len(errors)}个)</h3><p style="font-size:12px;color:#999;">部分文件/目录因权限不足无法访问</p></div>'

    CSS = '''* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; background:#f0f2f5; color:#333; padding:20px; }
.container { max-width:1200px; margin:0 auto; }
h1 { color:#1a1a2e; margin-bottom:5px; }
.subtitle { color:#666; margin-bottom:20px; font-size:14px; }
.card { background:white; border-radius:12px; padding:24px; margin-bottom:20px; box-shadow:0 2px 8px rgba(0,0,0,0.08); }
.card h3 { color:#2c3e50; margin-bottom:16px; border-bottom:2px solid #eee; padding-bottom:8px; }
.card.warn { border-left:4px solid #f39c12; }
.stats { display:flex; gap:30px; flex-wrap:wrap; }
.stats div { text-align:center; }
.big { font-size:28px; font-weight:bold; color:#2c3e50; }
.pie-section { display:flex; gap:30px; align-items:flex-start; flex-wrap:wrap; }
.pie-section svg { flex-shrink:0; }
.legend { font-size:13px; }
.legend table { border-collapse:collapse; }
.legend td { padding:3px 10px; }
.dot { display:inline-block; width:12px; height:12px; border-radius:3px; }
table.data { width:100%; border-collapse:collapse; font-size:13px; }
table.data th { background:#f8f9fa; padding:10px 12px; text-align:left; border-bottom:2px solid #dee2e6; position:sticky; top:0; }
table.data td { padding:8px 12px; border-bottom:1px solid #eee; }
table.data tr:hover { background:#f8f9fa; }
.r { text-align:right; }
.path { max-width:600px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-family:Consolas,monospace; font-size:12px; }
.scroll { max-height:600px; overflow-y:auto; }
.summary-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; margin-bottom:20px; }
.summary-item { background:white; border-radius:10px; padding:20px; text-align:center; box-shadow:0 2px 6px rgba(0,0,0,0.06); }
.summary-item .num { font-size:32px; font-weight:bold; }
.summary-item .label { color:#888; font-size:13px; margin-top:4px; }
.c-blue { color:#4E79A7; } .c-orange { color:#F28E2B; } .c-red { color:#E15759; } .c-green { color:#59A14F; }
footer { text-align:center; color:#aaa; font-size:12px; margin-top:30px; padding:20px; }'''

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>磁盘分析报告 — {esc(root_path)}</title>
<style>{CSS}</style></head>
<body><div class="container">
<h1>📊 磁盘空间分析报告</h1>
<p class="subtitle">扫描路径: {esc(root_path)} | 生成时间: {now} | 扫描耗时: {scan_time:.1f}s</p>

<div class="summary-grid">
<div class="summary-item"><div class="num c-blue">{len(files):,}</div><div class="label">文件总数</div></div>
<div class="summary-item"><div class="num c-orange">{fmt_size(total_size)}</div><div class="label">扫描总大小</div></div>
<div class="summary-item"><div class="num c-red">{len(duplicates):,}</div><div class="label">重复文件组</div></div>
<div class="summary-item"><div class="num c-green">{fmt_size(temp_total)}</div><div class="label">可清理临时文件</div></div>
</div>

{drive_card}

<div class="card"><h3>📁 目录空间占用分布</h3><div class="pie-section">{pie_svg}</div></div>

<div class="card"><h3>🏆 最大的 {len(top_files)} 个文件</h3>
<div class="scroll"><table class="data">
<tr><th>#</th><th>文件路径</th><th>大小</th><th>类型</th><th>修改日期</th></tr>
{top_rows_html}</table></div></div>

<div class="card"><h3>🔁 重复文件 (前30组, 共浪费 {fmt_size(dup_total_waste)})</h3>
<div class="scroll"><table class="data">
<tr><th>#</th><th>文件路径</th><th>单文件大小</th><th>副本数</th><th>浪费空间</th></tr>
{dup_rows_html}</table></div></div>

<div class="card"><h3>🧹 临时/缓存文件清理建议 (共 {len(temp_files):,} 个, {fmt_size(temp_total)})</h3>
<h4 style="margin:12px 0 8px;color:#555;">按类型统计</h4>
<table class="data"><tr><th>文件类型</th><th>数量</th><th>总大小</th></tr>{temp_ext_html}</table>
<h4 style="margin:16px 0 8px;color:#555;">最大的临时文件 (Top 20)</h4>
<div class="scroll" style="max-height:400px;"><table class="data">
<tr><th>#</th><th>文件路径</th><th>大小</th></tr>{temp_top_html}</table></div></div>

{error_card}
<footer>Generated by disk_analyzer.py | {now}</footer>
</div></body></html>'''


def main():
    parser = argparse.ArgumentParser(description='磁盘空间分析器 — 生成HTML可视化报告')
    parser.add_argument('path', help='要分析的盘符或目录路径 (如 D: 或 D:\\Projects)')
    parser.add_argument('--output', '-o', default='', help='输出HTML文件路径')
    parser.add_argument('--top', '-n', type=int, default=50, help='显示最大文件数量 (默认50)')
    parser.add_argument('--min-dup-size', type=int, default=100, help='重复检测最小文件大小KB (默认100)')

    args = parser.parse_args()

    root = args.path
    if len(root) == 2 and root[1] == ':':
        root += '\\'

    if not os.path.exists(root):
        print(f"错误: 路径不存在: {root}")
        sys.exit(1)

    output = args.output or f'disk_report_{root[0] if len(root)>=2 and root[1]==":" else "dir"}.html'

    print(f"{'='*60}")
    print(f"  磁盘空间分析器")
    print(f"  扫描路径: {root}")
    print(f"{'='*60}")

    print("\n[1/4] 扫描文件系统...")
    t0 = time.time()
    files, dir_sizes, total_size, errors = scan_directory(root)
    scan_time = time.time() - t0

    if not files:
        print("未找到任何文件!")
        sys.exit(1)

    print(f"\n[2/4] 排序找出 Top {args.top} 最大文件...")
    files_sorted = sorted(files, key=lambda x: x[1], reverse=True)
    top_files = files_sorted[:args.top]

    print(f"\n[3/4] 检测重复文件...")
    duplicates = find_duplicates(files, min_size=args.min_dup_size * 1024)

    print(f"\n[4/4] 识别临时/缓存文件...")
    temp_files, temp_total = find_temp_files(files)

    print(f"\n生成HTML报告...")
    html_content = build_html(
        root, files, dir_sizes, total_size,
        top_files, duplicates, temp_files, temp_total, errors, scan_time
    )

    with open(output, 'w', encoding='utf-8') as f:
        f.write(html_content)

    fsize = os.path.getsize(output)
    print(f"\n{'='*60}")
    print(f"  [OK] 报告已生成: {os.path.abspath(output)} ({fmt_size(fsize)})")
    print(f"  文件总数: {len(files):,}  总大小: {fmt_size(total_size)}")
    print(f"  重复文件组: {len(duplicates)}  可清理: {fmt_size(temp_total)}")
    print(f"{'='*60}")

    return output


if __name__ == '__main__':
    main()