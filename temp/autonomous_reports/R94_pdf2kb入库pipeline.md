# R94 | PDF→GNN论文库自动入库pipeline

日期: 2026-03-26
类型: 产出
验收: PASS

## 产出
- 文件: temp/pdf2kb.py（133行）
- 接口: process_pdf(path, dry_run) / process_dir(dir, dry_run)
- 依赖: local_skills/pdf_reader.py + research_paper_kb_like.py + pdfplumber

## 功能
- 从PDF首页提取标题（启发式，首非空行）
- 从前3页提取年份（最早4位年份数字）
- 提取Abstract段落（正则匹配）
- 防重复：按文件名stem生成ID，已存在则跳过
- --dry模式：预览不写入
- 批量：传目录自动处理所有.pdf

## 环境
- venv python: .venv/Scripts/python.exe
- pdfplumber: 0.11.9（已在venv中安装）
- FontBBox警告为pdfplumber已知警告，不影响文本提取

## 验收
- pdf2kb.py存在: YES
- dry-run QUICK_START.pdf 成功提取元数据: YES
- 正式add()入库PAPERS.md更新: YES
