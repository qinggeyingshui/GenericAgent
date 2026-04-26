# Word文档处理 SOP

## 工具
- `temp/word_toolkit.py`: Word文档操作工具集

## 功能
- 创建/读取/修改Word文档
- 段落/表格/图片操作
- 样式和格式设置

## 使用示例
```python
from word_toolkit import create_word, add_paragraph, add_table, save_word

doc = create_word()
add_paragraph(doc, "标题", style="Heading 1")
add_table(doc, data=[["列1", "列2"], ["数据1", "数据2"]])
save_word(doc, "output.docx")
```

## 注意事项
- 需要python-docx库
- 路径使用绝对路径
- 保存前检查文件是否被占用

[skill_mapping]
category: document_generation
skill: word
tools: word_toolkit.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('word_processing_sop.md')
```
