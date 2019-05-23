import os, sqlite3, uuid

#DIR = os.path.dirname(__file__)
#DIR += '/'

#DB_FILE = DIR + 'data/borkbook.db'

DB_FILE = os.path.abspath("data/borkbook.db")


def insert_test_data():
    '''INSERTS TEST DATA'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?)", ("useruno", "pass", "1,33", "johnny wong", 18, '''4'1"''', "9000lbs", 30))
    c.execute("INSERT INTO plays VALUES(?,?,?,?,?,?)", ("useruno", "i make big flayz", "", "useruno", "", "1"))
    c.execute("INSERT INTO teams VALUES(?,?,?,?)", ("team yeeters", "ultimate freesbi", "1", "useruno"))
    db.commit()
    db.close()


def create_db():
    '''CREATES THE DATABASE WITH THE TABLES'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, team_ids TEXT, player_name TEXT, player_age INT, player_height INT, player_weight INT, player_jersey INT)")
    c.execute("CREATE TABLE IF NOT EXISTS plays(creator TEXT, play_name TEXT, command_list TEXT, editor_list TEXT, viewer_list TEXT, team_ids INT)")
    c.execute("CREATE TABLE IF NOT EXISTS teams(team_name TEXT, sport TEXT, team_id INT PRIMARY KEY, team_admins TEXT)")
    db.commit()
    db.close()

    #insert_test_data()
    print(DB_FILE)
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
    c.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?,?)', (username, password, '', player_name, player_age, player_height, player_weight, player_jersey))
    #username TEXT PRIMARY KEY, password TEXT, team_ids TEXT, player_name TEXT, player_age INT, player_height INT, player_weight INT, player_jersey INT
    db.commit()
    db.close()
    return True

def changePlayerName(username, new_player_name):
    '''
    UPDATES THE PLAYER'S NAME GIVEN THE username AND THE new_player_name
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE users SET player_name = (?) WHERE users.username = (?)', (new_player_name, username))
    #username TEXT PRIMARY KEY, password TEXT, team_ids TEXT, player_name TEXT, player_age INT, player_height INT, player_weight INT, player_jersey INT
    db.commit()
    db.close()
    return True

def changePlayerAge(username, new_player_age):
    '''
    UPDATES THE PLAYER'S AGE GIVEN THE username AND THE new_player_name
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE users SET player_age = (?) WHERE users.username = (?)', (new_player_age, username))
    #username TEXT PRIMARY KEY, password TEXT, team_ids TEXT, player_name TEXT, player_age INT, player_height INT, player_weight INT, player_jersey INT
    db.commit()
    db.close()
    return True

def changePlayerHeight(username, new_player_height):
    '''
    UPDATES THE PLAYER'S HEIGHT GIVEN THE username AND THE new_player_height
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE users SET player_height = (?) WHERE users.username = (?)', (new_player_height, username))
    #username TEXT PRIMARY KEY, password TEXT, team_ids TEXT, player_name TEXT, player_age INT, player_height INT, player_weight INT, player_jersey INT
    db.commit()
    db.close()
    return True

def changePlayerWeight(username, new_player_weight):
    '''
    UPDATES THE PLAYER'S WEIGHT GIVEN THE username AND THE new_player_weight
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE users SET player_weight = (?) WHERE users.username = (?)', (new_player_weight, username))
    #username TEXT PRIMARY KEY, password TEXT, team_ids TEXT, player_name TEXT, player_age INT, player_height INT, player_weight INT, player_jersey INT
    db.commit()
    db.close()
    return True

def changePlayerJersey(username, new_player_jersey):
    '''
    UPDATES THE PLAYER'S JERSEY NUMBER GIVEN THE username AND THE new_player_jersey
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE users SET player_jersey = (?) WHERE users.username = (?)', (new_player_jersey, username))
    #username TEXT PRIMARY KEY, password TEXT, team_ids TEXT, player_name TEXT, player_age INT, player_height INT, player_weight INT, player_jersey INT
    db.commit()
    db.close()
    return True

def createPlay(creator, play_name, command_list, editor_list, viewer_list, team_id):
    '''
    CREATES A PLAY AND INSERTS INTO THE DATABASE
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('INSERT INTO plays VALUES (?,?,?,?,?,?)', (creator, play_name, command_list, editor_list, viewer_list, team_id))
    db.commit()
    db.close()
    return True

def editPlay(play_name, team_id):
    return 'WILL BE IMPLEMETED IN THE FUTURE'

def createTeam(team_name, sport, team_admin):
    '''
    CREATES TEAM AND INSERTS INTO THE DATABASE
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    team_id = str(uuid.uuid4())
    c.execute('INSERT INTO teams VALUES (?,?,?,?)', (team_name, sport, team_id, team_admin))
    db.commit()
    db.close()
    addTeamToUser(team_admin, team_id)
    return True


def addTeamToUser(username, team_id):
    '''
    INSERT TEAM ID TO CORRESPONDING USERNAME
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if len(getTeamsByUser(username)) < 1:
        # this is the user's first team
        # delimit each team_id by a comma
        c.execute('UPDATE users SET team_ids = ? WHERE username = ?', (team_id + ",", username))
    else:
        # the user is part of other teams
        prevIDS = ",".join(getTeamsByUser(username))
        c.execute('UPDATE users SET team_ids = ? WHERE username = ?', (prevIDS + ",{}".format(team_id), username))
    db.commit()
    db.close()
    return True

def getNameByTeamId(team_id):
    '''
    RETURNS TEAM NAME GIVEN TEAM_ID
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT team_name FROM teams WHERE team_id = ?', (team_id,))
    select = c.fetchone()
    db.commit()
    db.close()
    return select[0]

def getSportByTeamId(team_id):
    '''
    RETURNS TEAM SPORT GIVEN TEAM_ID
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT sport FROM teams WHERE team_id = ?', (team_id,))
    select = c.fetchone()
    db.commit()
    db.close()
    return select[0]

def getPlaysByTeamId(team_id):
    '''
    RETURNS PLAYS THAT MATCH THE GIVEN team_id
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT * FROM plays WHERE plays.team_ids = ?', (team_id,))
    plays = c.fetchall()
    db.commit()
    db.close()
    return plays

def getTeamsByUser(username):
    '''
    RETURNS LIST OF TEAM_IDS THAT USER username IS PART OF
    '''
    userInfo = getUser(username)
    #print(userInfo)
    teamsUserIsOn = userInfo[2]
    teamsUserIsOn = teamsUserIsOn.split(',')
    teamsUserIsOn = [x for x in teamsUserIsOn]
    return teamsUserIsOn

def getRosterByTeamId(team_id):
    '''
    RETURNS ROSTER OF TEAM GIVEN THE TEAM ID
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    userbase = c.execute('SELECT * FROM users')
    db.commit()
    db.close()
    return True
