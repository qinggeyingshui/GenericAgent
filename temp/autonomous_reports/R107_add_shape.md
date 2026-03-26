# R107 — ppt_com_toolkit.py add_shape() 通用AutoShape封装

**日期**: 2026-03-26
**类型**: 产出
**状态**: 完成

## 任务目标
在 ppt_com_toolkit.py 中封装 add_shape() 通用 AutoShape 函数，覆盖三角形/右箭头/五角星/菱形/流程框/标注等类型，支持形状内文字。

## 产出

| 文件 | 变化 |
|------|------|
| `temp/ppt_com_toolkit.py` | 追加 add_shape() + SHAPE_* 常量，255→371行 |
| `temp/ppt_lab/test_shapes.pptx` | 38KB，6种形状验证通过 |

## API 设计

    add_shape(slide, shape_type, l, t, w, h,
              fill, line_color, line_width,
              text, text_sz, text_bold, text_color, text_align, font)

    SHAPE_TRIANGLE=13, SHAPE_RIGHT_ARROW=20, SHAPE_STAR5=12
    SHAPE_DIAMOND=4, SHAPE_FLOWCHART=109, SHAPE_CALLOUT=100
    SHAPE_PENTAGON=56, SHAPE_PARALLELOGRAM=25

## 验证结果
- 等腰三角形(13)、右箭头(20)、五角星(12)、菱形(4)、流程图过程框(109)、矩形标注(100)
- 全部含文字标签，颜色各异
- test_shapes.pptx 38KB，验收 PASS

## 设计决策
- 复用已有 shape_text() 处理形状内文字，避免重复代码
- SHAPE_* 常量与 add_shape() 一起追加，调用无需记忆MsoAutoShapeType数字
- 使用 win32com（非 python-pptx），与 ppt_com_toolkit 体系一致
