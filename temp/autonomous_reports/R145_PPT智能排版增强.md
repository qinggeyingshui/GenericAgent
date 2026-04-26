# R145: PPT智能排版增强

## 任务目标
为PPT制作提供智能排版能力，支持3种布局模式，自动调整字号和间距。

## 产出文件
- **ppt_auto_layout.py** (7517 bytes)
  - 位置: temp/tools/ppt_auto_layout.py
  - 依赖: python-pptx, ppt_chart_toolkit.py

## 核心功能

### 1. 图文布局 (add_image_text_layout)
- **左图右文**: 图片40%宽度，文字60%
- **上图下文**: 图片50%高度，文字50%
- **自动调整**: 根据行数选择18-22pt字号，行距1.3倍
- **参数**: image_path, title, content, layout, margin

### 2. 纯文字布局 (add_text_layout)
- **智能字号**: 
  - ≤3行且≤100字 → 24pt，行距1.5倍
  - ≤5行且≤200字 → 22pt，行距1.4倍
  - ≤7行且≤300字 → 20pt，行距1.3倍
  - >7行或>300字 → 18pt，行距1.2倍
- **标题**: 32pt加粗居中
- **副标题**: 20pt居中（可选）
- **参数**: title, content, subtitle, margin

### 3. 图表布局 (add_chart_layout)
- **自动占满**: 图表占满剩余空间（slide_h - title_h - 2*margin）
- **标题**: 28pt加粗居中，占0.8英寸高度
- **图表类型**: COLUMN | BAR | LINE | PIE
- **参数**: title, chart_data, chart_type, margin

## 设计原则验证
- ✓ **对齐**: 所有元素基于margin对齐，标题居中
- ✓ **留白**: 边距0.5-0.8英寸，行距1.2-1.5倍
- ✓ **字体**: 标题28-32pt，正文18-24pt，自动调整
- ✓ **图文**: 图片和文字比例固定（40:60或50:50）

## 测试验证
- **测试文件**: test_auto_layout.pptx (38.8 KB)
- **测试页面**: 4页
  1. 图文布局（左图右文）- 图片40%宽度
  2. 图文布局（上图下文）- 图片50%高度
  3. 纯文字布局 - 5行内容自动选择22pt字号
  4. 图表布局 - 柱状图自动占满空间
- **验收标准**: ✓ 全部通过

## SOP更新
- **文件**: ../memory/ppt_com_sop.md
- **位置**: 第64行后插入"智能排版系统"章节
- **内容**: 3种布局的使用方法、自动调整规则、使用场景对比表

## 技术亮点
1. **自适应字号**: 根据内容长度和行数自动选择最佳字号
2. **比例固定**: 图文布局使用固定比例（40:60或50:50），避免手动调整
3. **遵循规范**: 严格遵循ppt_com_sop五大设计原则
4. **易于集成**: 可与Marp、python-pptx、win32com混合使用

## 使用示例
```python
from tools.ppt_auto_layout import *

prs = new_prs()
slide = add_blank_slide(prs)

# 图文布局
add_image_text_layout(slide, "image.png", "标题", "内容", "left_image")

# 纯文字布局
add_text_layout(slide, "标题", "内容", subtitle="副标题")

# 图表布局
add_chart_layout(slide, "标题", chart_data, "COLUMN")

save_prs(prs, "output.pptx")
```

## 后续优化方向
1. 支持更多布局模式（左右分栏、网格布局）
2. 集成配色方案（从ppt_template_manager读取）
3. 支持批量生成（从数据源自动生成多页）
