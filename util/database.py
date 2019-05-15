import sqlite3

DB_FILE = "data/borkbook.db"

def insert_test_data():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?)", ("useruno", "pass", "1", "johnny wong", 18, '''4'1"''', "9000lbs", 30))
    c.execute("INSERT INTO plays VALUES(?,?,?,?,?,?)", ("useruno", "i make big flayz", "", "useruno", "", "1"))
    c.execute("INSERT INTO teams VALUES(?,?,?,?)", ("team yeeters", "ultimate freesbi", "1", "useruno"))

    db.commit()
    db.close()


def create_db():
    '''
    CREATES THE DATABASE WITH THE TABLES
    '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, team_ids TEXT, player_name TEXT, player_age INT, player_height INT, player_weight INT, player_jersey INT)")
    c.execute("CREATE TABLE IF NOT EXISTS plays(creator TEXT, play_name TEXT, command_list TEXT, editor_list TEXT, viewer_list TEXT, team_ids INT)")
    c.execute("CREATE TABLE IF NOT EXISTS teams(team_name TEXT, sport TEXT, team_id INT PRIMARY KEY, team_admins TEXT)")

    db.commit()
    db.close()

    #insert_test_data()

    return True;

def getUser(inputusername):
    '''
    RETURNS TUPLE OF FOLLOWING USER INFO OF inputusername
    (username, password, team_ids, player_name, player_age, player_height, player_weight, player_jersey)
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username, password, team_ids, player_name, player_age, player_height, player_weight, player_jersey FROM users WHERE username = ?", (inputusername,))
    selectedVal = c.fetchone()
    db.commit()
    db.close()
    return selectedVal

def registerUser(username, password, player_name, player_age=0, player_height=0, player_weight=0, player_jersey=0):
    '''
    REGISTERS USERS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?)', (username, password, '', player_name, player_age, player_height, player_weight, player_jersey))
    #username TEXT PRIMARY KEY, password TEXT, team_ids TEXT, player_name TEXT, player_age INT, player_height INT, player_weight INT, player_jersey INT
    db.commit()
    db.close()

    return True

def createPlay(creator, play_name, command_list, editor_list, viewer_list, team_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.commit()
    c.close()
    return True
