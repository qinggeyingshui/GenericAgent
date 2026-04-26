# R185 - 自媒体运营看板Workflow

## 执行信息
- 时间: 2026-04-21
- 类型: 产出
- 任务: content_creation | 自媒体运营看板Workflow

## 产出
### 1. 核心工具
- **文件**: `temp/tools/media_dashboard_workflow.py` (101行)
- **功能**: 串联 media_analytics + trend_tracker + platform_adapter

### 2. 主要函数
```python
generate_daily_report(data_file, content_texts, output_dir)
  # 生成运营日报，包含数据概览和趋势分析

generate_weekly_report(data_file, content_texts, output_dir)
  # 生成运营周报，包含可视化图表

create_dashboard(data_file, content_texts, platforms, output_dir)
  # 创建完整运营看板，整合周报+平台适配
```

### 3. 验收结果
✅ 测试通过，成功生成:
- 日报: 数据概览 + 趋势分析
- 周报: 数据概览 + 可视化图表 + 趋势分析
- 看板: 周报 + 平台适配内容

生成文件:
- `daily_report_20260421.txt`
- `weekly_report_20260421.txt`
- `charts/trend_20260421.png` (趋势图)
- `platform_adapted.txt` (微信/知乎适配)

## 技术亮点
1. **Workflow设计**: 串联3个已有工具，形成端到端流程
2. **数据驱动**: 基于CSV/Excel数据自动生成分析报告
3. **可视化**: 自动生成趋势图表
4. **平台适配**: 支持多平台内容格式转换

## 使用示例
```python
import media_dashboard_workflow as mdw

# 生成周报
mdw.generate_weekly_report(
    'data.csv',
    ['文本1', '文本2'],
    './reports'
)

# 创建完整看板
mdw.create_dashboard(
    'data.csv',
    ['文本1', '文本2'],
    platforms=['wechat', 'zhihu'],
    output_dir='./dashboard'
)
```

## 后续优化方向
- 支持更多数据源（API接口）
- 增加更多可视化图表类型
- 支持自动定时生成报告
- 增加数据对比分析功能