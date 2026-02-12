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

average_price_CEA = round(ddc.get_CEA_average_price(),2)
def calcute_CBAM_carbon_rebar(pig_iron_weight=0,direct_reduced_iron=0,Fe_Ni=0,Fe_Cr=0,Mo_Fe=0,CaCO3=0,electrode=0,coal1=0,coal2=0,coal3=0,coal4=0,coal5=0,coal6=0,coal7=0,oil1=0,oil2=0,oil3=0,oil4=0,oil5=0,gas1=0,gas2=0,gas3=0,gas4=0,gas5=0,gas6=0,gas7=0,electric_use_MWh=0,month1=1,day1=1):#`计算螺纹钢碳排放总和`
    carbon_emit = rcd.rebar_carbon_progress_emit(pig_iron_weight,direct_reduced_iron,Fe_Ni,Fe_Cr,Mo_Fe,CaCO3,electrode)
    carbon_emit += rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    carbon_emit += rcd.electric_carbon_area(electric_use_MWh,month1,day1)
    carbon_rebar = carbon_emit
    process = rcd.rebar_carbon_progress_emit(pig_iron_weight,direct_reduced_iron,Fe_Ni,Fe_Cr,Mo_Fe,CaCO3,electrode)
    fuel = rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    electricity = rcd.electric_carbon_area(electric_use_MWh,month1,day1)
     
    return carbon_rebar,process,fuel,electricity
def calcute_CBAM_carbon_cement(coal1=0,coal2=0,coal3=0,coal4=0,coal5=0,coal6=0,coal7=0,oil1=0,oil2=0,oil3=0,oil4=0,oil5=0,gas1=0,gas2=0,gas3=0,gas4=0,gas5=0,gas6=0,gas7=0,electric_use_MWh=0,month1=1,day1=1,FeCO3=0,CaCO3=0,dolomitic=0):#计算水泥行业碳排放总和
    carbon_emit = rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    carbon_emit += rcd.electric_carbon_area(electric_use_MWh,month1,day1)
    carbon_emit += rcd.ore_emit(FeCO3,CaCO3,dolomitic)
    process = rcd.ore_emit(FeCO3,CaCO3,dolomitic)
    fuel = rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    electricity = rcd.electric_carbon_area(electric_use_MWh,month1,day1)
    carbon_cement = carbon_emit 
    return carbon_cement,process,fuel,electricity
def calculate_CBAM_fertilizer(coal1=0,coal2=0,coal3=0,coal4=0,coal5=0,coal6=0,coal7=0,oil1=0,oil2=0,oil3=0,oil4=0,oil5=0,gas1=0,gas2=0,gas3=0,gas4=0,gas5=0,gas6=0,gas7=0,electric_use_MWh=0,month1=1,day1=1,ammonia_coal=0,ammonia_gas=0,final_urea=0):#计算化肥碳排放总和
    carbon_emit = rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    carbon_emit += rcd.electric_carbon_area(electric_use_MWh,month1,day1)
    carbon_emit += rcd.fertilizer_process_emit(ammonia_coal,ammonia_gas,final_urea)#化肥生产过程碳排放因子
    process = rcd.fertilizer_process_emit(ammonia_coal,ammonia_gas,final_urea)
    fuel = rcd.fuel_carbon_emit(coal1,coal2,coal3,coal4,coal5,coal6,coal7,oil1,oil2,oil3,oil4,oil5,gas1,gas2,gas3,gas4,gas5,gas6,gas7)
    electricity = rcd.electric_carbon_area(electric_use_MWh,month1, day1)
    carbon_fertilizer = carbon_emit 
    return carbon_fertilizer,process,fuel,electricity
def calculate_CBAM_cost(carbon,days=30,free_allowance=0,free_allowance_EU=0):#计算CBAM成本
    _,_,average_price_CEA = cff4.main(number=days)
    if(free_allowance<=0):
        cost_CBAM = (rcd.get_CBAM_average_price()-average_price_CEA)*(carbon - carbon*free_allowance_EU)
    elif(free_allowance>0):
        cost_CBAM = (rcd.get_CBAM_average_price())*(carbon - free_allowance_EU) - (carbon-free_allowance)*average_price_CEA
    return round(cost_CBAM,2)


if __name__ == '__main__':
    x = int(input('请输入要预测的时间（天数）（不超过270）：'))
    print(f'预计CBAM总花费{calculate_CBAM_cost(calculate_CBAM_fertilizer(coal1=10,coal2=110,coal3=0,coal4=0,coal5=0,coal6=0,coal7=0,oil1=0,oil2=0,oil3=0,oil4=0,oil5=0,gas1=0,gas2=0,gas3=0,gas4=0,gas5=10,gas6=0,gas7=0,electric_use_MWh=100,month1=1,day1=1,ammonia_coal=0,ammonia_gas=100,final_urea=50)[0],days = x,free_allowance=0,free_allowance_EU=0)}RMB,总碳足迹{calculate_CBAM_fertilizer(coal1=10,coal2=110,coal3=0,coal4=0,coal5=0,coal6=0,coal7=0,oil1=0,oil2=0,oil3=0,oil4=0,oil5=0,gas1=0,gas2=0,gas3=0,gas4=0,gas5=100,gas6=0,gas7=0,electric_use_MWh=100,month1=1,day1=1,ammonia_coal=0,ammonia_gas=100,final_urea=50)[0]}t/CO2')#其中month1,day1代表生产日期中的月/日
    pass