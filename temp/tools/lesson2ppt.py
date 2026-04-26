#!/usr/bin/env python3
"""
lesson2ppt.py - 教案(lesson_plan.md) → PPT 自动生成管道
用法:
  python lesson2ppt.py <lesson_plan.md路径> [输出pptx路径] [配色方案]
  
会解析 lesson_plan.md 的结构化 Markdown，转换为 generate_ppt 所需的 config，
然后调用 generate_ppt() 生成教学PPT。
"""
import sys, os, re, json

# 路径设置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PPT_LAB = os.path.join(os.path.dirname(SCRIPT_DIR), 'ppt_lab')
sys.path.insert(0, PPT_LAB)

from generate_ppt import generate_ppt


def parse_lesson_plan(md_path: str) -> dict:
    """解析 lesson_plan.md，返回结构化字典"""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    result = {
        'title': '',
        'course': '',
        'code': '',
        'topic': '',
        'objectives': [],
        'hours': '',
        'content_overview': [],
        'key_points': '',
        'difficult_points': '',
        'teaching_process': [],   # list of (phase_name, items)
        'homework': [],
        'board_design': [],
    }
    
    # 提取标题行
    title_match = re.search(r'^#\s+(.+)', text, re.MULTILINE)
    if title_match:
        result['title'] = title_match.group(1).strip()
    
    # 按 ## 分割大节
    sections = re.split(r'\n(?=## )', text)
    
    for sec in sections:
        sec_title_m = re.match(r'## (.+)', sec)
        if not sec_title_m:
            continue
        sec_title = sec_title_m.group(1).strip()
        sec_body = sec[sec_title_m.end():]
        
        if '基本信息' in sec_title:
            for line in sec_body.split('\n'):
                line = line.strip().lstrip('- ')
                if line.startswith('课程名称'):
                    result['course'] = line.split('：', 1)[-1].strip() if '：' in line else line.split(':', 1)[-1].strip()
                elif line.startswith('课次编码'):
                    result['code'] = line.split('：', 1)[-1].strip() if '：' in line else line.split(':', 1)[-1].strip()
                elif line.startswith('主题'):
                    result['topic'] = line.split('：', 1)[-1].strip() if '：' in line else line.split(':', 1)[-1].strip()
                elif line.startswith('建议学时'):
                    result['hours'] = line.split('：', 1)[-1].strip() if '：' in line else line.split(':', 1)[-1].strip()
                elif line.startswith('-') or line.startswith('  -'):
                    # sub-bullet under 教学目标
                    clean = line.lstrip('- ').strip()
                    if clean and '教学目标' not in clean:
                        result['objectives'].append(clean)
                elif '教学目标' not in line and line:
                    # might be an objective continuation
                    pass
            # re-parse objectives more carefully
            obj_section = re.search(r'教学目标[：:]?\s*\n((?:\s+-\s+.+\n?)+)', sec_body)
            if obj_section:
                result['objectives'] = [
                    l.strip().lstrip('- ') 
                    for l in obj_section.group(1).strip().split('\n') 
                    if l.strip().startswith('-')
                ]
        
        elif '教学内容概述' in sec_title:
            result['content_overview'] = [
                l.strip().lstrip('- ') 
                for l in sec_body.strip().split('\n') 
                if l.strip().startswith('-')
            ]
        
        elif '教学重难点' in sec_title:
            for line in sec_body.strip().split('\n'):
                line = line.strip().lstrip('- ')
                if line.startswith('重点'):
                    result['key_points'] = line.split('：', 1)[-1].strip() if '：' in line else line
                elif line.startswith('难点'):
                    result['difficult_points'] = line.split('：', 1)[-1].strip() if '：' in line else line
        
        elif '教学过程' in sec_title:
            # 按 ### 分割子节
            sub_sections = re.split(r'\n(?=### )', sec_body)
            for sub in sub_sections:
                sub_m = re.match(r'### \d+\.\s*(.+)', sub.strip())
                if not sub_m:
                    continue
                phase_name = sub_m.group(1).strip()
                items = [
                    l.strip().lstrip('- ')
                    for l in sub[sub_m.end():].strip().split('\n')
                    if l.strip().startswith('-')
                ]
                result['teaching_process'].append((phase_name, items))
        
        elif '作业' in sec_title:
            result['homework'] = [
                l.strip().lstrip('- ')
                for l in sec_body.strip().split('\n')
                if l.strip().startswith('-')
            ]
        
        elif '板书' in sec_title:
            result['board_design'] = [
                l.strip().lstrip('- ')
                for l in sec_body.strip().split('\n')
                if l.strip().startswith('-')
            ]
    
    return result


