# ppt_com_toolkit 使用坑点 (L3 SOP)
工具: temp/tools/ppt_com_toolkit.py | 基于win32com+PowerPoint
动画增强: temp/tools/ppt_animation.py | 入场/强调/退出/路径动画
母版管理: temp/tools/ppt_master_toolkit.py | 母版编辑/主题色提取/批量应用

## 母版模块 ppt_master_toolkit.py (R210新增)
```python
from ppt_master_toolkit import *
# 母版编辑
master = get_master(prs, 1)  # 获取母版对象
layouts = get_layouts(prs)   # 获取版式列表 [{"index":1,"name":"标题"}]
set_master_background(prs, 240, 248, 255)  # 设置母版背景色
set_master_gradient(prs, r1,g1,b1, r2,g2,b2)  # 渐变背景
add_master_logo(prs, "logo.png", left=20, top=20, width=80)  # 添加LOGO
add_master_text(prs, "© 2026", left=50, top=510, width=300, height=30)  # 页脚

# 主题色提取
theme = extract_theme_colors(prs)  # {"background1":(r,g,b), "accent1":(r,g,b), ...}
colors = extract_slide_colors(prs, 1)  # 提取幻灯片使用的颜色
save_theme_to_json(theme, "theme.json")  # 保存为JSON

# 批量应用
apply_theme_to_master(prs, theme)  # 应用主题色到母版
batch_apply_master("source.pptx", ["a.pptx","b.pptx"], output_dir="out/")  # 批量应用
copy_master_elements("src.pptx", "tgt.pptx", ["background","theme"])  # 复制元素
```
坑点: 新建PPT需先添加幻灯片才有母版(get_master内部已处理)

## 动画模块 ppt_animation.py (R207新增)
```python
from ppt_animation import *
# 入场动画: add_entrance(slide, shape, effect="fade", trigger="after_prev", delay=0, duration=0.5)
# 强调动画: add_emphasis(slide, shape, effect="pulse", trigger="with_prev", delay=0, duration=0.5, repeat=1)
# 退出动画: add_exit(slide, shape, effect="fade_out", trigger="after_prev", delay=0, duration=0.5)
# 路径动画: add_motion_path(slide, shape, path_type="right", trigger="after_prev", delay=0, duration=1.0)
# 组合动画: add_combo(slide, shape, entrance="fade", emphasis="pulse", exit_effect=None)
# 交错入场: stagger_entrance(slide, shapes, effect="fade", interval=0.3)
# 演示生成: demo_animations(output_path) → 3页演示PPT
```
效果预设: appear/fly_in/fade/zoom/float_up(入场) | pulse/spin/grow_shrink/teeter/wave(强调) | fade_out/fly_out/zoom_out(退出)
触发方式: on_click/with_prev/after_prev

## 函数签名（已验证）
- set_bg_solid(slide, r, g, b)  # RGB分开传，不是tuple
- set_bg_gradient(slide, r1,g1,b1, r2,g2,b2, style=3, variant=1)
- add_text(slide, text, l, t, w, h, sz, bold, italic, color=(tuple), align, font, v_anchor, wrap) → tb
- add_rect(slide, l, t, w, h, fill=(r,g,b), line=None, lw=1) → shape
- add_rrect(slide, l, t, w, h, fill=(r,g,b), radius=0.3) → shape
- add_oval(slide, l, t, w, h, fill=(r,g,b)) → shape
- add_line_shape(slide, x1,y1,x2,y2, color=(r,g,b), weight=1)
- add_table(slide, data, l, t, w, h, head_fill, cell_fill, text_color, sz, font)
- add_anim_appear(slide, shape, delay=0, speed=3)
- set_transition(slide, effect=3845, speed=2)  # 3845=推进,3858=涡流

## 常见坑
1. set_bg_solid传tuple会报TypeError: missing r,g,b → 必须分开传
2. add_shape不存在 → 用add_rect/add_rrect/add_oval
3. add_rect没有line_color参数 → 用line=(r,g,b)或None
4. import前必须sys.path.append('temp目录绝对路径')

