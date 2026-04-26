# R159 PPT数据可视化增强

**日期**: 2026-04-20
**类型**: 产出
**主题**: PPT数据可视化工具开发

## 一、任务目标

开发ppt_data_viz.py，支持从Excel/CSV导入数据生成动态图表，并支持数据更新自动刷新。

## 二、产出内容

### 1. tools/ppt_data_viz.py（193行）

**核心函数**：
- `import_data_from_excel(file_path, sheet_name, header_row)` - 从Excel导入数据
- `import_data_from_csv(file_path, header_row)` - 从CSV导入数据
- `create_chart_from_file(slide, file_path, chart_type, ...)` - 从文件创建图表
- `update_chart_from_file(prs, slide_index, chart_index, new_file_path)` - 更新图表数据

**技术方案**：
- 基于pandas读取Excel/CSV
- 集成ppt_chart_toolkit生成图表
- 支持4种图表类型：COLUMN/BAR/LINE/PIE
- 数据格式：第一行表头，第一列类别，其余列系列

### 2. 更新ppt_com_sop第6节

新增数据可视化章节，包含：
- 核心函数签名
- 使用示例（创建+更新）
- 数据格式要求
- 注意事项

## 三、验收测试

```python
# 测试CSV导入和图表生成
data = import_data_from_csv('test.csv')
# ✓ categories=['Q1', 'Q2', 'Q3', 'Q4']
# ✓ series=['销售额', '成本']

prs = new_prs()
slide = add_blank_slide(prs)
chart = create_chart_from_file(slide, 'test.csv', 'COLUMN', title='季度销售数据')
save_prs(prs, 'test_data_viz.pptx')
# ✓ 图表生成成功

# 测试数据更新
prs = Presentation('test_data_viz.pptx')
update_chart_from_file(prs, 0, 0, 'test_new.csv')
prs.save('test_updated.pptx')
# ✓ 图表更新成功
```

**验收结果**：
- ✓ 支持从Excel/CSV导入数据
- ✓ 支持生成动态图表
- ✓ 支持数据更新自动刷新

## 四、技术亮点

1. **统一接口**：create_chart_from_file一步到位，无需手动解析数据
2. **灵活更新**：update_chart_from_file支持按索引更新任意图表
3. **格式兼容**：同时支持Excel和CSV，自动识别表头
4. **集成现有工具**：复用ppt_chart_toolkit，保持代码一致性

[skill_used]
- category: document_generation
- skill: presentation
- sop: ppt_com_sop.md
- tools: ppt_data_viz.py
[/skill_used]

## 五、结论

PPT数据可视化工具开发完成，支持Excel/CSV导入、图表生成和数据刷新，满足自媒体创作中的数据展示需求。
