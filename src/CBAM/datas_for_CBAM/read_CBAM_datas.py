import pandas as pd
import numpy as np
import sqlite3



db_path = './database/cbam_database.db'
conn = sqlite3.connect(db_path)
lower_heat_value = pd.read_sql_query(f'SELECT * FROM lower_heat_value',conn)#低位发热量
burning_heats = pd.read_sql_query(f'SELECT * FROM burning_heats',conn)#每太焦耳能量的燃料的CO2排放因子
electric_carbon_area1 = pd.read_sql_query(f'SELECT * FROM table1',conn)#全国区域电力平均排放因子（华东，华北...）
emit_of_iron_steel = pd.read_sql_query(f'SELECT * FROM emit_of_iron_steel',conn)#钢铁行业（以螺纹钢为例）排放因子
electric_carbon_area2 = pd.read_sql_query(f'SELECT * FROM table2',conn)#各省份电力平均排放因子
ore_producing = pd.read_sql_query(f'SELECT * FROM ore_producing',conn)#矿石开采及选矿碳排放因子
ore_using = pd.read_sql_query(f'SELECT * FROM ore_using',conn)#矿石使用碳排放因子
read_fertilizer_datas = pd.read_sql_query(f'SELECT * FROM read_fertilizer_datas',conn)#化肥生产过程排放因子
electric_carbon_daily  = pd.read_sql_query(f'SELECT * FROM electric_carbon_daily',conn)#日度电力碳排放因子
conn.close()

def fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7):     #计算各类燃料碳排放因子，单位tCO2/t或tCO2/万立方米(液化石油气，炼厂干气单位是吨)['电煤', '无烟煤', '炼焦烟煤', '一般烟煤', '褐煤', '煤制品', '焦炭', '原油', '燃料油', '汽油', '煤油', '柴油', '液化石油气', '炼厂干气', '天然气', '焦炉煤气', '高炉煤气', '转炉煤气','其他煤气']
    
    lower_heats = dict(zip(list(lower_heat_value['能源名称']),list(lower_heat_value['低位发热量'])))
    brun_heats = dict(zip(list(burning_heats['燃料类型']),list(burning_heats['CO2因子'])))
    lo1 = ['标准煤','标准煤','标准煤','标准煤','标准煤','标准煤','标准煤','原油','燃料油','汽油','煤油','柴油','液化石油气','炼厂干气','天然气','焦炉煤气','高炉煤气','转炉煤气','其它煤气']
    bn1 = ['电煤', '无烟煤', '炼焦烟煤', '一般烟煤', '褐煤', '煤制品', '焦炭', '原油', '燃料油', '汽油', '煤油', '柴油', '液化石油气', '炼厂干气', '天然气', '焦炉煤气', '高炉煤气', '转炉煤气','其他煤气']
    emit_of_fuel = []
    fuel = []
    for i in range(len(lo1)):
        heat = lower_heats[lo1[i]]
        emit = brun_heats[bn1[i]]
        burning_heat = heat * emit /1000  #tCO2/t或tCO2/万立方米(液化石油气，炼厂干气单位是吨)
        emit_of_fuel.append(round(burning_heat,4))
        fuel.append(bn1[i])
        #print(f'输出{fuel}的碳排放总和（单位碳排放量*低位发热量/1000*用量）')
    emit_of_fuel1 = emit_of_fuel[0]*coal1 + emit_of_fuel[1]*coal2 + emit_of_fuel[2]*coal3 + emit_of_fuel[3]*coal4 + emit_of_fuel[4]*coal5 + emit_of_fuel[5]*coal6 + emit_of_fuel[6]*coal7 + emit_of_fuel[7]*oil1 + emit_of_fuel[8]*oil2 + emit_of_fuel[9]*oil3 + emit_of_fuel[10]*oil4 + emit_of_fuel[11]*oil5 + emit_of_fuel[12]*gas1 + emit_of_fuel[13]*gas2 + emit_of_fuel[14]*gas3 + emit_of_fuel[15]*gas4 + emit_of_fuel[16]*gas5 + emit_of_fuel[17]*gas6 + emit_of_fuel[18]*gas7

    return emit_of_fuel1
