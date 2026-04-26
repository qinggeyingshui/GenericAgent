# R36 — teaching_kb 端到端激活与教案→PPT联动

## 任务目标
实测 teaching_kb 全流程，实现 create_lesson → generate_ppt 自动联动。验收标准：新建一份教案并自动生成配套教学PPT。

## 交付物

### 1. lesson2ppt.py 管道脚本
- 路径: `./teaching_kb/lesson2ppt.py` (~10KB)
- 功能: 解析 Markdown 教案 → 自动构建 PPT 配置 → 调用 generate_ppt 生成 PPTX
- 支持的教案结构: 课程信息、教学目标、教学过程（多阶段）、课后作业
- 自动映射 slide 类型: title_slide / section_header / bullet_list / two_column / key_point / summary
- 自动生成 materials_index.md 素材清单

### 2. L01 编译原理概述 — 示例教案
- 路径: `./teaching_kb/courses/编译原理/lessons/L01_编译原理概述/lesson_plan.md`
- 内容: 4个教学目标 + 4个教学阶段（导入/讲授/实践/总结）
- 覆盖编译器结构、词法分析、语法分析、语义分析等核心知识点

### 3. 自动生成的教学PPT
- 路径: `./teaching_kb/courses/编译原理/lessons/L01_编译原理概述/slides/编译原理_编译原理概述_教学课件.pptx`
- 规模: 15页幻灯片，49,749 bytes
- 配色: academic_blue 学术蓝配色方案
- 配置: `ppt_config.json` 同目录保存，可复现/微调

## 端到端验证结果

| 步骤 | 状态 | 说明 |
|------|------|------|
| 教案解析 | ✅ | 正确提取课程名、主题、4条目标、4个阶段 |
| PPT配置生成 | ✅ | 15页 slide 配置，类型映射正确 |
| PPTX文件生成 | ✅ | 49KB，通过 generate_ppt 引擎 |
| 素材清单更新 | ✅ | materials_index.md 自动生成 |

## 使用方法

```bash
# 从教案生成PPT（命令行）
python ./teaching_kb/lesson2ppt.py <教案路径.md>

# 示例
python ./teaching_kb/lesson2ppt.py ./teaching_kb/courses/编译原理/lessons/L01_编译原理概述/lesson_plan.md
```

## 技术备注
- generate_ppt.py 依赖 python-pptx，需 `pip install python-pptx`
- lesson2ppt.py 自动将 ppt_lab 加入 sys.path，无需额外配置
- 教案格式遵循 teaching_kb_sop 规范（Markdown 二级标题分区）