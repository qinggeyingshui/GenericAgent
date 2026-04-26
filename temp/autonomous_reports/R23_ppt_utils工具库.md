# R23 — PPT生成工具函数库 `ppt_utils.py`

## 任务目标
封装 `ppt_lab/ppt_utils.py`，提供 ≥6 个可复用的幻灯片生成函数，支持配色方案动态切换，并附带调用示例脚本。

## 产出文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `ppt_lab/ppt_utils.py` | 19,433 B | 工具函数库主文件 |
| `ppt_lab/ppt_demo.py` | 1,876 B | 示例脚本（演示全部8个函数） |
| `ppt_lab/demo_output.pptx` | 39,571 B | 示例输出（8页，含配色切换） |

## 架构设计

### 核心类

- **`ColorScheme`** — 从 `design_tokens.json` 解析配色方案，提供 `primary/secondary/accent1~3/highlight/text_dark/text_light/bg_main/bg_card` 等颜色属性及字体信息
- **`PPTBuilder`** — PPT生成器，管理 `Presentation` 对象，支持 `switch_scheme()` 随时切换配色

### 8 个幻灯片函数（✅ 超额完成，要求 ≥6）

| # | 方法名 | 功能 | 特色 |
|---|--------|------|------|
| 1 | `add_title_slide()` | 封面页 | 左侧色块 + 右侧标题 + 分隔线 |
| 2 | `add_section_slide()` | 章节过渡页 | 大号编号 + 装饰圆形 |
| 3 | `add_content_slide()` | 要点列表页 | 支持条目高亮（`highlight_indices`） |
| 4 | `add_image_content_slide()` | 图文混排页 | 文字/图片左右可切换 |
| 5 | `add_comparison_slide()` | 双栏对比页 | 左右独立标题栏 + 列表 |
| 6 | `add_timeline_slide()` | 时间轴页 | 水平线 + 交替上下标签 |
| 7 | `add_ending_slide()` | 结尾致谢页 | 装饰圆形 + 大号文字 |
| 8 | `add_toc_slide()` | 目录页 | 编号圆形 + 当前章节高亮 |

### 配色切换验证

示例脚本中前5页使用 `academic_blue`，后3页切换为 `morandi_warm`，验证了 `switch_scheme()` 的中途切换能力。

## 关键设计决策

1. **基于空白布局**：使用 `slide_layouts[6]`（空白），所有元素纯代码绘制，避免模板兼容性问题
2. **tokens 驱动**：颜色、字体、间距全部从 `design_tokens.json` 读取，修改 JSON 即可全局换肤
3. **图片容错**：`add_image_content_slide()` 在图片文件不存在时自动显示占位框
4. **链式调用**：每个 `add_*` 方法返回 `slide` 对象，方便后续追加自定义元素

## 验收结果

- [x] ≥6 个可复用函数（实际 8 个）
- [x] 配色方案切换（`switch_scheme("morandi_warm")`）
- [x] 调用示例脚本（`ppt_demo.py`，8页完整演示）
- [x] PPTX 输出有效（39,571 bytes，8 slides）