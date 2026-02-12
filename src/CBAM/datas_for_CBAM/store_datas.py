import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine


lower_heat_value = pd.read_csv('./低位发热量.csv')#低位发热量
burning_heats = pd.read_csv('./燃料燃烧_化石燃料.csv')#每太焦耳能量的燃料的CO2排放因子
electric_carbon_area1 = pd.read_csv('./净购入电力与热力_电力消费排放因子-全国和区域.csv')#全国区域电力平均排放因子（华东，华北...）
emit_of_iron_steel = pd.read_csv('./螺纹钢（钢铁）过程排放计算参数.csv')#钢铁行业（以螺纹钢为例）排放因子
electric_carbon_area2 = pd.read_csv('./净购入电力与热力_电力消费排放因子-省级.csv')#各省份电力平均排放因子
ore_producing = pd.read_csv('./工业生产过程和产品使用_碳化工艺吸收过程.csv')#矿石开采及选矿碳排放因子
ore_using = pd.read_csv('./工业生产过程和产品使用_碳酸盐使用过程.csv')#矿石使用碳排放因子
read_fertilizer_datas = pd.read_csv('./尿素过程排放计算关键参数.csv')#化肥生产过程排放因子
electric_carbon_daily  = pd.read_csv('./daily_carbon_factors_all.csv')#日度电力碳排放因子

def store_datas():
    conn = sqlite3.connect('cbam_database.db')
    lower_heat_value.to_sql('lower_heat_value',conn,if_exists='replace')
    burning_heats.to_sql('burning_heats',conn,if_exists='replace')
    electric_carbon_area1.to_sql('electric_carbon_area1',conn,if_exists='replace')
    emit_of_iron_steel.to_sql('emit_of_iron_steel',conn,if_exists='replace')
    electric_carbon_area2.to_sql('electric_carbon_area2',conn,if_exists='replace')
    ore_producing.to_sql('ore_producing',conn,if_exists='replace')
    ore_using.to_sql('ore_using',conn,if_exists='replace')
    read_fertilizer_datas.to_sql('read_fertilizer_datas',conn,if_exists='replace')
    electric_carbon_daily.to_sql('electric_carbon_daily',conn,if_exists='replace')
    return 'successfully_store_datas'

if __name__ == '__main__':
    print(store_datas())