def lesson_to_ppt_config(lesson: dict, scheme: str = 'academic_blue') -> dict:
    """将解析后的教案字典转换为 generate_ppt 所需的 config"""
    slides = []
    
    # 1. 封面
    subtitle_parts = []
    if lesson['course']:
        subtitle_parts.append(lesson['course'])
    if lesson['code']:
        subtitle_parts.append(lesson['code'])
    if lesson['hours']:
        subtitle_parts.append(lesson['hours'])
    
    slides.append({
        'type': 'title',
        'title': lesson['topic'] or lesson['title'],
        'subtitle': ' | '.join(subtitle_parts)
    })
    
    # 2. 目录 - 从教学过程的阶段名构建
    toc_sections = []
    if lesson['content_overview']:
        toc_sections.append('教学内容概述')
    if lesson['key_points'] or lesson['difficult_points']:
        toc_sections.append('重点与难点')
    for phase_name, _ in lesson['teaching_process']:
        toc_sections.append(phase_name)
    if lesson['homework']:
        toc_sections.append('作业布置')
    
    if toc_sections:
        slides.append({
            'type': 'toc',
            'title': '教学大纲',
            'sections': toc_sections,
            'current': -1
        })
    
    # 2.5 教学流程总览 (timeline) —— 鸟瞰整个教学过程
    if lesson['teaching_process']:
        flow_events = []
        time_icons = ['🚀', '📖', '✏️', '💬', '📋', '🔬', '🎯', '⚡']
        for i, (phase_name, items) in enumerate(lesson['teaching_process']):
            summary = f"{len(items)} 个要点" if items else "教学环节"
            flow_events.append([f"{time_icons[i % len(time_icons)]} 环节{i+1}", f"{phase_name}（{summary}）"])
        slides.append({
            'type': 'timeline',
            'title': '📋 教学流程总览',
            'events': flow_events
        })
    
    # 3. 教学目标 (icon_cards)
    if lesson['objectives']:
        obj_cards = []
        icons = ['🎯', '📚', '🔬', '💡', '🧠', '⚡']
        for i, obj in enumerate(lesson['objectives']):
            obj_cards.append({
                'icon': icons[i % len(icons)],
                'title': f'目标 {i+1}',
                'desc': obj
            })
        slides.append({
            'type': 'icon_cards',
            'title': '教学目标',
            'cards': obj_cards
        })
    
    # 3.5 课程数据概览 (stats) —— 用数字卡片展示课程关键指标
    stats_items = []
    if lesson['objectives']:
        stats_items.append({'number': str(len(lesson['objectives'])), 'label': '教学目标'})
    if lesson['teaching_process']:
        stats_items.append({'number': str(len(lesson['teaching_process'])), 'label': '教学环节'})
    total_points = sum(len(items) for _, items in lesson['teaching_process'])
    if total_points:
        stats_items.append({'number': str(total_points), 'label': '知识要点'})
    if lesson['key_points']:
        stats_items.append({'number': str(len(lesson['key_points'])), 'label': '教学重点'})
    if stats_items:
        slides.append({
            'type': 'stats',
            'title': '📊 课程数据概览',
            'stats': stats_items
        })
    
    # 4. 教学内容概述
    if lesson['content_overview']:
        slides.append({
            'type': 'content',
            'title': '教学内容概述',
            'bullets': lesson['content_overview'],
            'highlights': [0] if len(lesson['content_overview']) > 0 else []
        })
    
    # 5. 重点与难点 (comparison)
    if lesson['key_points'] or lesson['difficult_points']:
        slides.append({
            'type': 'comparison',
            'title': '教学重点与难点',
            'left_title': '🔑 重点',
            'left_items': [lesson['key_points']] if lesson['key_points'] else ['（无）'],
            'right_title': '⚠️ 难点',
            'right_items': [lesson['difficult_points']] if lesson['difficult_points'] else ['（无）']
        })
    
    # 6. 教学过程各阶段 —— 不同阶段使用不同版式，避免单调
    phase_icons = {
        '导入': '🚀', '课程导入': '🚀', '情境导入': '🚀',
        '新课讲解': '📖', '新课讲授': '📖', '知识讲解': '📖', '讲授': '📖',
        '课堂练习': '✏️', '实践练习': '✏️', '练习': '✏️', '实验': '🔬',
        '课堂小结': '📋', '小结': '📋', '总结': '📋', '归纳总结': '📋',
        '互动讨论': '💬', '讨论': '💬', '案例分析': '🔍',
    }
    # 阶段→slide类型映射（让不同环节有不同视觉风格）
    phase_slide_type = {
        '导入': 'highlight_content', '课程导入': 'highlight_content', '情境导入': 'highlight_content',
        '新课讲解': 'content', '新课讲授': 'content', '知识讲解': 'content', '讲授': 'content',
        '课堂练习': 'step_cards', '实践练习': 'step_cards', '练习': 'step_cards', '实验': 'step_cards',
        '课堂小结': 'stats', '小结': 'stats', '总结': 'stats', '归纳总结': 'stats',
        '互动讨论': 'content', '讨论': 'content', '案例分析': 'step_cards',
    }
    # 阶段→bullet emoji映射
    phase_bullet_emojis = {
        '导入': ['💡', '🌟', '❓', '🎬', '🔔'],
        '新课讲解': ['📌', '🔹', '📐', '🧩', '📊'],
        '课堂练习': ['✅', '📝', '🔧', '⚙️', '🎯'],
        '课堂小结': ['⭐', '🔑', '💎', '📍', '🏆'],
        '互动讨论': ['💬', '🤔', '💭', '🗣️', '📢'],
    }
    # 通用 emoji 池（找不到精确匹配时用）
    default_emojis = ['▸', '◆', '●', '★', '►']
    
    for idx, (phase_name, items) in enumerate(lesson['teaching_process']):
        # 阶段分隔页
        icon = phase_icons.get(phase_name, '📌')
        # 为 section 页添加描述性副标题
        section_subtitle = f'第 {idx+1} 环节 · 共 {len(items)} 个要点' if items else ''
        slides.append({
            'type': 'section',
            'title': f'{icon} {phase_name}',
            'subtitle': section_subtitle
        })
        
        # 阶段内容 —— 根据阶段类型选择不同版式
        if items:
            # 确定 slide 类型
            slide_type = phase_slide_type.get(phase_name, 'content')
            
            # 给 bullet 加 emoji 前缀
            emojis = default_emojis
            for key, emos in phase_bullet_emojis.items():
                if key in phase_name:
                    emojis = emos
                    break
            enriched_items = [
                f"{emojis[i % len(emojis)]} {item}" for i, item in enumerate(items)
            ]
            
            if slide_type == 'stats':
                # 统计卡片版式：每条要点作为一张数字卡片（适合小结/总结）
                summary_stats = []
                stat_icons = ['⭐', '🔑', '💎', '📍', '🏆', '✅']
                for si, item in enumerate(items):
                    summary_stats.append({
                        'number': stat_icons[si % len(stat_icons)],
                        'label': item
                    })
                slides.append({
                    'type': 'stats',
                    'title': f'{icon} {phase_name}',
                    'stats': summary_stats
                })
            elif slide_type == 'highlight_content':
                # 高亮内容版式：第一条作为主高亮，其余作为辅助说明
                slides.append({
                    'type': 'highlight_content',
                    'title': f'{icon} {phase_name}',
                    'highlight_text': enriched_items[0] if enriched_items else phase_name,
                    'sub_points': enriched_items[1:] if len(enriched_items) > 1 else [''],
                })
            elif slide_type == 'step_cards':
                # 步骤卡片版式：每条作为一个编号步骤
                slides.append({
                    'type': 'step_cards',
                    'title': f'{icon} {phase_name}',
                    'steps': items,  # step_cards 内部会加编号，不需要 emoji
                })
            else:
                # 增强内容版式（默认）
                slides.append({
                    'type': 'content',
                    'title': f'{icon} {phase_name}',
                    'bullets': enriched_items,
                    'highlights': [0] if len(enriched_items) > 2 else []
                })
    
    # 7. 作业布置 —— 使用 step_cards 版式（编号任务更清晰）
    if lesson['homework']:
        slides.append({
            'type': 'step_cards',
            'title': '📝 作业布置',
            'steps': lesson['homework'],
        })
    
    # 7.5 教学内容分布图 (chart) —— 饼图展示各环节知识点占比
    if lesson['teaching_process'] and len(lesson['teaching_process']) >= 2:
        chart_categories = []
        chart_values = []
        for phase_name, items in lesson['teaching_process']:
            if items:  # 只展示有内容的环节
                chart_categories.append(phase_name)
                chart_values.append(len(items))
        if chart_categories:
            slides.append({
                'type': 'chart',
                'title': '📊 教学内容分布',
                'chart_type': 'pie',
                'categories': chart_categories,
                'series': [{'name': '知识点数量', 'values': chart_values}]
            })
    
    # 8. 结尾
    slides.append({
        'type': 'ending',
        'title': '谢谢！',
        'contact': f'{lesson["course"]} - {lesson["topic"]}'
    })
    
    return {
        'scheme': scheme,
        'slides': slides
    }


