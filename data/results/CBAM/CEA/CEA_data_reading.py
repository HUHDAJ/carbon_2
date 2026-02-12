import re
import pandas as pd
import numpy as np
import sqlite3




with open('./CEA_original_data_v1.0.txt',encoding='utf-8') as f1:
    content = f1.read()

    date = re.compile('截至[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日')#日期
    date20 = re.compile('发布时间：[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}')#日期
    opening = re.compile('开盘价[0-9]+\.[0-9]+')#开盘价
    highest = re.compile('最高价[0-9]+\.[0-9]+')#最高价
    least = re.compile('最低价[0-9]+\.[0-9]+')#最低价
    ending = re.compile('收盘价[0-9]+\.[0-9]+')#收盘价
    percent_of_change = re.compile('收盘价(?:较前一日(?:上涨[0-9]+\.[0-9]+%|下跌[0-9]+\.[0-9]+%)|与前一日持平)')#涨幅
    exchange = re.compile('总成交量[0-9,]+吨')#单日总成交量
    charge = re.compile('总成交额[0-9,]+\.[0-9]+')#单日总成交额

    date2 = re.compile('[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日')#日期
    date22 = re.compile('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}')
    opening2 = re.compile('[0-9]+\.[0-9]+')#开盘价
    highest2 = re.compile('[0-9]+\.[0-9]+')#最高价
    least2 = re.compile('[0-9]+\.[0-9]+')#最低价
    ending2 = re.compile('[0-9]+\.[0-9]+')#收盘价
    percent_of_change2 = re.compile('上涨[0-9]+\.[0-9]+%|下跌[0-9]+\.[0-9]+%|持平')#涨幅
    exchange2 = re.compile('[0-9,]+')#单日总成交量
    charge2 = re.compile('[0-9,]+\.[0-9]+')#单日总成交额

    date_ = date.findall(content)
    opening_ = opening.findall(content)
    highest_ = highest.findall(content)
    least_ = least.findall(content)
    ending_ =ending.findall(content)
    percent_of_change_ = percent_of_change.findall(content)
    exchange_ = exchange.findall(content)
    charge_ = charge.findall(content)
    date2_ = date20.findall(content)
    date1 = []
    opening1 = []
    highest1 = []
    least1 = []
    ending1 = []
    percent_of_change1 = []
    exchange1 = []
    charge1 = []
    date21 = []
    
    for dates in range(len(date_)):         #提取出精确的日期信息
        date1.append(date2.findall(date_[dates]))
    for dates in range(len(date_)):         #二维列表一维化，便于生成csv文件
        date1[dates] = date1[dates][0]
    for dates in range(len(date2_)):         #提取出精确的日期信息
        date21.append(date22.findall(date2_[dates]))
    for dates in range(len(date2_)):         #二维列表一维化，便于生成csv文件
        date21[dates] = date21[dates][0]
    date1 = date21 + date1
    for openings in range(len(opening_)):
        opening1.append(opening2.findall(opening_[openings]))
    for openings in range(len(opening_)):
        opening1[openings] = opening1[openings][0]
    for highests in range(len(highest_)):
        highest1.append(highest2.findall(highest_[highests]))
    for highests in range(len(highest_)):
        highest1[highests] = highest1[highests][0]
    for leasts in range(len(least_)):
        least1.append(least2.findall(least_[leasts]))
    for leasts in range(len(least_)):
        least1[leasts] = least1[leasts][0]
    for endings in range(len(ending_)):
        ending1.append(ending2.findall(ending_[endings]))
    for endings in range(len(ending_)):
        ending1[endings] = ending1[endings][0]
    for pct in range(len(percent_of_change_)):
        percent_of_change1.append(percent_of_change2.findall(percent_of_change_[pct]))
    for pct in range(len(percent_of_change_)):
        percent_of_change1[pct] = percent_of_change1[pct][0]
    for exc in range(len(exchange_)):
        exchange1.append(exchange2.findall(exchange_[exc]))
    for exc in range(len(exchange_)):
        exchange1[exc] = exchange1[exc][0]
    for chg in range(len(charge_)):
        charge1.append(charge2.findall(charge_[chg]))
    for chg in range(len(charge_)):
        charge1[chg] = charge1[chg][0]
    pct_1 = str.maketrans({'上':'+','涨':'','下':'-','跌':'','持':'0','平':''})
    for i in range(len(percent_of_change1)):
        percent_of_change1[i] = str.translate(percent_of_change1[i],pct_1)
    date_1 = str.maketrans({"年":"/",'月':'/','日':'','-':'/'})
    for i in range(len(date1)):
        date1[i] = str.translate(date1[i],date_1)
    #print(len(date1),len(opening1),len(highest1),len(least1),len(ending1),len(percent_of_change1),len(exchange1),len(charge1))
    #print(date1,opening1,highest1,least1,ending1,percent_of_change1,exchange1,charge1),opening1,highest1,ending1,percent_of_change1,exchange1,charge1
    #print(len(date1),len(percent_of_change1))
    store = pd.DataFrame({
        'date':date1,
        'price(RMB/ton)':opening1,
        'highest(RMB/ton)':highest1,
        'lower(RMB/ton)':least1,
        'close(RMB/ton)':ending1,
        'upper(percent)':percent_of_change1,
        'daily_total_volume(tons)':exchange1,
        'daily_total_transaction_volume(RMB)':charge1

    })
    for col in store.columns:
        try:
            store[col] = store[col].astype('float64')
        except ValueError:
            pass
    



    # conn = sqlite3.connect('../datas_for_CBAM/cbam_database.db')
    # cursor = conn.cursor()
    # store.to_sql('CEA_datas',conn,if_exists='replace')
    # store['date'] = pd.to_datetime(store['date'])
    # print(store.groupby(store['date'].dt.month)['price(RMB/ton)'].mean())
    

