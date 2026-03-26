# Ability Map — GenericAgent 工具函数索引

> 自动生成于 2026-03-26 | 覆盖 local_skills/ + temp/ 主要工具

## 论文与知识库

### `local_skills/research_paper_kb_like.py` — GNN论文库接口
| 函数 | 说明 |
|------|------|
| `list_papers()` | 列出所有论文 |
| `search(keyword)` | 按关键词搜索（标题/摘要/关键词） |
| `add(meta_dict)` | 追加一篇论文到PAPERS.md |
| `fetch(arxiv_id)` | 从arXiv获取论文摘要（需联网） |

### `local_skills/pdf_reader.py` — PDF解析
| 函数 | 说明 |
|------|------|
| `extract(pdf_path, save)` | 提取PDF全文文本，返回按页列表 |
| `meta(pdf_path)` | 提取PDF元数据（标题/作者/创建时间/页数） |
| `tables(pdf_path, pages)` | 提取PDF中的表格 |
| `search(pdf_path, keyword, context)` | 在PDF全文中搜索关键词 |

### `temp/arxiv2kb.py` — arXiv抓取入库
| 函数 | 说明 |
|------|------|
| `extract_id(raw)` | 从URL或纯ID提取arXiv ID |
| `fetch_meta(arxiv_id)` | 抓取arXiv页面，返回元数据dict |

### `temp/pdf2kb.py` — PDF→论文库自动入库
| 函数 | 说明 |
|------|------|
| `process_pdf(pdf_path, dry_run)` | 处理单个PDF，提取元数据并入库 |
| `process_dir(dir_path, dry_run)` | 批量处理目录下所有PDF |

### `temp/kb_cli.py` — 论文库CLI查询
| 函数 | 说明 |
|------|------|
| `cmd_list(args)` | 列出论文，支持年份过滤 |
| `cmd_search(args)` | 搜索论文 |
| `cmd_fetch(args)` | 联网获取论文摘要 |
| `fmt_table(papers)` | 输出Markdown表格 |

## PPT制作

### `temp/ppt_com_toolkit.py` — win32com PPT工具库（推荐主力）
| 函数 | 说明 |
|------|------|
| `open_ppt(visible)` | 启动PowerPoint COM实例 |
| `new_prs(app)` | 新建演示文稿 |
| `save_and_quit(app, prs, path)` | 保存并退出 |
| `add_slide(prs, layout)` | 添加幻灯片 |
| `set_bg_solid(slide, r, g, b)` | 纯色背景 |
| `set_bg_gradient(slide, r1,g1,b1, r2,g2,b2, style, variant)` | 渐变背景 |
| `set_transition(slide, effect, speed)` | 幻灯片切换动画 |
| `add_text(slide, text, l,t,w,h, sz, bold, italic, color, align, font, v_anchor, wrap)` | 插入文本框 |
| `add_text_lines(slide, lines, l,t,w,h, sizes, bolds, colors, align, font, spacing)` | 多段落多样式文本框 |
| `add_rect(slide, l,t,w,h, fill, line, lw)` | 矩形 |
| `add_rrect(slide, l,t,w,h, fill, corner)` | 圆角矩形 |
| `add_oval(slide, l,t,w,h, fill)` | 椭圆 |
| `add_line_shape(slide, x1,y1,x2,y2, color, weight)` | 直线 |
| `add_picture(slide, path, l,t,w,h)` | 插入本地图片 |
| `add_table(slide, data, l,t,w,h, head_fill, cell_fill, text_color, sz, font)` | 插入表格 |
| `add_anim_appear(slide, shape, trigger, delay)` | 进入动画（出现） |
| `add_animation(slide, shape, anim_type, effect_id, trigger, delay)` | 统一动画封装 |
| `add_anim_sequence(slide, shapes, effect_id, base_delay, interval)` | 批量顺序动画 |
| `batch_replace_text(prs, replacements)` | 批量替换文本占位符 |
| `set_master_logo(prs, logo_path, l,t,w,h)` | 母版统一插入LOGO |
| `apply_theme_colors(slide, theme)` | 应用预设配色主题 |

### `python-pptx`（直接import，适合图表/复杂布局）
| 能力 | 用法要点 |
|------|---------|
| 原生图表 | `ChartData` + `shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, ...)` |
| 支持类型 | COLUMN_CLUSTERED / BAR / LINE / PIE / AREA 等 |
| 图表标题 | `chart.has_title=True; chart.chart_title.text_frame.text='...'` |

