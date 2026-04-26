# R74 | python-pptx 高级教学模板制作

**日期**: 2026-03-26  
**类型**: 产出  
**状态**: 验收通过

## 任务目标

基于 python-pptx 制作可复用教学 PPT 母版模板，含封面/目录/内容/总结 4 种版式。

## 产出

- **文件**: `./ppt_lab/template_teaching.pptx`
- **大小**: 35719 bytes (34 KB)
- **幻灯片数**: 5 页（5 种版式示例）
- **验收**: PASS（>=4 个自定义版式）

## 5 种版式设计

### 版式1：封面 (Cover)
- 深色背景(#111827) + 左侧蓝色竖条装饰
- 右上角大圆形装饰元素
- 课程标签(青绿) + 主标题(白色 48pt) + 副标题 + 底部横线 + 机构信息

### 版式2：目录 (Table of Contents)
- 左侧深色面板(4.5英寸) + 右侧白色内容区
- 大字"目录/CONTENTS" + 5条带编号的目录条目
- 分隔线区分各条目

### 版式3：内容 (Content)
- 顶部主色条 + 章节标签 + 幻灯片标题
- 左侧4个要点(圆形编号+标题+描述)
- 右侧浅灰信息卡片(核心公式展示区)
- 底部页码

### 版式4：总结 (Summary)
- 深色渐变背景
- 顶部青绿装饰条 + 居中大标题
- 3 列卡片(核心概念/关键技术/应用场景)，各卡片顶色条区分

### 版式5：节标题 (Section Title)
- 左侧主色面板(6英寸) + 右侧白色
- 节编号 + 大标题 + 青绿分隔线 + 英文副标题
- 右侧本节简介文字

## 技术要点

```python
# 关键模式
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# 填充形状
def sfill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()  # 去掉边框

# 多段文本
p2 = tf.add_paragraph()
r2 = p2.add_run()
r2.text = '第二行'
r2.font.size = Pt(16)
```

## 坑与注意事项

1. `slide.name` 赋值在 python-pptx 中对 Slide 对象无效（name 属性只读），命名只能通过 XML 修改
2. 使用 `blank_layout = prs.slide_layouts[6]` 获取空白版式
3. 形状 shape_type=1(矩形) / 9(椭圆)
4. 去边框必须用 `shape.line.fill.background()`，不能直接设 `line.color`

## 记忆更新建议

建议在 `ppt_com_sop.md` 的 python-pptx 章节补充：
- 5种版式代码片段路径: `temp/ppt_lab/template_teaching.pptx`
- slide.name 赋值无效坑
- sfill() 工具函数模式