## 高级能力（R73新增验证）
- **图片插入**: `slide.Shapes.AddPicture(FileName=绝对路径, LinkToFile=False, SaveWithDocument=True, Left, Top, Width, Height)` → 支持PNG/JPG/BMP/GIF/SVG；Left/Top/Width/Height单位为pt（win32com直接接受，非EMU）
- **SmartArt模拟**: 用`add_rrect+add_text+add_rect(箭头)`组合模拟，比`Shapes.AddSmartArt()`更灵活（后者需msoSmartArtLayout枚举常量）
- **多配色主题**: 预定义配色字典 → `set_bg_solid/set_bg_gradient` + accent色参数化，一键切换
- **母版操作**: `prs.SlideMasters[0]` 访问母版；`master.Shapes.AddPicture(...)` 统一插入LOGO；`prs.SlideMasters[0].Slides[i]` 访问版式；`slide.CustomLayout=layout` 指定版式
- **PIL生成图片**: `Image.new+ImageDraw` 生成测试图；加随机噪点可防PNG过度压缩

## 验证输出
win32com_demo.pptx: 2页36KB，背景/文本/表格/过渡动画均正常
demo_advanced.pptx: 6页1490KB，图片嵌入/SmartArt模拟/多配色/母版说明均正常

## python-pptx 坑点（R74验证）
模板文件: temp/ppt_lab/template_teaching.pptx (5版式/34KB)
- slide.name赋值无效（只读属性），命名需改XML
- 空白版式: prs.slide_layouts[6]
- 形状类型: 1=矩形, 9=椭圆
- 去边框: shape.line.fill.background()，不能直接设line.color
- sfill工具函数: shape.fill.solid(); shape.fill.fore_color.rgb=color; shape.line.fill.background()
- 多段文本: tf.add_paragraph()后add_run()，每段独立设font属性

## 设计规范（源自iSlide专业原则，2026-03-26学习）

### 五大核心原则
1. **对齐** 一页只用一种对齐方式；用参考线+对齐工具；同类元素对齐方式一致
2. **留白** 宁多勿少；段落行距1.2-1.5倍；每页文字≤5-7行，每行≤10字
3. **配色** 主色≤3种；70%主色+25%辅色+5%点缀色；场景推荐：
   - 商务/学术：深蓝+灰+白 或 墨绿+浅灰+白
   - 科技：深灰+亮蓝+白
   - 教育培训：暖橙+米白+深灰
4. **字体** 全篇≤2种字体；封面36-44pt/标题28-32pt/正文20-24pt/注释14-16pt；优先微软雅黑/思源黑体；重点用加粗变色，不用斜体
5. **图文** 能用图不用字，能用表不用图；图片必须高清+风格统一；图标保持线性或面性统一

### 常见误区（必须避免）
- 文字过多：每页提炼关键词，详细内容口头表达
- 字体混乱：全篇≤2种字体
- 配色花哨：主色≤3种，避免大红大绿
- 图片拉伸：缩放时按Shift保持比例
- 动画过度：只用淡入/擦除等简洁动画，或不用

### 图表选用原则
- 折线图→趋势；柱状图→对比；饼图→占比；流程图→步骤；概念图→抽象关系

---

## 智能排版系统（Auto Layout）

**工具**: `temp/tools/ppt_auto_layout.py` | 依赖: python-pptx, ppt_chart_toolkit.py

### 核心功能
提供3种自动布局模式，遵循五大设计原则（对齐/留白/配色/字体/图文）：

#### 1. 图文布局 (Image + Text)
```python
from tools.ppt_auto_layout import add_image_text_layout, new_prs, add_blank_slide, save_prs

prs = new_prs()
slide = add_blank_slide(prs)

# 左图右文布局（图片40%宽度）
add_image_text_layout(
    slide, 
    image_path=r"C:\path\to\image.png",  # 绝对路径
    title="标题文字",
    content="正文内容\n支持换行\n自动调整字号",
    layout="left_image",  # 或 "top_image"（上图下文，图片50%高度）
    margin=0.5  # 边距（英寸）
)

save_prs(prs, "output.pptx")
```

**自动调整规则**：
- 字号：根据行数自动选择 18-22pt（≤5行用22pt，>7行用18pt）
- 行距：1.3倍
- 标题：固定28pt加粗
- 图片：左图右文40%宽度，上图下文50%高度

#### 2. 纯文字布局 (Text Only)
```python
add_text_layout(
    slide,
    title="主标题",
    subtitle="副标题（可选）",  # None则不显示
    content="正文内容\n自动调整字号和行距",
    margin=0.8
)
```