## Word文档

### `temp/word_toolkit.py` — win32com Word工具库
| 函数 | 说明 |
|------|------|
| `open_word(visible)` | 启动Word COM实例 |
| `new_doc(app)` | 新建空白文档 |
| `open_doc(app, path)` | 打开已有docx |
| `save_and_quit(app, doc, path)` | 保存并退出 |
| `save_doc(doc, path)` | 仅保存不退出 |
| `add_heading(doc, text, level)` | 插入标题（1-6级） |
| `add_paragraph(doc, text, bold, italic, sz, align, color)` | 插入正文段落 |
| `add_bullet_list(doc, items, sz, indent_cm)` | 插入项目符号列表（⚠️中文Word需用lesson2word.py的add_bullets替代） |
| `add_page_break(doc)` | 插入分页符 |
| `add_table(doc, data, header_bold, border)` | 插入表格 |
| `add_picture(doc, path, width_cm, height_cm)` | 插入图片 |
| `set_page_margin(doc, top, bottom, left, right)` | 设置页边距(cm) |
| `build_report(output_path, title, sections, table_data)` | 一键生成报告型文档 |

### `temp/lesson2word.py` — 教案Markdown→Word讲义
| 函数 | 说明 |
|------|------|
| `add_bullets(doc, items, sz)` | 前缀模拟项目符号（绕过中文Word List Bullet问题） |
| `build_word(lesson_md, output)` | lesson_plan.md → .docx 讲义 |

## 系统与文件管理

### `temp/phone_sync.py` — ADB手机文件同步
| 函数 | 说明 |
|------|------|
| `check_adb(device)` | 检查adb可用性和设备连接 |
| `cmd_list(phone_dir, ext_filter, device)` | 列出手机目录文件 |
| `cmd_pull(phone_dir, local_dir, ext_filter, dry, device)` | 从手机pull文件到本地 |
| `cmd_push(local_dir, phone_dir, ext_filter, dry, device)` | 从本地push文件到手机 |

### `temp/path_cleaner.py` — PATH环境变量清理
| 函数 | 说明 |
|------|------|
| `get_path_entries()` | 获取当前PATH条目 |
| `analyze(entries)` | 分析无效路径 |
| `build_clean_path(entries, issues)` | 构建清理后的路径列表 |
| `generate_ps1(...)` | 生成修复PowerShell脚本 |
| `generate_report(...)` | 生成分析报告 |

### `temp/disk_analyzer.py` — 磁盘空间分析
| 函数 | 说明 |
|------|------|
| `scan_directory(root_path, ...)` | 扫描目录，统计文件大小 |
| `find_duplicates(files, min_size)` | 查找重复文件 |
| `find_temp_files(files)` | 查找临时文件 |
| `build_html(...)` | 生成HTML分析报告 |

### `temp/cleanup_executor.py` — 安全清理执行
| 函数 | 说明 |
|------|------|
| `collect_safe_targets(root)` | 收集可安全删除的目标 |
| `delete_targets(targets, log_lines)` | 执行删除 |
| `remove_empty_pycache(root, log_lines)` | 清理空__pycache__ |

## 自主任务辅助

### `temp/quality_scorer_v2.py` — 自主任务质量评分
| 函数 | 说明 |
|------|------|
| `parse(path)` | 解析history.txt |
| `score(e)` | 对单条任务评分 |
| `batches(entries)` | 按Batch分组 |
| `run(hist, out)` | 生成HTML评分报告 |

### `temp/history_normalizer.py` — history.txt格式规范化
| 函数 | 说明 |
|------|------|
| `normalize_history()` | 统一history.txt条目格式 |

---

## 覆盖统计

| 类别 | 文件数 | 函数数 |
|------|--------|--------|
| 论文/知识库 | 4 | 15 |
| PPT制作 | 1+pptx | 20+ |
| Word文档 | 2 | 16 |
| 系统/文件 | 3 | 13 |
| 自主任务辅助 | 2 | 8 |
| **合计** | **12** | **72+** |

> 注：build_gnn_ppt.py/build_gnn_ppt2.py/gnn_pptx.py为实验脚本，函数名过短无文档，未纳入主索引。