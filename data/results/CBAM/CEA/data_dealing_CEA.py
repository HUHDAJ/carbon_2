import pandas as pd
import numpy as np
import sqlite3 
conn = sqlite3.connect('./datas_for_CBAM/cbam_database.db')
datas = pd.read_sql_query(f'SELECT * FROM CEA_datas',conn)
conn.close()

def get_CEA_average_price():
    higher_price = np.array(datas['highest(RMB/ton)']).mean()
    lower_price = np.array(datas['lower(RMB/ton)']).mean()
    average_price = (higher_price + lower_price)/2
    return average_price

if __name__ == '__main__':
    print(f'{get_CEA_average_price():.2f}')