**自动调整规则**：
- 字号：根据内容长度和行数
  - ≤3行且≤100字 → 24pt，行距1.5倍
  - ≤5行且≤200字 → 22pt，行距1.4倍
  - ≤7行且≤300字 → 20pt，行距1.3倍
  - >7行或>300字 → 18pt，行距1.2倍
- 标题：32pt加粗居中
- 副标题：20pt居中

#### 3. 图表布局 (Chart)
```python
add_chart_layout(
    slide,
    title="图表标题",
    chart_data={
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series": {
            "销售额": [100, 150, 120, 180],
            "成本": [60, 80, 70, 90]
        }
    },
    chart_type="COLUMN",  # "COLUMN" | "BAR" | "LINE" | "PIE"
    margin=0.6
)
```

**自动调整规则**：
- 标题：28pt加粗居中，占0.8英寸高度
- 图表：自动占满剩余空间（slide_h - title_h - 2*margin）
- 图表内部标题：不显示（避免重复）

### 使用场景
| 布局模式 | 适用场景 | 图片位置 | 文字占比 |
|---------|---------|---------|---------|
| left_image | 产品介绍/案例展示 | 左侧40% | 右侧60% |
| top_image | 大图展示/封面页 | 上方50% | 下方50% |
| text_only | 纯文字说明/引言 | 无 | 100% |
| chart | 数据分析/趋势展示 | 无 | 图表占满 |

### 设计原则验证
- ✓ **对齐**：所有元素基于margin对齐，标题居中
- ✓ **留白**：边距0.5-0.8英寸，行距1.2-1.5倍
- ✓ **字体**：标题28-32pt，正文18-24pt，自动调整
- ✓ **图文**：图片和文字比例固定（40:60或50:50）
- ✓ **配色**：不涉及（由用户或模板控制）

### 与其他工具的配合
```python
# 混合使用：Marp基础 + 智能排版增强
import subprocess
from pptx import Presentation
from tools.ppt_auto_layout import add_chart_layout

# 1. Marp生成基础框架
subprocess.run(['npx', '@marp-team/marp-cli', 'base.md', '-o', 'base.pptx'])

# 2. 打开并添加图表页
prs = Presentation('base.pptx')
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_chart_layout(slide, "销售数据", chart_data, "COLUMN")
prs.save('final.pptx')
```

### 增强功能（R174, 2026-04-20）

#### 4. 多列布局 (Multi-Column)
```python
from tools.ppt_auto_layout import add_multi_column_layout

# 2列布局
columns_2 = [
    "第一列内容\n• 要点1\n• 要点2",
    "第二列内容\n• 要点A\n• 要点B"
]
add_multi_column_layout(slide, "双列布局", columns_2, num_columns=2)

# 3列布局
columns_3 = ["列1内容", "列2内容", "列3内容"]
add_multi_column_layout(slide, "三列布局", columns_3, num_columns=3)
```

**自动调整规则**：
- 列宽：自动计算 (总宽度 - 列间距) / 列数
- 列间距：0.3英寸
- 字号：根据行数自动选择 16-20pt
- 行距：1.3倍

#### 5. 图文混排 (Mixed Content)
```python
from tools.ppt_auto_layout import add_mixed_content_layout

content_blocks = [
    {"type": "text", "content": "第一段文字说明"},
    {"type": "image", "path": r"C:\path\to\img1.png", "height": 1.5},
    {"type": "text", "content": "第二段文字说明"},
    {"type": "image", "path": r"C:\path\to\img2.png", "height": 1.8}
]
add_mixed_content_layout(slide, "图文混排示例", content_blocks)
```

**自动调整规则**：
- 图片：指定高度，宽度自动占满
- 文字：固定18pt，行距1.3倍
- 间距：每个块之间0.2英寸
- 溢出：超出页面自动截断

#### 6. 响应式布局 (Auto Layout)
```python
from tools.ppt_auto_layout import auto_select_layout

# 自动选择最佳布局
content = {
    "title": "标题",
    "text": "文字内容",
    "images": ["img1.png", "img2.png"],
    "chart_data": {...},
    "columns": ["列1", "列2"]
}
layout_type, shapes = auto_select_layout(slide, content)
print(f"选择的布局：{layout_type}")
```

**决策逻辑**：
1. 有chart_data → 图表布局
2. 有columns(≥2) → 多列布局
3. 有images+text且多图 → 图文混排
4. 有images+text且单图 → 左图右文
5. 仅有images → 上图下文
6. 仅有text → 纯文字布局

