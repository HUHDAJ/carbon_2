import csv
import os
from typing import Dict, List


def read_and_process_power_data(base_path: str = "data/raw") -> Dict[int, Dict[str, List[float]]]:
    """读取电源数据，补全缺失值，计算月度占比"""
    power_files = {
        'total': '发电量月度数据.csv',
        'wind': '风力发电量月度数据.csv',
        'nuclear': '核能发电量月度数据.csv',
        'thermal': '火力发电量月度数据.csv',
        'hydro': '水力发电量月度数据.csv',
        'solar': '太阳能发电量月度数据.csv'
    }
    
    monthly_ratios = {}
    
    for year in [2022, 2023, 2024]:
        year_path = os.path.join(base_path, '各类电源的发电量', str(year))
        year_data = {}
        
        # 读取总发电量
        total_path = os.path.join(year_path, power_files['total'])
        if os.path.exists(total_path):
            year_data['total'] = fill_missing_data_with_annual_average(
                read_monthly_data(total_path, '当期值')
            )
        
        # 读取各电源数据
        for power_type, filename in power_files.items():
            if power_type == 'total':
                continue
            file_path = os.path.join(year_path, filename)
            if os.path.exists(file_path):
                year_data[power_type] = fill_missing_data_with_annual_average(
                    read_monthly_data(file_path, '当期值')
                )
        
        # 计算月度占比
        if 'total' in year_data:
            monthly_ratios[year] = {
                power_type: [
                    (monthly_values[i] / year_data['total'][i] if year_data['total'][i] > 0 else 0.0)
                    for i in range(12)
                ]
                for power_type, monthly_values in year_data.items()
                if power_type != 'total'
            }
    
    return monthly_ratios


def read_monthly_data(file_path: str, data_type: str) -> List[float]:
    """读取CSV中的月度数据"""
    monthly_data = [0.0] * 12
    
    try:
        with open(file_path, 'r', encoding='gbk') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and data_type in row[0]:
                    # 从第1列开始，对应月份为12-i（CSV中第一列是12月）
                    for i, cell in enumerate(row[1:13], start=1):
                        try:
                            value = float(cell) if cell else 0.0
                            month_index = 12 - i
                            if 0 <= month_index < 12:
                                monthly_data[month_index] = value
                        except ValueError:
                            continue
                    break
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
    
    return monthly_data


def fill_missing_data_with_annual_average(monthly_data: List[float]) -> List[float]:
    """使用年度平均值补全缺失数据"""
    valid_values = [v for v in monthly_data if v != 0.0]
    
    if not valid_values:
        return monthly_data
    
    average = sum(valid_values) / len(valid_values)
    return [v if v != 0.0 else average for v in monthly_data]


if __name__ == "__main__":
    # 简化调试输出
    print(f"当前目录: {os.getcwd()}")
    print(f"数据目录: {os.path.join(os.getcwd(), 'data/raw')}")
    
    ratios = read_and_process_power_data()
    
    print("\n月度占比结果:")
    for year, power_types in ratios.items():
        print(f"\n{year}年:")
        for power_type, ratios_list in power_types.items():
            print(f"  {power_type}: {[f'{r:.2%}' for r in ratios_list]}")