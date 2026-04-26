# R26 — Markdown → PPT 端到端 Pipeline

**日期**: 2025-07-11 | **类型**: 产出 | **状态**: 完成

## 目标

构建端到端 Pipeline：输入 Markdown 大纲文件，自动输出 ≥8 页带视觉设计的学术 PPT (.pptx)。

## 产出物

| 文件 | 大小 | 说明 |
|------|------|------|
| `ppt_lab/md2ppt.py` | ~9.6KB | Pipeline 核心：Markdown 解析 + PPT 生成 + CLI |
| `ppt_lab/sample_outline.md` | 1.2KB | 示例大纲（GNN 推荐系统主题） |
| `ppt_lab/gnn_recommender.pptx` | 56KB | 生成结果：**19 页**学术 PPT |

## 架构设计

```
sample_outline.md ──→ parse_frontmatter() ──→ parse_slides() ──→ generate_ppt() ──→ .pptx
                      (YAML元数据)           (结构化slide列表)    (调用PPTBuilder)
```

### Markdown 语法映射

| Markdown 语法 | 幻灯片类型 | PPTBuilder 方法 |
|---------------|-----------|----------------|
| `# 章节名` | 章节过渡页 + TOC | `add_section_slide()` + `add_toc_slide()` |
| `## 标题` + 列表 | 内容页 | `add_content_slide()` |
| `## [对比] 标题` + H3 双栏 | 对比页 | `add_comparison_slide()` |
| `## [时间线] 标题` + `年份\|事件` | 时间轴页 | `add_timeline_slide()` |
| `## [图文] 标题 \| 图片` | 图文页 | `add_image_content_slide()` |
| `## [致谢]` | 结尾页 | `add_ending_slide()` |
| `- **加粗条目**` | 高亮要点 | highlights 参数 |

### 生成结果统计（19 页）

- 标题页: 1
- 章节过渡页: 4（含自动 TOC）
- 内容页: 4
- 对比页: 2
- 时间线页: 1
- 图文页: 1
- 致谢页: 1
- TOC 页: 4（每章节前自动插入）

## 修复记录

| 问题 | 原因 | 修复 |
|------|------|------|
| GBK 编码错误 | `ppt_utils.py` save() 中含 ✅ emoji | 替换为 ASCII `[OK]` |
| 输出到 `-o` 文件 | CLI 用 `sys.argv[2]` 取位置参数 | 改用 `argparse` 支持 `-o` flag |

## CLI 用法

```bash
python ppt_lab/md2ppt.py input.md -o output.pptx
python ppt_lab/md2ppt.py input.md              # 默认输出 input.pptx
```

## 验收

- [x] 输入 Markdown 大纲 → 自动输出 .pptx
- [x] ≥ 8 页（实际 19 页）
- [x] 带视觉设计（配色方案、渐变背景、装饰元素）
- [x] 覆盖全部 6 种幻灯片类型