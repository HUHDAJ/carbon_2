import pandas as pd
import numpy as np
try:
    from CBAM.CEA import data_dealing_CEA as ddc # type: ignore
    from CBAM.datas_for_CBAM import read_CBAM_datas as rcd # type: ignore
    from CBAM.CEA import CEAforecast4 as cff4 # type: ignore

except Exception:
    import sys
    from pathlib import Path
    # When running this file directly, ensure project root is on sys.path
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from CBAM.CEA import data_dealing_CEA as ddc # type: ignore
    from CBAM.datas_for_CBAM import read_CBAM_datas as rcd # type: ignore
    from CBAM.CEA import CEAforecast4 as cff4# type: ignore

def judge_area_label(area_label):
    if area_label == '华东' or area_label == '华北' or area_label == '华南' or area_label == 1:
        return 1
    elif area_label == '西北' or area_label == '东北' or area_label == '西南'or area_label == 2:
        return 2
    else:
        print('输入地区有误，请检查，已默认按照全国平均值计算')
        return 1


def calcute_CBAM_carbon_rebar(pig_iron_weight=0,direct_reduced_iron=0,Fe_Ni=0,Fe_Cr=0,Mo_Fe=0,CaCO3=0,electrode=0,coal1=0,coal2=0,coal3=0,coal4=0,coal5=0,coal6=0,coal7=0,oil1=0,oil2=0,oil3=0,oil4=0,oil5=0,gas1=0,gas2=0,gas3=0,gas4=0,gas5=0,gas6=0,gas7=0,electric_use_MWh=0,month1=1,day1=1,area_label=1):#`计算螺纹钢碳排放总和`
    area_label1 = judge_area_label(area_label)
    carbon_emit = rcd.rebar_carbon_progress_emit(pig_iron_weight,direct_reduced_iron,Fe_Ni,Fe_Cr,Mo_Fe,CaCO3,electrode)
    carbon_emit += rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    carbon_emit += rcd.electric_carbon_area(electric_use_MWh,month1,day1,area_label=area_label1)
    carbon_rebar = carbon_emit
    process = rcd.rebar_carbon_progress_emit(pig_iron_weight,direct_reduced_iron,Fe_Ni,Fe_Cr,Mo_Fe,CaCO3,electrode)
    fuel = rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    electricity = rcd.electric_carbon_area(electric_use_MWh,month1,day1,area_label=area_label1)
     
    return carbon_rebar,process,fuel,electricity#返回：总碳排放，生产过程碳排放，燃料碳排放，电力碳排放
def calcute_CBAM_carbon_cement(coal1=0,coal2=0,coal3=0,coal4=0,coal5=0,coal6=0,coal7=0,oil1=0,oil2=0,oil3=0,oil4=0,oil5=0,gas1=0,gas2=0,gas3=0,gas4=0,gas5=0,gas6=0,gas7=0,electric_use_MWh=0,month1=1,day1=1,FeCO3=0,CaCO3=0,dolomitic=0,area_label=1):#计算水泥行业碳排放总和
    area_label1 = judge_area_label(area_label)
    carbon_emit = rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    carbon_emit += rcd.electric_carbon_area(electric_use_MWh,month1,day1,area_label=area_label1)
    carbon_emit += rcd.ore_emit(FeCO3,CaCO3,dolomitic)
    process = rcd.ore_emit(FeCO3,CaCO3,dolomitic)
    fuel = rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    electricity = rcd.electric_carbon_area(electric_use_MWh,month1,day1,area_label=area_label1)
    carbon_cement = carbon_emit 
    return carbon_cement,process,fuel,electricity#返回：总碳排放，生产过程碳排放，燃料碳排放，电力碳排放
def calculate_CBAM_fertilizer(coal1=0,coal2=0,coal3=0,coal4=0,coal5=0,coal6=0,coal7=0,oil1=0,oil2=0,oil3=0,oil4=0,oil5=0,gas1=0,gas2=0,gas3=0,gas4=0,gas5=0,gas6=0,gas7=0,electric_use_MWh=0,month1=1,day1=1,ammonia_coal=0,ammonia_gas=0,final_urea=0,area_label=1):#计算化肥碳排放总和
    area_label1 = judge_area_label(area_label)
    carbon_emit = rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    carbon_emit += rcd.electric_carbon_area(electric_use_MWh,month1,day1,area_label=area_label1)
    carbon_emit += rcd.fertilizer_process_emit(ammonia_coal,ammonia_gas,final_urea)#化肥生产过程碳排放因子
    process = rcd.fertilizer_process_emit(ammonia_coal,ammonia_gas,final_urea)
    fuel = rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    electricity = rcd.electric_carbon_area(electric_use_MWh,month1, day1,area_label=area_label1)
    carbon_fertilizer = carbon_emit 
    return carbon_fertilizer,process,fuel,electricity #返回：总碳排放，生产过程碳排放，燃料碳排放，电力碳排放
def calculate_CBAM_cost(carbon,days=30,free_allowance=0,free_allowance_EU=0):#计算CBAM成本
    _,_,average_price_CEA = cff4.main(number=days)
    if(free_allowance<=0):
        cost_CBAM = (rcd.get_CBAM_average_price()-average_price_CEA)*(carbon - carbon*free_allowance_EU)#无（中国地区）免费配额，将直接依据CBAM价格与CEA价格的差额进行计算（即欧盟中“已在第三国支付的碳价可以抵扣CBAM税，但是要补足差额）
    elif(free_allowance>0):
        cost_CBAM = (rcd.get_CBAM_average_price())*(carbon - free_allowance_EU) - (carbon-free_allowance)*average_price_CEA#有（中国地区）免费配额，将依据CBAM价格与CEA价格的差额进行计算，同时考虑免费配额不予抵扣的影响
    return round(cost_CBAM,2)


if __name__ == '__main__':
    x = int(input('请输入要预测的时间（天数）（不超过270）：'))
    y = input('请输入要计算的地区(华东/华北/华南/西北/东北/西南)：')
    print(calculate_CBAM_fertilizer(coal1=100,coal2=0,coal3=0,coal4=0,coal5=0,coal6=0,coal7=0,oil1=0,oil2=0,oil3=0,oil4=500,oil5=0,gas1=0,gas2=70,gas3=0,gas4=0,gas5=0,gas6=0,gas7=0,electric_use_MWh=10000,month1=1,day1=1,ammonia_coal=10000,ammonia_gas=100000,final_urea=1000,area_label=y))


    
    pass