# def electric_carbon_area(use_MWh,area_level = '全国'):      #根据输入的地区，返回该地区的电力碳排放因子，单位tCO2/MWh
#     average_carbon_emit1 = electric_carbon_area1['2021年排放因子']*electric_carbon_area1['2022年排放因子']/2  #全国和区域电力平均排放因子
#     average_carbon_emit_KWh1 = []
#     average_carbon_emit_KWh2 = []
#     use_MWh = (float(use_MWh))
#     average_carbon_emit2 = electric_carbon_area2['2021年排放因子']*electric_carbon_area2['2022年排放因子']/2  #全国和区域电力平均排放因子
#     for i in average_carbon_emit1:
#         average_carbon_emit_KWh1.append(i/1000)#kgCO2/kWh转为tCO2/MWh
#     for i in average_carbon_emit2:
#         average_carbon_emit_KWh2.append(i/1000)#kgCO2/kWh转为tCO2/MWh
#     area1 = dict(zip(list(electric_carbon_area1['地区']),average_carbon_emit_KWh1))
#     area2 = dict(zip(list(electric_carbon_area2['地区']),average_carbon_emit_KWh2))
#     area3 = dict(zip(['北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏','浙江','安徽','福建','西藏','香港','澳门','台湾','华南'],[area1['华北'],area1['华北'],area1['华北'],area1['华北'],area1['华北'],area1['东北'],area1['东北'],area1['东北'],area1['华东'],area1['华东'],area1['华东'],area1['华东'],area1['华东'],area1['西南'],area1['全国'],area1['全国'],area1['全国'],area1['南方']]))
#     if (area_level in area1.keys()):
#         return area1[area_level]*use_MWh
#     elif (area_level in area2.keys()):
#         return area2[area_level]*use_MWh
#     elif (area_level in area3.keys()):
#         return area3[area_level]*use_MWh
#     else:
#         area_level = '全国'
#         print('输入地区有误，请检查，已默认按照全国平均值计算')
#         return area1[area_level]*use_MWh
def electric_carbon_area(use_MWh,month1,day1,area_label = 1):      #根据输入的地区，返回该地区的日级电力碳排放因子，单位tCO2/MWh
    use_MWh = (float(use_MWh))
    if area_label == 1:
        electric_carbon_area1['日期'] = pd.to_datetime(electric_carbon_area1['日期'])
        elec1 = electric_carbon_area1[(electric_carbon_area1['日期'].dt.month == month1) & (electric_carbon_area1['日期'].dt.day == day1)]
        total_carbon1 = elec1.loc[:,'电力碳因子(kgCO2e/kWh)'].sum()/(len(elec1))*use_MWh/1000
    elif area_label == 2:
        electric_carbon_daily['日期'] = pd.to_datetime(electric_carbon_daily['日期'])
        elec2 = electric_carbon_daily[(electric_carbon_daily['日期'].dt.month == month1) & (electric_carbon_daily['日期'].dt.day == day1)]
        total_carbon1 = elec2.loc[:,'电力碳因子(kgCO2e/kWh)'].sum()/(len(elec2))*use_MWh/1000
    return round(total_carbon1,4)

    
    
def rebar_carbon_progress_emit(pig_iron_weight,direct_reduced_iron,Fe_Ni,Fe_Cr,Mo_Fe,CaCO3,electrode):   #钢铁行业螺纹钢碳排放因子，单位tCO2/ton(生铁，直接还原铁，镍铁合金，铬铁合金，钼铁合金,石灰石，电极)的质量
    pig_iron_weight = float(pig_iron_weight)
    direct_reduced_iron = float(direct_reduced_iron)
    Fe_Ni = float(Fe_Ni)
    Fe_Cr = float(Fe_Cr)
    Mo_Fe = float(Mo_Fe)
    CaCO3 = float(CaCO3)
    electrode = float(electrode)
    emit_single_ton = list(emit_of_iron_steel['CO₂排放因子'])
    emit_total = pig_iron_weight*emit_single_ton[0] + direct_reduced_iron*emit_single_ton[1] + Fe_Ni*emit_single_ton[2] + Fe_Cr*emit_single_ton[3] + Mo_Fe*emit_single_ton[4] + CaCO3*emit_single_ton[5] + electrode*emit_single_ton[6]
    #print(f'钢铁行业碳排放总和（单位碳排放量*用量）{list(emit_of_iron_steel['物料名称'])}')
    return emit_total
def ore_emit(FeCO3,CaCO3,dolomitic):
    FeCO3 = float(FeCO3)#铁矿石用量
    CaCO3 = float(CaCO3)#石灰石用量
    dolomitic = float(dolomitic)#白云石用量
    emit_single_ton = list(ore_producing['排放因子'])
    emit_single_ton2 = list(ore_using['排放因子'])
    emit_total = FeCO3*float(emit_single_ton[4]) + FeCO3*float(emit_single_ton2[4]) + CaCO3*float(emit_single_ton[0]) + CaCO3*float(emit_single_ton2[0]) + dolomitic*float(emit_single_ton[-1]) + dolomitic*float(emit_single_ton2[-2])
    return emit_total    
def fertilizer_process_emit(ammonia_coal,ammonia_gas,final_urea=0):   #化肥生产过程碳排放因子，单位tCO2/ton(煤制氨，气制氨),最终产量
    ammonia_coal = float(ammonia_coal)  #煤制氨用量
    ammonia_gas = float(ammonia_gas)    #气制氨用量
    emit_single_ton = list(read_fertilizer_datas['数值'])
    emit_total = ammonia_coal*emit_single_ton[0] + ammonia_gas*emit_single_ton[1] - final_urea*emit_single_ton[2]
    return emit_total

def get_CBAM_average_price():        #获取CBAM平均价格，单位RMB/ton
    return 658.60  #单位RMB/ton

if __name__ == '__main__':
    #print(emit_of_iron_steel)
    # print(lower_heat_value)
    # print(burning_heats)
    #print(electric_carbon_area1)
    # print(electric_carbon_area2)
    #print(fuel_carbon_emit(100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100))
    #print(electric_carbon_area('天津'))
    #print(rebar_carbon_progress_emit(100,100,10,10,10,10,10))
    # print(ore_producing)
    # print(ore_using)
    # print(ore_emit(100,100,100))
    # print(read_fertilizer_datas)
    # print(electric_carbon_area(1000,1,5))
    pass