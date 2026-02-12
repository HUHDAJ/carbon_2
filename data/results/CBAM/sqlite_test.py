import sqlite3
conn = sqlite3.connect('my_first_db.db')
cursor = conn.cursor()
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER          
    )          
''')
cursor.execute("INSERT INTO users(name,age)VALUES(?,?)",('XIAOMING',25))
conn.commit()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for line in rows:
    print(f'{rows}')
conn.close()