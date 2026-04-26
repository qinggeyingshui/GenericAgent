# Excel数据处理 SOP

## 功能概述
提供Excel文件的读取、写入、公式计算和图表生成能力，支持数据分析和报表自动化。

## 工具文件
- **excel_toolkit.py**: Excel处理工具（位于 temp/）
- **依赖**: pandas, xlsxwriter (读取需额外安装openpyxl)

## 核心功能

### 1. 读取Excel
```python
from excel_toolkit import read_excel

# 读取Excel文件（需要openpyxl）
df = read_excel("data.xlsx", sheet_name="Sheet1")
```

### 2. 写入Excel
```python
from excel_toolkit import write_excel
import pandas as pd

df = pd.DataFrame({"姓名": ["张三", "李四"], "年龄": [25, 30]})
write_excel(df, "output.xlsx", sheet_name="员工")
```

### 3. 创建带图表的Excel
```python
from excel_toolkit import create_chart_excel

data = {
    "月份": ["1月", "2月", "3月"],
    "销售额": [100, 150, 200],
    "成本": [60, 80, 100]
}

create_chart_excel(
    data, 
    "sales_chart.xlsx",
    chart_type="column",  # column/line/pie/bar
    title="销售数据分析"
)
```

### 4. 创建带公式的Excel
```python
from excel_toolkit import create_with_formula

data = {
    "产品": ["A", "B", "C"],
    "收入": [1000, 1500, 2000],
    "支出": [600, 800, 1000]
}

formulas = {
    "利润": "=B2-C2",
    "利润率": "=(B2-C2)/B2"
}

create_with_formula(data, "report.xlsx", formulas)
```

## 支持的图表类型
- **column**: 柱状图
- **line**: 折线图
- **pie**: 饼图
- **bar**: 条形图

## 应用场景
1. **数据报表**: 自动生成月度/季度销售报表
2. **数据分析**: 处理实验数据并生成可视化图表
3. **财务报表**: 自动计算利润、成本等财务指标
4. **批量处理**: 批量读取多个Excel文件进行数据整合

## 注意事项
- 读取功能需要安装 openpyxl: `pip install openpyxl`
- 写入和图表生成使用 xlsxwriter，无需额外安装
- 公式使用Excel格式，如 `=B2-C2`
- 图表默认插入在E2单元格位置

## 验收测试
```python
from excel_toolkit import create_chart_excel, create_with_formula

# 测试1: 10行数据生成图表
test_data = {
    "月份": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月"],
    "销售额": [120, 150, 180, 160, 200, 220, 190, 210, 230, 250],
    "成本": [80, 90, 100, 95, 110, 120, 105, 115, 125, 135]
}
create_chart_excel(test_data, "test.xlsx", chart_type="column", title="月度数据")

# 测试2: 公式计算
create_with_formula(test_data, "test_formula.xlsx", 
                   formulas={"利润": "=B2-C2"})

print("✓ 验收测试通过")
```

---
[skill_mapping]
category: document_generation
skill: excel_processing
tools: excel_toolkit.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('excel_processing_sop.md')
```
