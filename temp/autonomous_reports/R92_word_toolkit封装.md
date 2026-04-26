# R92 | word_toolkit.py 封装

日期: 2026-03-26
类型: 产出
验收: PASS

## 目标
基于 win32com 封装 Word 文档操作工具库，接口风格与 ppt_com_toolkit.py 一致。

## 产出
- 文件: temp/word_toolkit.py（198行）
- 验收文件: temp/test_word_output.docx（14,227B）

## 函数清单（共11个）

| 函数 | 功能 | 参数 |
|---|---|---|
| open_word(visible) | 启动Word COM应用 | visible=False |
| new_doc(app) | 新建空白文档 | app |
| open_doc(app, path) | 打开已有docx | app, path |
| save_and_quit(app, doc, path) | 保存并退出 | app, doc, path |
| save_doc(doc, path) | 仅保存不退出 | doc, path |
| add_heading(doc, text, level) | 插入标题(1-3级) | doc, text, level=1 |
| add_paragraph(doc, text, ...) | 插入正文段落 | bold/italic/sz/align/color |
| add_bullet_list(doc, items) | 插入项目符号列表 | doc, items, sz, indent_cm |
| add_page_break(doc) | 插入分页符 | doc |
| add_table(doc, data, ...) | 插入表格 | header_bold=True, border=True |
| add_picture(doc, path, ...) | 插入图片 | width_cm/height_cm |
| set_page_margin(doc, ...) | 设置页边距(cm) | top/bottom/left/right |
| build_report(output_path, title, sections, table_data) | 一键生成报告型文档 | 快捷组合函数 |

## 验收结果
- word_toolkit.py 存在: YES
- build_report() 生成 test_word_output.docx: YES (14,227B)
- 文档含标题+正文段落+数据表格: YES
- Word COM 启动/保存/退出正常: YES

## 接口风格对比
| 特性 | ppt_com_toolkit | word_toolkit |
|---|---|---|
| COM启动 | open_ppt() | open_word() |
| 新建文件 | new_prs(app) | new_doc(app) |
| 保存退出 | save_and_quit() | save_and_quit() |
| 快捷函数 | 无 | build_report() |

## 后续扩展建议
- add_toc(): 自动生成目录
- set_font_default(): 设置全局字体
- add_numbered_list(): 有序列表
- export_pdf(): 另存为PDF