**更新的使用场景表**：
| 布局模式 | 适用场景 | 特点 | 验收状态 |
|---------|---------|------|---------|
| left_image | 产品介绍/案例展示 | 左侧40%图，右侧60%文 | ✓ |
| top_image | 大图展示/封面页 | 上方50%图，下方50%文 | ✓ |
| text_only | 纯文字说明/引言 | 100%文字 | ✓ |
| chart | 数据分析/趋势展示 | 图表占满 | ✓ |
| multi_column | 对比说明/并列内容 | 2-3列文字 | ✓ R174 |
| mixed_content | 长文档/教程 | 多图+文字混排 | ✓ R174 |
| auto_layout | 动态内容 | 自动选择最佳布局 | ✓ R174 |

**示例文件**：
- demo_multi_column.pptx - 2列和3列布局示例
- demo_mixed_content.pptx - 图文混排示例
- demo_auto_layout.pptx - 响应式布局示例

---

## 图表生成（R104验证）

### python-pptx 原生图表（推荐）
```python
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
cd = ChartData()
cd.categories = ['A','B','C']
cd.add_series('系列名', (v1, v2, v3))
slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, left, top, w, h, cd)
```
- 支持类型：COLUMN_CLUSTERED/BAR_CLUSTERED/LINE/PIE/AREA等
- 设标题：chart.has_title=True; chart.chart_title.text_frame.text='标题'
- 验证输出：test_chart_pptx.pptx 34572B PASS

### win32com AddChart2（不推荐）
- 坑1：不支持关键字参数，必须位置参数
- 坑2：WithWindow=False时触发COM错误(-2147467259)，需visible窗口
- 结论：改用python-pptx方案

### AutoShape 形状类型ID（win32com AddShape第一参数）
- 1=矩形, 5=圆角矩形, 9=椭圆, 13=三角形, 20=右箭头
- 32=平行四边形, 33=梯形, 60=五边形, 92=流程图:过程
- 完整枚举见 MsoAutoShapeType

## 6. 数据可视化（ppt_data_viz.py, R159）

### 核心函数
```python
import_data_from_excel(file_path, sheet_name=0, header_row=0)
import_data_from_csv(file_path, header_row=0)
create_chart_from_file(slide, file_path, chart_type, l=1, t=1.5, w=8, h=5, title="", **kwargs)
update_chart_from_file(prs, slide_index, chart_index, new_file_path, **kwargs)
```

### 使用示例
```python
from tools.ppt_data_viz import *

# 从CSV创建图表
prs = new_prs()
slide = add_blank_slide(prs)
chart = create_chart_from_file(slide, 'data.csv', 'COLUMN', title='销售数据')
save_prs(prs, 'output.pptx')

# 更新图表数据
from pptx import Presentation
prs = Presentation('output.pptx')
update_chart_from_file(prs, 0, 0, 'new_data.csv')
prs.save('updated.pptx')
```

### 数据格式要求
- Excel/CSV第一行为表头
- 第一列为类别（categories）
- 其余列为系列（series）
- 示例：
  ```
  季度,销售额,成本
  Q1,100,60
  Q2,150,80
  ```

### 注意事项
- 依赖：pandas, openpyxl（Excel）
- 支持图表类型：COLUMN/BAR/LINE/PIE
- 更新图表时保持原有样式和位置

---

## PPT制作技术路线决策树（R113/R114整合）

### 场景1：标准化演示文稿（教案/学术汇报/培训）
**推荐方案**: Marp (Markdown → PPTX)
- **工具**: `temp/lesson_plan_to_marp.py` 或 npx @marp-team/marp-cli
- **优势**: 
  - 学习成本低（Markdown语法）
  - 开发效率高（声明式，~100行代码）
  - 支持LaTeX公式/代码高亮/表格/分栏
  - 主题系统（gaia/default/uncover）+ 自定义CSS
- **适用条件**:
  - 内容结构化（标题/列表/代码/公式）
  - 不需要像素级精确控制
  - 需要快速迭代修改
- **示例**: `npx @marp-team/marp-cli input.md -o output.pptx --allow-local-files`

### 场景2：数据可视化/图表密集型
**推荐方案**: python-pptx
- **工具**: `temp/ppt_chart_toolkit.py`
- **优势**:
  - 原生图表支持（柱状/折线/饼图/面积图）
  - 精确控制图表样式和数据
  - 可编程生成动态内容
