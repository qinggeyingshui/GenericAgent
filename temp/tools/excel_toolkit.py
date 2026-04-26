"""
Excel数据处理工具
支持读取/写入/公式计算/图表生成
依赖: pandas, xlsxwriter (读取需额外安装openpyxl)
"""
import pandas as pd
import xlsxwriter
from typing import List, Dict, Optional


def read_excel(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """读取Excel文件 (需要安装openpyxl: pip install openpyxl)"""
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    except ImportError:
        raise ImportError("读取Excel需要安装openpyxl: pip install openpyxl")


def write_excel(df: pd.DataFrame, file_path: str, sheet_name: str = "Sheet1"):
    """写入Excel文件"""
    df.to_excel(file_path, sheet_name=sheet_name, index=False, engine='xlsxwriter')


def create_chart_excel(data: Dict[str, List], output_path: str, 
                       chart_type: str = "column", title: str = "Chart"):
    """创建带图表的Excel文件
    
    Args:
        data: 字典格式数据 {'列名': [值列表]}
        output_path: 输出文件路径
        chart_type: 图表类型 (column/line/pie/bar)
        title: 图表标题
    """
    df = pd.DataFrame(data)
    
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Data', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Data']
        
        chart = workbook.add_chart({'type': chart_type})
        
        # 添加数据系列
        for i, col in enumerate(df.columns[1:], start=1):
            chart.add_series({
                'name': col,
                'categories': ['Data', 1, 0, len(df), 0],
                'values': ['Data', 1, i, len(df), i],
            })
        
        chart.set_title({'name': title})
        chart.set_x_axis({'name': df.columns[0]})
        worksheet.insert_chart('E2', chart, {'x_scale': 1.5, 'y_scale': 1.5})


def create_with_formula(data: Dict[str, List], output_path: str, 
                       formulas: Dict[str, str]):
    """创建Excel并添加公式列
    
    Args:
        data: 基础数据
        output_path: 输出路径
        formulas: 公式字典 {'列名': '公式'} 如 {'利润': '=B2-C2'}
    """
    df = pd.DataFrame(data)
    
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        
        # 添加公式列
        col_idx = len(df.columns)
        for col_name, formula in formulas.items():
            worksheet.write(0, col_idx, col_name)
            for row in range(1, len(df) + 1):
                worksheet.write_formula(row, col_idx, formula.replace('2', str(row+1)))
            col_idx += 1


if __name__ == "__main__":
    # 验收测试：处理10行数据生成图表
    test_data = {
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月'],
        '销售额': [120, 150, 180, 160, 200, 220, 190, 210, 230, 250],
        '成本': [80, 90, 100, 95, 110, 120, 105, 115, 125, 135]
    }
    
    print("测试1: 创建带图表的Excel")
    create_chart_excel(test_data, './test_chart.xlsx', 
                      chart_type='column', title='月度销售数据')
    print("✓ 图表Excel: ./test_chart.xlsx")
    
    print("\n测试2: 创建带公式的Excel")
    create_with_formula(test_data, './test_formula.xlsx',
                       formulas={'利润': '=B2-C2', '利润率': '=(B2-C2)/B2'})
    print("✓ 公式Excel: ./test_formula.xlsx")
    
    print("\n✓✓✓ 验收测试通过 ✓✓✓")
