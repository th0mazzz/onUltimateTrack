import sqlite3

DB_FILE = 'data/borkbook.db'

db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute("SELECT * from users")
selectedVal = c.fetchall()
db.commit()
db.close()

print(selectedVal)
