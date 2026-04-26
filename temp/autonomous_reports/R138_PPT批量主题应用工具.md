# PPT批量主题应用工具开发

## 任务背景

**需求来源**: 用户长期目标是"Office本地能力专家（尤其PPT）"，skill_tree统计显示document_generation类别使用8次，其中ppt_creation使用2次，ppt_generation使用3次，存在明确的PPT能力提升需求。

**功能缺口**: 现有ppt_theme_manager.py仅支持将主题应用到配置对象，无法直接修改已有PPT文件。用户需要"一键切换主题，批量应用"的能力。

## 开发内容

### 1. 工具文件

**文件路径**: `./tools/ppt_batch_theme_applier.py`

**核心功能**:
- 单文件主题应用: `apply_theme_to_file(ppt_path, theme_id, output_path)`
- 批量目录处理: `batch_apply_theme(input_dir, theme_id, output_dir)`
- 主题配色应用: 背景色、文本色、形状填充色
- 字体统一设置: 标题字体、正文字体
- CLI命令行接口: 支持单文件/批量处理、主题列表查看

### 2. 技术实现

**技术栈**:
- `win32com.client`: 操控PowerPoint应用
- `ppt_theme_manager.py`: 复用现有主题配置（6个预设主题）
- `pathlib.Path`: 文件路径处理

**关键逻辑**:
```python
# 颜色转换
def _hex_to_rgb(hex_color: str) -> int:
    # 将#1E3A8A转换为RGB整数
    r, g, b = int(hex_color[0:2], 16), ...
    return r + (g << 8) + (b << 16)

# 主题应用
- 遍历所有幻灯片
- 设置背景颜色: slide.Background.Fill.ForeColor.RGB
- 遍历所有形状，处理文本框和填充
- 标题使用primary色，正文使用text色，形状使用accent色
```

### 3. 使用示例

```bash
# 列出所有主题
python ppt_batch_theme_applier.py --list-themes

# 单文件应用主题
python ppt_batch_theme_applier.py presentation.pptx -t tech_dark -o output.pptx

# 批量处理目录
python ppt_batch_theme_applier.py ./ppt_folder -t fresh_green -o ./themed_output

# 覆盖原文件
python ppt_batch_theme_applier.py presentation.pptx -t elegant_purple
```

## 功能增强对比

| 功能 | 原ppt_theme_manager | 新工具 |
|------|-------------------|--------|
| 主题配置管理 | ✓ | ✓ |
| 应用到配置对象 | ✓ | ✓ |
| 修改已有PPT文件 | ✗ | ✓ |
| 批量处理 | ✗ | ✓ |
| 命令行接口 | 仅list | 完整CLI |
| 颜色方案应用 | ✗ | ✓ |
| 字体统一设置 | ✗ | ✓ |

## 技能树更新

**类别**: document_generation.ppt_creation

**新增工具**: ppt_batch_theme_applier.py

**新增函数**:
- `apply_theme_to_file()`: 单文件主题应用
- `batch_apply_theme()`: 批量目录处理
- `_hex_to_rgb()`: 颜色转换

## 后续优化方向

1. **主题预览**: 生成主题效果预览图
2. **自定义主题**: 支持用户创建新主题配置
3. **智能识别**: 根据PPT内容自动推荐主题
4. **撤销功能**: 保存原始配色方案，支持一键还原
5. **模板库**: 集成更多专业PPT模板

## 评分复盘

**任务评分**: 0.71 (排名第1)
- 广度: 0.3 (增强现有PPT能力)
- 深度: 0.9 (显著提升ppt_creation功能完整性)
- 实用: 1.0 (直接响应用户明确需求)
- 创新: 0.4 (技术成熟但组合创新)

**实际产出**:
- ✓ 完整的批量主题应用工具
- ✓ 支持6种预设主题
- ✓ CLI和API双接口
- ✓ 与现有ppt_theme_manager无缝集成

---

[skill_used: ppt_theme_manager.py, win32com]
[ability_upgraded: document_generation.ppt_creation]
[tags: ppt, theme, batch_processing, office_automation]