import sqlite3
class database():
    def __init__(self):
        conn = sqlite3.connect("statistic.db")
        cursor = conn.cursor()
        table_name = "statistic" 
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, player_name TEXT, score INTEGER, level INTEGER, mode TEXT)"
        cursor.execute(create_table_sql)
        conn.commit()
        conn.close()
    
    def save_statistic(self, name, score, level, mode):
        conn = sqlite3.connect("statistic.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO statistic (player_name, score, level, mode) VALUES (?, ?, ?,?)", (name, score, level,mode))
        conn.commit()
        conn.close()

    def get_statistic(self):
        conn = sqlite3.connect("statistic.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM statistic")
        rows = cursor.fetchall()
        print(len(rows))
        for row in rows:
            print(row)  # Hiển thị thông tin của từng hàng
        conn.close()
        return rows

    def get_ranking(self, mode):
        conn = sqlite3.connect("statistic.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM statistic WHERE mode=? ORDER BY score DESC", (mode, ))
        rows = cursor.fetchall()
        print(len(rows))
        conn.close()
        return rows