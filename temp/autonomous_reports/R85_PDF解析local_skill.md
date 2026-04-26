# R85 | PDF解析local_skill封装

日期: 2026-03-26
类型: 产出
验收: PASS

## 任务目标
封装pdf_reader.py，能从任意PDF提取>=3类结构化信息，接口风格与research_paper_kb_like.py一致。

## 实施过程

### 环境准备
- pdfplumber/pymupdf均未安装 → pip install pdfplumber 0.11.9 安装成功

### 接口设计
参照research_paper_kb_like.py风格（argparse子命令+函数直接调用双模式）：

| 接口 | 功能 | 输出 |
|------|------|------|
| meta(pdf_path) | 元数据：页数/尺寸/作者/标题/创建时间 | pdf_extracts/<stem>/meta.json |
| extract(pdf_path) | 全文文本按页提取 | pdf_extracts/<stem>/text.json |
| tables(pdf_path) | 表格结构化提取 | pdf_extracts/<stem>/tables.json |
| search(pdf_path, kw) | 关键词全文搜索+上下文snippet | 打印结果 |

命令行: `python pdf_reader.py extract/meta/tables/search <pdf> [keyword]`

### 验证结果（QUICK_START.pdf，4页）
- meta: 共4页，612x792pt，Creator=HeadlessChrome，Title=QUICK_START.html ✓
- extract: 4页文本，第1页493字符，text.json已保存 ✓
- tables: 0张表格（该PDF无表格，正常）✓
- search("agent"): 7处命中，snippet含上下文80字符 ✓

坑: FontBBox警告（pdfplumber处理非标准字体时的stderr噪音，不影响结果，不需处理）

## 文件位置
- local_skills/pdf_reader.py (153行)
- local_skills/pdf_extracts/<stem>/（运行时生成）

## 验收状态
PASS：pdf_reader.py存在，能从任意PDF提取>=3类结构化信息（文本/元数据/搜索）