- **适用条件**:
  - 需要嵌入matplotlib/seaborn生成的图表
  - 数据驱动的演示文稿
  - 需要批量生成相似结构的PPT
- **示例**:
```python
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
cd = ChartData()
cd.categories = ['Q1','Q2','Q3']
cd.add_series('销售额', (100, 150, 200))
slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, left, top, w, h, cd)
```

### 场景3：复杂定制/企业模板
**推荐方案**: win32com (PowerPoint COM)
- **工具**: `temp/ppt_com_toolkit.py`
- **优势**:
  - 完全访问PowerPoint所有功能
  - 支持母版操作/SmartArt/复杂动画
  - 可操作现有PPTX文件
- **适用条件**:
  - 需要使用企业模板
  - 需要高级动画/过渡效果
  - 需要修改现有PPT
- **限制**: 仅Windows + 已安装PowerPoint

### 场景4：AI辅助生成（商业工具）
**推荐方案**: Gamma AI (Web自动化)
- **工具**: tmwebdriver + web_execute_js
- **优势**:
  - 设计美观（现代化风格）
  - AI生成内容质量高
  - 免费版400额度（每次10张卡片）
  - 支持导出PPTX/PDF
- **适用条件**:
  - 需要快速生成美观PPT
  - 内容创意为主（非数据密集）
  - 可接受Web自动化流程
- **备选**: Canva（模板丰富）/Beautiful.ai（智能布局）

### 混合方案（推荐）
**最佳实践**: Marp基础框架 + python-pptx后处理
1. 用Marp生成标准页面（封面/目录/文字页）
2. 用python-pptx插入图表页
3. 用win32com添加高级动画（可选）

**实施步骤**:
```python
# 1. Marp生成基础PPT
subprocess.run(['npx', '@marp-team/marp-cli', 'base.md', '-o', 'base.pptx'])

# 2. python-pptx打开并添加图表
from pptx import Presentation
prs = Presentation('base.pptx')
slide = prs.slides.add_slide(prs.slide_layouts[5])
# 添加图表...
prs.save('final.pptx')

# 3. win32com添加动画（可选）
import win32com.client
app = win32com.client.Dispatch('PowerPoint.Application')
prs = app.Presentations.Open(os.path.abspath('final.pptx'))
# 添加动画...
prs.Save()
```

---

## 模板管理系统（Template Manager）

**工具**: `temp/ppt_template_manager.py` | 依赖: `ppt_com_toolkit.py`

### 核心功能
```python
import ppt_template_manager as tmgr

# 1. 初始化预定义模板（首次使用）
tmgr.init_templates()  # 创建3个预定义模板到 ./ppt_templates/

# 2. 列出所有可用模板
templates = tmgr.list_templates()
# 返回: [{"id": "business_blue", "name": "商务蓝", "path": "..."}, ...]

# 3. 加载模板配置
template = tmgr.load_template("business_blue")
# 返回: {"name": "商务蓝", "colors": {...}, "fonts": {...}, "bg_style": "..."}

# 4. 保存自定义模板
custom_template = {
    "name": "我的模板",
    "colors": {"primary": [0,51,102], "secondary": [102,102,102], ...},
    "fonts": {"title": {"name": "微软雅黑", "size": 36, "bold": True}, ...},
    "bg_style": "solid"  # 或 "gradient"
}
tmgr.save_template(custom_template, "my_template")

# 5. 应用模板到幻灯片
import ppt_com_toolkit as toolkit
tmgr.apply_bg(slide, template, toolkit)  # 应用背景
tmgr.apply_title(slide, template, toolkit, "标题文字")  # 应用标题样式
tmgr.apply_body(slide, template, toolkit, "正文内容")  # 应用正文样式

# 6. 快速创建页面
tmgr.create_title_slide(slide, template, toolkit, "主标题", "副标题")
tmgr.create_content_slide(slide, template, toolkit, "页面标题", "内容文字")
```

### 预定义模板
| 模板ID | 名称 | 主色 | 背景样式 | 适用场景 |
|--------|------|------|----------|----------|
| business_blue | 商务蓝 | RGB(0,51,102) | 纯色 | 商务/学术报告 |
| tech_gray | 科技灰 | RGB(44,62,80) | 渐变 | 科技/产品发布 |
| education_orange | 教育橙 | RGB(230,126,34) | 纯色 | 教育培训 |

