"""
batch_import_toolkit.py - 教案知识库批量导入工具

功能：从文件夹批量导入markdown教案到teaching_kb
"""
import os
import re
import shutil
from pathlib import Path

def parse_lesson_filename(filename):
    """解析教案文件名，提取课次编号和主题
    支持格式：L01_主题.md, 01_主题.md, L01-主题.md
    """
    patterns = [
        r'^L?(\d+)[_-](.+)\.md$',
        r'^lesson_?(\d+)[_-](.+)\.md$',
    ]
    for p in patterns:
        m = re.match(p, filename, re.I)
        if m:
            num = m.group(1).zfill(2)
            topic = m.group(2).strip()
            return f'L{num}', topic
    return None, None

def batch_import(source_dir, course_name, kb_base='./teaching_kb', dry_run=False):
    """批量导入教案文件
    
    Args:
        source_dir: 源文件夹路径
        course_name: 课程名称
        kb_base: teaching_kb根目录
        dry_run: 仅预览不实际操作
    
    Returns:
        dict: {success: [], failed: [], skipped: []}
    """
    result = {'success': [], 'failed': [], 'skipped': []}
    
    course_dir = Path(kb_base) / 'courses' / course_name / 'lessons'
    
    if not Path(source_dir).exists():
        result['failed'].append(f'源目录不存在: {source_dir}')
        return result
    
    for f in os.listdir(source_dir):
        if not f.endswith('.md'):
            continue
        
        lesson_num, topic = parse_lesson_filename(f)
        if not lesson_num:
            result['skipped'].append(f'{f} (无法解析文件名)')
            continue
        
        lesson_dir = course_dir / f'{lesson_num}_{topic}'
        target_file = lesson_dir / 'lesson_plan.md'
        
        if target_file.exists():
            result['skipped'].append(f'{f} (目标已存在: {target_file})')
            continue
        
        if dry_run:
            result['success'].append(f'{f} -> {target_file} (预览)')
        else:
            lesson_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(Path(source_dir) / f, target_file)
            # 创建materials_index.md骨架
            (lesson_dir / 'materials_index.md').write_text(
                f'# {lesson_num}_{topic} 素材清单\n\n暂无素材\n',
                encoding='utf-8'
            )
            result['success'].append(f'{f} -> {target_file}')
    
    return result

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('用法: python batch_import_toolkit.py <源目录> <课程名> [--dry-run]')
        sys.exit(1)
    
    src = sys.argv[1]
    course = sys.argv[2]
    dry = '--dry-run' in sys.argv
    
    r = batch_import(src, course, dry_run=dry)
    print(f'成功: {len(r["success"])}')
    for s in r['success']: print(f'  ✓ {s}')
    print(f'跳过: {len(r["skipped"])}')
    for s in r['skipped']: print(f'  - {s}')
    print(f'失败: {len(r["failed"])}')
    for s in r['failed']: print(f'  ✗ {s}')
