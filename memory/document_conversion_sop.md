# 文档格式转换 SOP

## 工具
- `temp/pdf2kb.py`: PDF转知识库
- pandoc: 通用文档转换（需安装）

## 功能
- PDF → Markdown/Text
- Word → PDF
- Markdown → HTML/PDF
- 格式批量转换

## 使用示例
```python
# PDF转Markdown
from pdf2kb import pdf_to_markdown
md_content = pdf_to_markdown("input.pdf")

# 使用pandoc（需安装）
import subprocess
subprocess.run(["pandoc", "input.md", "-o", "output.pdf"])
```

## 注意事项
- PDF转换质量取决于原文档结构
- pandoc需单独安装
- 大文件转换耗时较长

[skill_mapping]
category: document_generation
skill: document_conversion
tools: pdf2kb.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('document_conversion_sop.md')
```