### 模板配置结构
```python
{
    "name": "模板名称",
    "colors": {
        "primary": [R, G, B],      # 主色（标题）
        "secondary": [R, G, B],    # 辅色（副标题）
        "accent": [R, G, B],       # 点缀色
        "bg": [R, G, B],           # 背景色
        "text": [R, G, B]          # 正文色
    },
    "fonts": {
        "title": {"name": "字体名", "size": 36, "bold": True},
        "subtitle": {"name": "字体名", "size": 26, "bold": False},
        "body": {"name": "字体名", "size": 22, "bold": False},
        "note": {"name": "字体名", "size": 16, "bold": False}
    },
    "bg_style": "solid",  # 或 "gradient"
    "gradient": {  # 仅当bg_style="gradient"时需要
        "color1": [R, G, B],
        "color2": [R, G, B],
        "style": 3,    # 1-7，见ppt_com_toolkit
        "variant": 1   # 1-4
    }
}
```

### 使用示例
```python
import win32com.client
import sys
sys.path.append('../temp/tools')
import ppt_com_toolkit as toolkit
import ppt_template_manager as tmgr

# 创建PPT
app = win32com.client.Dispatch('PowerPoint.Application')
prs = app.Presentations.Add()

# 加载模板
template = tmgr.load_template("business_blue")

# 创建标题页
slide1 = prs.Slides.Add(1, 12)
tmgr.create_title_slide(slide1, template, toolkit, "项目汇报", "2026年度总结")

# 创建内容页
slide2 = prs.Slides.Add(2, 12)
tmgr.create_content_slide(slide2, template, toolkit, "核心成果", "完成目标A\n完成目标B")

prs.SaveAs("output.pptx")
```

### 注意事项
- 模板文件存储在 `./ppt_templates/` 目录，JSON格式
- 颜色值使用RGB列表 `[R, G, B]`，范围0-255
- 字体名称需系统已安装（推荐：微软雅黑、宋体、Arial）
- 渐变背景的style参数：1=水平，2=垂直，3=对角，4-7=其他方向
- 位置参数单位：厘米（cm）

---

## 设计规范速查表（iSlide专业原则）

### 配色方案推荐
| 场景 | 主色 | 辅色 | 点缀色 | 背景 |
|------|------|------|--------|------|
| 商务/学术 | 深蓝#003366 | 灰色#666666 | 橙色#FF6B35 | 白色#FFFFFF |
| 科技 | 深灰#2C3E50 | 亮蓝#3498DB | 青色#1ABC9C | 白色#FFFFFF |
| 教育培训 | 暖橙#E67E22 | 米白#ECF0F1 | 深灰#34495E | 浅灰#F8F9FA |
| 医疗健康 | 医疗蓝#4A90E2 | 浅绿#7ED321 | 深灰#4A4A4A | 白色#FFFFFF |

### 字体规范
| 元素 | 字号 | 字体 | 颜色 | 备注 |
|------|------|------|------|------|
| 封面标题 | 36-44pt | 微软雅黑Bold | 主色 | 可用思源黑体 |
| 页面标题 | 28-32pt | 微软雅黑Bold | 主色 | 每页必有 |
| 正文 | 20-24pt | 微软雅黑 | 深灰#333 | 行距1.2-1.5倍 |
| 注释/引用 | 14-16pt | 微软雅黑 | 灰色#666 | 右下角或底部 |

### 留白原则
- 页边距：≥0.5英寸（36pt）
- 标题与正文间距：≥0.3英寸（22pt）
- 每页文字：≤5-7行
- 每行文字：≤10字（中文）/15词（英文）

### 图表选型决策
```
数据类型 → 图表类型
├─ 时间序列 → 折线图
├─ 类别对比 → 柱状图（≤7类）/条形图（>7类）
├─ 占比关系 → 饼图（≤5类）/环形图
├─ 相关性 → 散点图
├─ 层级关系 → 树状图/旭日图
└─ 流程步骤 → 流程图/时间轴
```

### 动画使用原则
- **推荐**: 淡入(Fade)/擦除(Wipe)/推进(Push)
- **避免**: 旋转/弹跳/飞入等花哨效果
- **时长**: 0.3-0.5秒（快速）/0.5-1秒（标准）
- **触发**: 统一使用"单击"或"与上一动画同时"
- **原则**: 能不用就不用，用则统一风格

---

