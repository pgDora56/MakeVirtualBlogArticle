import sqlite3

DB_NAME = "database.sqlite"

class DB:
    def __init__(self, dbname = DB_NAME):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS words(no INTEGER, parent INTEGER, cnt INTEGER, word TEXT)")

    def append(self, no, cnt, parent, word):
        sql = "INSERT INTO words (no, cnt, parent, word) VALUES (?, ?, ? ,?)"
        self.cur.execute(sql, (no, cnt, parent, word))
        
    def close(self):
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    database = DB("db.sqlite")
    database.append(417, "SHIINA")
    database.close()