def update_materials_index(lesson_dir: str, pptx_filename: str):
    """更新或创建 materials_index.md"""
    index_path = os.path.join(lesson_dir, 'materials_index.md')
    # 获取课次信息
    dir_name = os.path.basename(lesson_dir)
    
    content = f"""# {dir_name} - 教学素材清单

| 文件名 | 类型 | 用途说明 |
|--------|------|----------|
| {pptx_filename} | PPT | 课堂讲授用主课件（自动生成） |
"""
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] 素材清单已更新: {index_path}")




def batch_convert(course_dir: str, scheme: str = 'academic_blue', force: bool = False) -> list:
    """
    批量转换：扫描course_dir下所有lesson_plan.md，逐一生成PPT。
    参数:
        course_dir: 课程根目录，如 teaching_kb/courses/图神经网络与大语言模型
        scheme: 配色方案，默认 academic_blue
        force: True则跳过已存在PPT的检查强制重新生成
    返回: 生成成功的pptx路径列表
    """
    import glob
    results = []
    errors = []

    # 找所有 lesson_plan.md
    pattern = os.path.join(course_dir, '**', 'lesson_plan.md')
    md_files = sorted(glob.glob(pattern, recursive=True))

    if not md_files:
        print(f'[BATCH] 未找到任何 lesson_plan.md in {course_dir}')
        return results

    print(f'[BATCH] 发现 {len(md_files)} 个教案，课程目录: {course_dir}')
    print(f'[BATCH] 配色方案: {scheme} | 强制重生成: {force}')
    print('-' * 60)

    for i, md_path in enumerate(md_files, 1):
        lesson_dir = os.path.dirname(md_path)
        slides_dir = os.path.join(lesson_dir, 'slides')

        # 检查是否已生成（非force模式跳过）
        if not force:
            existing = [f for f in os.listdir(slides_dir) if f.endswith('.pptx')] if os.path.exists(slides_dir) else []
            if existing:
                print(f'[{i}/{len(md_files)}] SKIP (已存在): {existing[0]}')
                results.append(os.path.join(slides_dir, existing[0]))
                continue

        print(f'[{i}/{len(md_files)}] 处理: {os.path.relpath(md_path, course_dir)}')
        try:
            lesson = parse_lesson_plan(md_path)
            config = lesson_to_ppt_config(lesson, scheme)
            os.makedirs(slides_dir, exist_ok=True)
            safe_topic = lesson['topic'] or 'teaching'
            out_path = os.path.join(slides_dir, f"{lesson['course']}_{safe_topic}_教学课件.pptx")
            generate_ppt(config, out_path)
            update_materials_index(lesson_dir, os.path.basename(out_path))
            results.append(out_path)
            sz = os.path.getsize(out_path)
            print(f'       OK -> {os.path.basename(out_path)} ({sz//1024}KB, {len(config["slides"])}页)')
        except Exception as e:
            errors.append((md_path, str(e)))
            print(f'       ERROR: {e}')

    print('-' * 60)
    print(f'[BATCH] 完成: {len(results)} 成功 / {len(errors)} 失败')
    if errors:
        for ep, emsg in errors:
            print(f'  FAIL: {ep} -> {emsg}')
    return results