## 常见问题排查

### Marp相关
**Q**: PPTX中公式显示为图片？  
**A**: 正常现象，Marp将LaTeX渲染为SVG后嵌入

**Q**: 中文字体显示异常？  
**A**: 在style中指定字体：`section { font-family: "Microsoft YaHei"; }`

**Q**: 背景图片不显示？  
**A**: 检查路径是否正确，使用`--allow-local-files`参数

### python-pptx相关
**Q**: 图表数据更新后不刷新？  
**A**: 需要重新创建ChartData对象并替换

**Q**: 中文显示为方框？  
**A**: 设置字体：`run.font.name = '微软雅黑'`

### win32com相关
**Q**: COM错误-2147467259？  
**A**: PowerPoint需要可见窗口，设置`app.Visible = True`

**Q**: 保存后文件损坏？  
**A**: 确保调用`prs.Save()`而非`SaveAs()`，路径使用绝对路径

---

## 模板管理系统

### 功能概述
`temp/ppt_template_manager.py` 提供统一的模板管理接口，支持保存/加载/应用自定义配色和字体方案。

### 预定义模板
| 模板ID | 名称 | 主色调 | 适用场景 | 背景样式 |
|--------|------|--------|----------|----------|
| business_blue | 商务蓝 | 深蓝#003366 | 商务汇报/学术演讲 | 纯色 |
| tech_gray | 科技灰 | 深灰#2C3E50 | 科技产品/技术分享 | 渐变 |
| education_orange | 教育橙 | 暖橙#E67E22 | 教育培训/课程讲义 | 纯色 |

### 核心函数
```python
import ppt_template_manager as tmpl

# 初始化预定义模板
tmpl.init_templates()

# 加载模板
template = tmpl.load_template("business_blue")

# 应用到幻灯片
tmpl.create_title_slide(slide, template, ppt, "标题", "副标题")
tmpl.create_content_slide(slide, template, ppt, "页面标题", "正文内容")

# 自定义模板
custom = {
    "name": "我的模板",
    "colors": {"primary": [R,G,B], "bg": [R,G,B], ...},
    "fonts": {"title": {"name": "微软雅黑", "size": 32, "bold": True}, ...},
    "bg_style": "solid"  # or "gradient"
}
tmpl.save_template(custom, "my_template")
```

### 模板结构
```json
{
  "name": "模板名称",
  "colors": {
    "primary": [R, G, B],    // 主色（标题）
    "secondary": [R, G, B],  // 辅色（副标题）
    "accent": [R, G, B],     // 点缀色
    "bg": [R, G, B],         // 背景色
    "text": [R, G, B]        // 正文色
  },
  "fonts": {
    "title": {"name": "字体", "size": 32, "bold": true},
    "subtitle": {"name": "字体", "size": 24, "bold": false},
    "body": {"name": "字体", "size": 20, "bold": false},
    "note": {"name": "字体", "size": 14, "bold": false}
  },
  "bg_style": "solid",  // "solid" 或 "gradient"
  "gradient": {         // 仅当bg_style="gradient"时需要
    "color1": [R, G, B],
    "color2": [R, G, B],
    "style": 3,         // 1=水平, 2=垂直, 3=对角线
    "variant": 1
  }
}
```

### 使用示例
```python
import sys
sys.path.append('./tools')
import ppt_com_toolkit as ppt
import ppt_template_manager as tmpl

# 创建PPT
app = ppt.open_ppt()
prs = ppt.new_prs(app)

# 应用商务蓝模板
template = tmpl.load_template("business_blue")
slide1 = ppt.add_slide(prs)
tmpl.create_title_slide(slide1, template, ppt, "年度总结", "2026财年")

slide2 = ppt.add_slide(prs)
tmpl.create_content_slide(slide2, template, ppt, "核心数据", "• 营收增长25%\n• 用户突破100万")

ppt.save_and_quit(app, prs, "output.pptx")
```

### 验收输出
- `temp/ppt_templates/` - 模板配置文件目录（JSON格式）
- `temp/ppt_lab/template_demo.pptx` - 3个模板演示（6页/42KB）

---

## 工具文件索引
- `temp/lesson_plan_to_marp.py` - Markdown→PPTX转换器（Marp封装）
- `temp/ppt_com_toolkit.py` - win32com封装（背景/文本/表格/动画）
- `temp/ppt_chart_toolkit.py` - python-pptx图表封装（4种类型）
- `temp/ppt_template_manager.py` - 模板管理系统（保存/加载/应用）
- `temp/tools/speech_helper.py` - 演讲稿生成与排练助手（R195新增）
- `temp/ppt_lab/template_teaching.pptx` - 教学模板（5版式）

