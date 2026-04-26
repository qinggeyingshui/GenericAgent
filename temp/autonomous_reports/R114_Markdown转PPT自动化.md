# Markdown转PPT深度自动化方案探索报告

## 任务背景
R113任务仅完成了Marp/Slidev等工具的调研，未进行实际实现和验证。本次探索深入研究Markdown转PPT的自动化方案，并实现了完整的教案转换工具。

## 探索过程

### 1. Marp技术验证
- **官网学习**：访问marp.app了解核心特性
- **CLI测试**：使用npx直接调用@marp-team/marp-cli（无需全局安装）
- **格式支持**：验证了HTML/PDF/PPTX三种输出格式

### 2. 基础功能实验
创建测试文件验证基本转换：
- Markdown → HTML：成功（即时预览）
- Markdown → PDF：成功（95KB）
- Markdown → PPTX：成功（274KB）

### 3. 高级特性测试
测试文件包含：
- 主题系统（gaia/default/uncover）
- 自定义CSS样式
- 分栏布局（grid）
- 数学公式（LaTeX）
- 代码高亮（多语言）
- 表格支持
- 背景图片（bg指令）
- 单页样式控制

结果：所有特性均成功转换为PPTX（1.1MB）

### 4. 教案转换工具开发

#### 工具名称
`lesson_plan_to_marp.py`

#### 核心功能
1. **自动解析**：读取教案Markdown文件
2. **智能分页**：按一级/二级标题自动插入分页符
3. **样式注入**：添加Marp frontmatter和自定义CSS
4. **一键生成**：调用Marp CLI输出PPTX

#### 使用方法
```bash
python lesson_plan_to_marp.py <教案文件.md> [输出目录]
```

#### 实际测试
- 输入：demo_lesson_plan.md（图神经网络教案，包含公式/代码/表格）
- 输出：demo_lesson_plan.pptx（1.06MB，自动分页为8页）
- 状态：✓ 转换成功

## 技术对比分析

### Marp vs python-pptx

| 维度 | Marp | python-pptx |
|------|------|-------------|
| **学习曲线** | 低（Markdown语法） | 高（需理解对象模型） |
| **开发效率** | 高（声明式） | 低（命令式） |
| **样式控制** | 中（CSS+主题） | 高（像素级控制） |
| **代码量** | 少（~100行） | 多（~500行） |
| **维护成本** | 低 | 高 |
| **适用场景** | 标准化演示文稿 | 复杂定制需求 |

### 推荐策略
- **教案→PPT**：优先使用Marp（快速、标准化）
- **数据可视化**：使用python-pptx（精确控制图表）
- **混合方案**：Marp生成基础框架 + python-pptx后处理特殊页面

## 技术要点

### 1. Marp CLI调用
```python
npx_path = r'E:\nvm\v20.12.2\npx.cmd'
subprocess.run([
    npx_path, '@marp-team/marp-cli',
    'input.md', '-o', 'output.pptx',
    '--allow-local-files'
])
```

### 2. Frontmatter配置
```yaml
---
marp: true
theme: default
paginate: true
backgroundColor: #fff
style: |
  section { font-size: 28px; }
  h1 { color: #0066cc; }
---
```

### 3. 分页控制
- 手动分页：`---`
- 自动分页：正则替换标题前插入`---`

### 4. 编码陷阱
Windows环境下print()使用Unicode字符（✓/✗）会触发GBK编码错误，需替换为ASCII字符。

## 成果交付

### 文件清单
1. `lesson_plan_to_marp.py` - 教案转换工具（主程序）
2. `marp_test.md` / `marp_advanced_test.md` - 测试用例
3. `demo_lesson_plan.md` - 模拟教案
4. `demo_lesson_plan.pptx` - 生成的演示文稿

### 工具特性
- ✓ 零配置使用（npx自动下载依赖）
- ✓ 跨平台支持（需Node.js环境）
- ✓ 保留Markdown所有格式
- ✓ 自动优化样式（字号/颜色/间距）

## 后续建议

### 短期优化
1. 添加主题选择参数（default/gaia/uncover）
2. 支持自定义CSS文件注入
3. 图片路径自动处理（相对→绝对）
4. 批量转换模式

### 长期规划
1. 集成到教案知识库系统
2. 开发VS Code插件（实时预览）
3. 探索Slidev（Vue驱动，更强交互性）
4. 研究Reveal.js（Web原生方案）

## 记忆更新建议

### global_mem_insight.txt
在"PPT制作"条目补充：
```
Marp教案转换: temp/lesson_plan_to_marp.py(MD→PPTX,npx CLI,智能分页) | 坑:Windows print Unicode需ASCII
```

### 新增SOP（可选）
创建 `memory/marp_automation_sop.md` 记录：
- Marp CLI完整参数
- 主题定制方法
- 常见问题解决方案
- 与python-pptx的协作模式

## 结论

本次探索成功验证了Marp作为Markdown→PPT自动化方案的可行性，并实现了可直接投入使用的教案转换工具。相比python-pptx，Marp在标准化场景下具有显著的效率优势，建议作为教案助手的首选方案。

---
**探索时间**：2026-04-02  
**任务编号**：R114（推测）  
**状态**：✓ 完成
