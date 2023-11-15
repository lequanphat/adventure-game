import sqlite3
class database():
    def __init__(self):
        conn = sqlite3.connect("statistic.db")
        print('connected')
        cursor = conn.cursor()
        print('connected')
        table_name = "statistic" 
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, player_name TEXT, score TEXT, level TEXT, mode TEXT)"
        print('connected')
        cursor.execute(create_table_sql)
        print('connected')
        conn.commit()
        conn.close()
        print('connected')
    
    def save_statistic(self, name, score, level, mode):
        conn = sqlite3.connect("statistic.db")
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO statistic (player_name, score, level, mode) VALUES (?, ?, ?,?)", (name, score, level,mode))
        conn.commit()
        conn.close()

    def get_statistic(self):
        print('connected')
        conn = sqlite3.connect("statistic.db")
        print('connected')
        cursor = conn.cursor()
        print('connected')
        cursor.execute("SELECT * FROM statistic")
        rows = cursor.fetchall()
        print(len(rows))
        for row in rows:
            print(row)  # Hiển thị thông tin của từng hàng
        conn.close()