## 8. 演讲稿生成与排练助手 (R195)

**工具**: `temp/tools/speech_helper.py`

### 8.1 核心功能

#### SpeechGenerator - 演讲稿生成
从PPT自动生成演讲稿，支持自定义风格。

```python
import sys
sys.path.append('./tools')
import speech_helper

gen = speech_helper.SpeechGenerator()
slides = gen.extract_content_from_ppt("demo.pptx")
speech = gen.generate_speech(slides)
optimization = gen.optimize_speech(speech)
```

#### RehearsalTimer - 排练计时器
支持暂停/继续，实时显示进度。

```python
timer = speech_helper.RehearsalTimer(target_minutes=10)
timer.start()
# 演讲中...
timer.pause()  # 暂停
timer.resume()  # 继续
print(timer.get_status())
```

#### KeyPointHelper - 关键点提示
提取PPT关键点，生成演讲提示卡。

```python
helper = speech_helper.KeyPointHelper()
key_points = helper.extract_key_points(slides)
helper.save_prompts(key_points, "prompts.txt")
```

### 8.2 快速使用

```python
# 一键生成演讲稿
speech = speech_helper.quick_generate_speech("demo.pptx", "speech.txt")

# 一键开始排练
timer = speech_helper.quick_rehearsal(target_minutes=15)
```

### 8.3 演讲稿优化建议
- 字数统计和时长估算
- 句子长度分析
- 内容丰富度评估

---

## R204 智能排版增强 (2026-04-21)

### 新增布局模式

#### 6. 时间线布局 (Timeline)
```python
from tools.ppt_auto_layout import add_timeline_layout

timeline = [
    {"time": "2020", "event": "项目启动"},
    {"time": "2021", "event": "产品发布"},
    {"time": "2022", "event": "市场扩张"}
]
add_timeline_layout(slide, "发展历程", timeline)
```

#### 7. 对比布局 (Comparison)
```python
from tools.ppt_auto_layout import add_comparison_layout

comparison = {
    "left": {"title": "方案A", "points": ["优点1", "优点2"]},
    "right": {"title": "方案B", "points": ["优点1", "优点2"]}
}
add_comparison_layout(slide, "方案对比", comparison)
```

### 智能功能

#### 内容类型识别
```python
from tools.ppt_auto_layout import detect_content_type

content_type = detect_content_type(text, has_images, has_chart)
# 返回: "text_only" | "image_text" | "chart" | "timeline" | "comparison"
```

#### 美观度评分
```python
from tools.ppt_auto_layout import calc_beauty_score

score = calc_beauty_score(slide, layout_type)
# 返回: 0-100分，评估对齐/留白/字体/图文比例
```

#### 智能布局选择
```python
from tools.ppt_auto_layout import smart_layout

# 自动识别内容类型并选择最佳布局
smart_layout(slide, title, content, images=None, chart_data=None)
```

### 现在支持的布局模式（共7种）
1. 图文布局 (left_image/top_image)
2. 纯文字布局 (text_only)
3. 图表布局 (chart)
4. 多列布局 (multi_column)
5. 图文混排 (mixed_content)
6. 时间线布局 (timeline) - R204新增
7. 对比布局 (comparison) - R204新增

---

## PPT导出功能 (R216新增)

```python
from tools.ppt_export_toolkit import export_to_pdf, export_to_images, export_to_video, export_to_html

# 导出PDF
export_to_pdf("demo.pptx", "output.pdf")

# 导出图片(每页一张PNG)
export_to_images("demo.pptx", "slides_dir", format="PNG")

# 导出视频(MP4)
export_to_video("demo.pptx", "output.mp4", duration_per_slide=3)

# 导出HTML(网页浏览)
export_to_html("demo.pptx", "output.html")
```

**最后更新**: 2026-04-24 (R216导出功能增强)

---
[skill_mapping]
category: document_generation
skill: ppt_creation
tools: ppt_com_toolkit.py, ppt_chart_toolkit.py, ppt_template_manager.py, ppt_auto_layout.py, ppt_export_toolkit.py, speech_helper.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('ppt_com_sop.md')
```
