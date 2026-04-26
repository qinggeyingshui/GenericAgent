# R25 — GitHub 高星 PPT 自动生成项目调研

> **任务**: TODO#4 — 搜索 GitHub 上高星 PPT/演示文稿自动生成项目，提炼可借鉴技术  
> **日期**: 2025-03-25  
> **方法**: GitHub REST API 搜索 + README 分析（浏览器 TM 驱动不可用，改用 API）

---

## 一、项目全景（按 Star 数排序）

| # | 项目 | ★ Stars | 语言 | 输出格式 | 核心定位 | License |
|---|-------|---------|------|----------|----------|---------|
| 1 | [reveal.js](https://github.com/hakimel/reveal.js) | 70,850 | JavaScript | HTML/Web | HTML 演示框架鼻祖 | MIT |
| 2 | [Slidev](https://github.com/slidevjs/slidev) | 45,114 | TypeScript | Web/PDF/PPTX | 面向开发者的 Markdown 幻灯片 | MIT |
| 3 | [mdx-deck](https://github.com/jxnblk/mdx-deck) | 11,483 | JavaScript | Web | React MDX 演示文稿 | MIT |
| 4 | [slides](https://github.com/maaslalani/slides) | 11,353 | Go | 终端 | 终端内 Markdown 演示 | MIT |
| 5 | [Marp](https://github.com/marp-team/marp) | 10,708 | TypeScript | HTML/PDF/PPTX | Markdown 演示生态系统 | MIT |
| 6 | [nodeppt](https://github.com/ksky521/nodeppt) | 10,377 | JavaScript | Web | Web 演示工具 | MIT |
| 7 | [md2pptx](https://github.com/MartinPacker/md2pptx) | 485 | Python | **PPTX** | Markdown→PowerPoint 转换器 | MIT |
| 8 | [Text-to-PPT](https://github.com/AIAnytime/Text-to-PPT-Generation-Streamlit-App) | 36 | Python | **PPTX** | GPT + python-pptx 生成 | — |
| 9 | [PPT_Generate](https://github.com/CY202227/PPT_Generate) | 6 | Python | **PPTX** | AI + MCP Server 生成 | — |

---

## 二、重点项目深度对比（≥3 个）

### 对比表 1：架构与技术栈

| 维度 | Slidev (45k★) | Marp (10.7k★) | md2pptx (485★) | Text-to-PPT (36★) |
|------|---------------|---------------|-----------------|-------------------|
| **输入** | Markdown + Vue 组件 | 纯 Markdown + 指令 | 纯 Markdown | 自然语言文本 |
| **输出** | Web / PDF / PPTX导出 | HTML / PDF / PPTX | PPTX | PPTX |
| **核心引擎** | Vite + Vue 3 + UnoCSS | Marpit (自研MD解析) | python-pptx | GPT API + python-pptx |
| **主题系统** | npm 主题包 + UnoCSS | CSS 主题 + 指令覆盖 | 内联元数据控制 | 无 |
| **插件机制** | Vite 插件 + Vue 组件 | Marpit 插件链 | 无 | 无 |
| **社区规模** | Forks 1,973 | Forks 236 | Forks 74 | 极小 |
| **与我们的相关性** | ⭐⭐⭐ 主题/布局系统 | ⭐⭐⭐ Markdown指令 | ⭐⭐⭐⭐ 直接PPTX生成 | ⭐⭐⭐⭐ AI+PPTX流程 |

### 对比表 2：内容组织与分页策略

| 维度 | Slidev | Marp | md2pptx | reveal.js |
|------|--------|------|---------|-----------|
| **分页符** | `---` 三横线 | `---` 三横线 | `---` + 标题自动分页 | `<section>` 标签 |
| **布局声明** | YAML frontmatter `layout: two-cols` | Marp 指令 `<!-- class: lead -->` | Markdown 语义推断 | HTML class |
| **元数据** | 每页 YAML frontmatter | 全局/局部指令 | 文件头元数据块 | data-* 属性 |
| **多列支持** | `::left::` `::right::` 插槽 | CSS Grid/Flexbox | 表格语法映射 | CSS 自定义 |
| **演讲者备注** | `<!-- 备注内容 -->` | `<!-- 备注 -->` | 不支持 | `<aside class="notes">` |

### 对比表 3：与我们项目 (ppt_utils) 的技术契合度

| 维度 | 我们的 ppt_utils | 可借鉴来源 | 借鉴方向 |
|------|-----------------|-----------|---------|
| **模板系统** | Design Token + 模板函数 | Slidev 布局系统 | 将布局声明为独立可组合单元 |
| **PPTX 生成** | python-pptx 直接操作 | md2pptx | Markdown→PPTX 的映射规则 |
| **AI 集成** | 尚未实现 | Text-to-PPT / PPT_Generate | LLM 输出结构化 JSON → 模板映射 |
| **主题切换** | design_tokens 字典 | Marp CSS 主题 | 主题热切换 + 指令覆盖机制 |
| **内容输入** | Python 函数参数 | Slidev/Marp Markdown | 支持 Markdown 输入层 |

---

## 三、可借鉴设计模式（≥2 个）

### 模式 1：📐 Markdown-as-Source + Pipeline Transform（管道转换）

**来源**: Slidev、Marp、md2pptx 共同采用

**核心思想**:

    Markdown 源文件 → 解析器 → AST/中间表示 → 渲染器 → 目标格式(Web/PDF/PPTX)

**关键设计**:
- **分页约定**: 用 `---` 分隔符切分页面，零学习成本
- **指令注入**: 通过 YAML frontmatter 或 HTML 注释注入布局/样式指令
- **中间表示**: Marp 的 Marpit 引擎将 Markdown 解析为带有指令标注的 token 流，再由不同后端渲染

**对我们的价值**:
- 可为 `ppt_utils` 增加 **Markdown 输入层**：用户写 Markdown → 解析为结构化 dict → 调用现有模板函数生成 PPTX
- 分页符 `---` + YAML frontmatter 的约定可直接复用
- 示例流程：

      用户 Markdown → parse_md_to_slides(md_text) → [{"layout": "title", ...}, ...] → 逐页调用 ppt_utils 模板

---

### 模式 2：🎨 Theme + Layout 可组合生态系统

**来源**: Slidev（最成熟）、Marp

**核心思想**:

    主题(Theme) = 颜色/字体/间距定义
    布局(Layout) = 页面结构模板（标题页/双栏/图文等）
    最终页面 = Theme × Layout × Content

**关键设计**:
- **Slidev**: 主题是 npm 包，包含多个 Vue 布局组件 + 全局样式；用户在 frontmatter 中声明 `layout: two-cols`
- **Marp**: 主题是 CSS 文件，通过 `<!-- class: invert -->` 指令切换变体
- **解耦**: 主题和布局正交——同一布局在不同主题下呈现不同视觉效果

**对我们的价值**:
- 当前 `ppt_utils` 的 `design_tokens` 已实现了主题层，但**布局层尚未独立抽象**
- 可借鉴 Slidev 将布局注册为命名模板：

      LAYOUTS = {
          "title": create_title_slide,
          "content": create_content_slide,
          "two-cols": create_two_column_slide,
          "image-right": create_image_right_slide,
      }

- 用户只需声明 `{"layout": "two-cols", "left": [...], "right": [...]}` 即可

---

### 模式 3（附加）：🤖 LLM → Structured JSON → Template Mapping

**来源**: Text-to-PPT、PPT_Generate

**核心思想**:

    用户自然语言 → LLM 生成结构化 JSON → 模板引擎映射 → PPTX 输出

**关键设计**:
- **Text-to-PPT**: GPT 生成每页标题+要点列表 → python-pptx 逐页渲染
- **PPT_Generate**: 已转为 MCP Server，AI Agent 通过工具调用生成 PPT
- **核心约束**: LLM 输出必须符合预定义 schema（JSON），否则模板映射失败

**对我们的价值**:
- 与模式 1 结合：LLM 输出 Markdown（而非 JSON），降低 prompt 复杂度
- 或直接输出 slide schema JSON，与我们的布局注册表对接
- PPT_Generate 的 MCP 模式值得关注——未来可将 `ppt_utils` 封装为 MCP 工具

---

## 四、关键发现与建议

### 发现
1. **高星项目多为 Web 演示**（reveal.js/Slidev/mdx-deck），真正生成 PPTX 的项目较少且星数低
2. **Markdown 是事实标准输入格式**，所有主流项目都以 Markdown 为源
3. **python-pptx 是 Python 生态唯一的 PPTX 生成库**，md2pptx 和 Text-to-PPT 都依赖它
4. **AI 生成 PPT 仍处早期**，Text-to-PPT(36★) 和 PPT_Generate(6★) 规模很小

### 对 ppt_utils 的演进建议
1. **短期**: 增加 Markdown 解析输入层（模式 1），支持 `---` 分页 + YAML frontmatter
2. **短期**: 将布局注册为命名字典（模式 2），与 design_tokens 正交组合
3. **中期**: 增加 LLM 集成接口（模式 3），接受结构化 JSON 或 Markdown 输入
4. **远期**: 考虑 MCP Server 封装，让 AI Agent 直接调用生成 PPT

---

## 五、数据来源

- GitHub REST API (`api.github.com`)：项目元数据、README
- 搜索关键词：`ppt generation`, `markdown presentation`, `slides generator`, `powerpoint python`
- 搜索时间：2025-03-25
- 注：因浏览器 TM 驱动不可用，未使用网页搜索，全部通过 API 获取