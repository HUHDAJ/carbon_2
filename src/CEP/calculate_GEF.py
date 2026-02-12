import csv
import os
from monthly_percentage import read_and_process_power_data

POWER_TYPE_MAPPING = {
    'wind': '风力发电',
    'nuclear': '核能发电', 
    'thermal': '燃煤发电',
    'hydro': '水力发电',
    'solar': '光伏发电'
}


def read_csv_data(filepath, year_col, val_col, encoding='utf-8'):
    data = {}
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    year = int(row[year_col])
                    val_str = row[val_col].replace('%', '')
                    data[year] = float(val_str) / (100.0 if '%' in row[val_col] else 1.0)
        except Exception as e:
            print(f"读取 {filepath} 时出错: {e}")
    return data


def read_power_carbon_factors(base_path="data/raw"):
    #读取各电源类型的年度碳因子
    carbon_factors = {}
    
    for year in [2022, 2023, 2024]:
        year_path = os.path.join(base_path, '全国电力碳因子', str(year), '主要发电类型碳因子.csv')
        
        if not os.path.exists(year_path):
            print(f"警告: 文件 {year_path} 不存在")
            continue
            
        try:
            with open(year_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                year_factors = {}
                for row in reader:
                    headers = list(row.keys())
                    if len(headers) >= 2:
                        power_type = row[headers[0]]
                        try:
                            year_factors[power_type] = float(row[headers[1]])
                        except ValueError:
                            continue
                carbon_factors[year] = year_factors
        except Exception as e:
            print(f"读取碳因子文件 {year_path} 时出错: {e}")
    
    return carbon_factors


def calculate_monthly_carbon_factor(monthly_ratios, carbon_factors, loss_rates, transmission_carbon):
    #计算月电碳因子
    monthly_carbon_factors = {}
    
    for year, power_ratios in monthly_ratios.items():
        if year not in carbon_factors or year not in loss_rates or year not in transmission_carbon:
            continue
        
        year_factors = []
        loss_rate = loss_rates[year]
        transmission_factor = transmission_carbon[year]
        
        for month in range(12):
            total_factor = sum(
                power_ratios[power_en][month] * carbon_factors[year].get(POWER_TYPE_MAPPING[power_en], 0)
                for power_en in power_ratios if power_en in POWER_TYPE_MAPPING
            )
            
            if loss_rate >= 1.0:
                monthly_factor = total_factor + loss_rate * transmission_factor
            else:
                monthly_factor = (total_factor + loss_rate * transmission_factor) / (1 - loss_rate)
            
            year_factors.append(monthly_factor)
        
        monthly_carbon_factors[year] = year_factors
    
    return monthly_carbon_factors


def main():
    monthly_ratios = read_and_process_power_data()
    carbon_factors = read_power_carbon_factors()
    loss_rates = read_csv_data('data/raw/线路损失率/线路损失率.csv', '年份', '损耗率')
    transmission_carbon = read_csv_data('data/raw/输配电碳因子/输配电碳因子.csv', '年份', 'kgCO₂e/kWh')
    
    monthly_carbon_factors = calculate_monthly_carbon_factor(
        monthly_ratios, carbon_factors, loss_rates, transmission_carbon
    )
    
    annual_carbon_factors = {
        year: sum(monthly_factors) / len(monthly_factors)
        for year, monthly_factors in monthly_carbon_factors.items()
    }
    
    # 保存月度碳因子到CSV
    output_dir = "data/results/carbon_factors/month"
    os.makedirs(output_dir, exist_ok=True)
    
    for year, monthly_factors in monthly_carbon_factors.items():
        output_file = os.path.join(output_dir, f"monthly_carbon_factors_{year}.csv")
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["月份", "电力碳因子(kgCO2e/kWh)"])
            for month_idx, factor in enumerate(monthly_factors):
                writer.writerow([month_idx + 1, f"{factor:.6f}"])
        print(f"已保存月度碳因子: {output_file}")
    
    # 保存年度碳因子到CSV
    annual_output_file = os.path.join(output_dir, "annual_carbon_factors.csv")
    with open(annual_output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["年份", "电力碳因子(kgCO2e/kWh)"])
        for year, factor in annual_carbon_factors.items():
            writer.writerow([year, f"{factor:.6f}"])
    print(f"已保存年度碳因子: {annual_output_file}")
    
    print("="*50)
    print("月度碳因子结果 (kgCO2e/kWh):")
    print("="*50)
    
    for year, monthly_factors in monthly_carbon_factors.items():
        print(f"\n{year}年:")
        for month_idx, factor in enumerate(monthly_factors):
            print(f"  月份{month_idx+1:2d}: {factor:.6f}")
    
    print("\n" + "="*50)
    print("年度平均碳因子结果 (kgCO2e/kWh):")
    print("="*50)
    
    for year, factor in annual_carbon_factors.items():
        print(f"{year}年: {factor:.6f}")


if __name__ == "__main__":
    main()