import sqlite3
from util import database

'''
DB_FILE = 'data/borkbook.db'

db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute("SELECT * from users")
selectedVal = c.fetchall()
db.commit()
db.close()

print(selectedVal)
'''

print(database.getTeamsByUser('a'))