def main():
    if len(sys.argv) < 2:
        print('用法:')
        print('  单文件: python lesson2ppt.py <lesson_plan.md路径> [output.pptx] [scheme]')
        print('  批量:   python lesson2ppt.py --batch <课程目录> [scheme] [--force]')
        print('示例:')
        print('  python lesson2ppt.py teaching_kb/courses/编译原理/lessons/L01_编译原理概述/lesson_plan.md')
        print('  python lesson2ppt.py --batch teaching_kb/courses/图神经网络与大语言模型 academic_blue')
        sys.exit(1)

    # 批量模式
    if sys.argv[1] == '--batch':
        if len(sys.argv) < 3:
            print('[ERROR] --batch 需要指定课程目录')
            sys.exit(1)
        course_dir = sys.argv[2]
        scheme = sys.argv[3] if len(sys.argv) > 3 else 'academic_blue'
        force = '--force' in sys.argv
        if not os.path.isdir(course_dir):
            print(f'[ERROR] 目录不存在: {course_dir}')
            sys.exit(1)
        results = batch_convert(course_dir, scheme=scheme, force=force)
        print(f'\n批量生成完成，共 {len(results)} 个PPT')
        return results

    # 单文件模式
    md_path = sys.argv[1]
    scheme = sys.argv[3] if len(sys.argv) > 3 else 'academic_blue'

    if not os.path.exists(md_path):
        print(f'[ERROR] 文件不存在: {md_path}')
        sys.exit(1)

    print(f'[1/4] 解析教案: {md_path}')
    lesson = parse_lesson_plan(md_path)
    print(f'      课程: {lesson["course"]} | 主题: {lesson["topic"]}')
    print(f'      教学目标: {len(lesson["objectives"])} 条')
    print(f'      教学过程: {len(lesson["teaching_process"])} 个阶段')

    print(f'[2/4] 生成PPT配置...')
    config = lesson_to_ppt_config(lesson, scheme)
    print(f'      共 {len(config["slides"])} 页幻灯片')

    lesson_dir = os.path.dirname(md_path)
    slides_dir = os.path.join(lesson_dir, 'slides')
    os.makedirs(slides_dir, exist_ok=True)

    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        safe_topic = re.sub(r'[/\\:*?"<>|]', '、', lesson['topic'] or 'teaching').strip()
        output_path = os.path.join(slides_dir, f"{lesson['course']}_{safe_topic}_教学课件.pptx")

    print(f'[3/4] 生成PPT: {output_path}')
    generate_ppt(config, output_path)

    print(f'[4/4] 更新素材清单...')
    pptx_filename = os.path.basename(output_path)
    update_materials_index(lesson_dir, pptx_filename)

    config_path = os.path.join(slides_dir, 'ppt_config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        import json as _json
        _json.dump(config, f, ensure_ascii=False, indent=2)

    print(f'\n教案->PPT 生成完成!')
    print(f'   PPT文件: {output_path}')
    print(f'   配置文件: {config_path}')
    print(f'   幻灯片数: {len(config["slides"])} 页')

    # [quality_scorer集成] 生成质量报告
    try:
        _slides = config.get('slides', [])
        _n = len(_slides)
        _title = lesson.get('title', '') or lesson.get('topic', '')
        _objectives = lesson.get('objectives', [])
        _phases = lesson.get('teaching_process', [])
        _homework = lesson.get('homework', [])

        # 各维度评分
        _s_structure = min(10, 4 + len(_phases) * 1.2)  # 教学结构完整性
        _s_content = min(10, 3 + len(_objectives) * 1.5 + (1 if _homework else 0))  # 内容覆盖度
        _s_slides = min(10, 4 + _n * 0.4)  # 幻灯片数量合理性(10页以上满分)
        _s_homework = 8.0 if _homework else 4.0  # 作业设计
        _s_total = round((_s_structure + _s_content + _s_slides + _s_homework) / 4, 1)

        _report_lines = [
            f'# 教案->PPT 质量报告',
            f'生成时间: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            f'教案文件: {md_path}',
            f'PPT文件:  {output_path}',
            f'',
            f'## 各维度得分',
            f'教学结构完整性 : {_s_structure:.1f} / 10  (教学阶段数: {len(_phases)})',
            f'内容覆盖度     : {_s_content:.1f} / 10  (教学目标数: {len(_objectives)}, 作业: {"有" if _homework else "无"})',
            f'幻灯片数量合理性: {_s_slides:.1f} / 10  (幻灯片数: {_n})',
            f'作业设计       : {_s_homework:.1f} / 10',
            f'',
            f'## 总分',
            f'**{_s_total} / 10**',
            f'',
            f'## 建议',
        ]
        if _s_structure < 6:
            _report_lines.append('- 教学结构偏简，建议补充更多教学阶段（导入/讲授/练习/总结）')
        if len(_objectives) < 3:
            _report_lines.append('- 教学目标数量偏少（建议>=3条），建议细化知识/能力/素养目标')
        if _n < 8:
            _report_lines.append(f'- 幻灯片数量偏少({_n}页)，建议每个教学阶段至少2页')
        if not _homework:
            _report_lines.append('- 未发现作业设计，建议添加课后作业或思考题')
        if not _report_lines[-1].startswith('-'):
            _report_lines.append('- 教案质量良好，无明显改进建议')

        _report_path = os.path.join(slides_dir, 'quality_report.txt')
        with open(_report_path, 'w', encoding='utf-8') as _f:
            _f.write('\n'.join(_report_lines) + '\n')
        print(f'   质量报告: {_report_path}')
        print(f'   质量总分: {_s_total} / 10')
    except Exception as _qe:
        print(f'   [WARN] 质量评分失败: {_qe}')

    return output_path


if __name__ == '__main__':
    main()
