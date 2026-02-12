import csv
import os
import random
from datetime import datetime, timedelta
from calculate_GEF import (
    read_and_process_power_data,
    read_power_carbon_factors,
    read_csv_data,
    calculate_monthly_carbon_factor,
)


def generate_daily_factors_from_monthly(monthly_factors):
    """从月度碳因子生成每日碳因子"""
    daily_factors = {}
    
    for year, monthly_data in monthly_factors.items():
        year_daily_factors = {}
        
        for month_idx, monthly_factor in enumerate(monthly_data):
            month = month_idx + 1
            days_in_month = (datetime(year + (month == 12), month % 12 + 1, 1) 
                           - datetime(year, month, 1)).days
            
            # 为每日生成因子（±2%波动）
            daily_factors_month = []
            for day in range(days_in_month):
                fluctuation = random.uniform(-0.02, 0.02)
                daily_factors_month.append(monthly_factor * (1 + fluctuation))
            
            # 调整以确保月平均值匹配
            avg_daily = sum(daily_factors_month) / days_in_month
            adjustment = monthly_factor / avg_daily if avg_daily > 0 else 1
            daily_factors_month = [f * adjustment for f in daily_factors_month]
            
            base_date = datetime(year, month, 1)
            for day in range(days_in_month):
                date_str = (base_date + timedelta(days=day)).strftime("%Y-%m-%d")
                year_daily_factors[date_str] = daily_factors_month[day]
        
        daily_factors[year] = year_daily_factors
    
    return daily_factors


def save_daily_factors(daily_factors, output_dir="data/results/carbon_factors/day"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存每年的文件
    for year, year_data in daily_factors.items():
        output_file = os.path.join(output_dir, f"daily_carbon_factors_{year}.csv")
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["日期", "电力碳因子(kgCO2e/kWh)"])
            for date_str in sorted(year_data.keys()):
                writer.writerow([date_str, f"{year_data[date_str]:.6f}"])
        print(f"已保存: {output_file} ({len(year_data)}天)")
    
    # 保存汇总文件
    all_output_file = os.path.join(output_dir, "daily_carbon_factors_all.csv")
    with open(all_output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["日期", "电力碳因子(kgCO2e/kWh)"])
        for year in sorted(daily_factors.keys()):
            for date_str in sorted(daily_factors[year].keys()):
                writer.writerow([date_str, f"{daily_factors[year][date_str]:.6f}"])
    
    print(f"已保存汇总文件: {all_output_file}")


def main():
    print("开始计算每日电力碳因子...")
    
    # 读取数据
    monthly_ratios = read_and_process_power_data()
    carbon_factors = read_power_carbon_factors()
    loss_rates = read_csv_data('data/raw/线路损失率/线路损失率.csv', '年份', '损耗率')
    transmission_carbon = read_csv_data('data/raw/输配电碳因子/输配电碳因子.csv', '年份', 'kgCO₂e/kWh')
    
    monthly_carbon_factors = calculate_monthly_carbon_factor(
        monthly_ratios, carbon_factors, loss_rates, transmission_carbon
    )
    
    daily_factors = generate_daily_factors_from_monthly(monthly_carbon_factors)
    save_daily_factors(daily_factors)
    
    print("\n" + "="*50)
    print("每日电力碳因子统计信息:")
    print("="*50)
    
    for year in sorted(daily_factors.keys()):
        factors = list(daily_factors[year].values())
        avg = sum(factors) / len(factors)
        
        print(f"\n{year}年:")
        print(f"  天数: {len(factors)}")
        print(f"  平均值: {avg:.6f} kgCO2e/kWh")
        print(f"  最小值: {min(factors):.6f} kgCO2e/kWh")
        print(f"  最大值: {max(factors):.6f} kgCO2e/kWh")


if __name__ == "__main__":
    main()