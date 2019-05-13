import sqlite3

DB_FILE = "data/borkbook.db"

def create_db():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, team_ids TEXT, player_name TEXT, player_age INT, player_height INT, player_weight INT, player_jersey INT)")
    c.execute("CREATE TABLE IF NOT EXISTS plays(creator TEXT, command_list TEXT, editor_list TEXT, viewer_list TEXT, team_ids INT)")
    c.execute("CREATE TABLE IF NOT EXISTS teams(team_name TEXT, sport TEXT, team_id INT PRIMARY KEY, team_admins TEXT)")

    db.commit()
    db.close()

    return True;

def getUser(inputusername):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username, team_ids, player_name, player_age, player_height, player_weight, player_jersey FROM users WHERE username = ?", (inputusername,))
    selectedVal = c.fetchone()
    db.commit()
    db.close()
    return selectedVal
