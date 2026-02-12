import sqlite3
import pandas as pd
conn = sqlite3.connect('cbam_database.db')
cursor = conn.cursor()
data_input = pd.read_sql_query("SELECT * FROM forecast", conn)
data_input.to_csv('forecast.csv', index=False)