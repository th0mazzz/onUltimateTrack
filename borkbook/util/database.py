import os, sqlite3, uuid

DIR = os.path.dirname(__file__) or '.'
DIR += '/../'

DB_FILE = DIR + 'data/borkbook.db'

#DB_FILE = os.path.abspath("data/borkbook.db")

#method not accurate with schema no more
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
    c.execute("CREATE TABLE IF NOT EXISTS plays(creator TEXT, play_name TEXT, command_list TEXT, editor_list TEXT, team_ids TEXT, play_id TEXT PRIMARY KEY)")
    c.execute("CREATE TABLE IF NOT EXISTS teams(team_name TEXT, sport TEXT, team_id TEXT PRIMARY KEY, invite_code TEXT, team_admins TEXT)")
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
    UPDATES THE PLAYERS NAME GIVEN THE username AND THE new_player_name
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
    UPDATES THE PLAYERS AGE GIVEN THE username AND THE new_player_name
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
    UPDATES THE PLAYERS HEIGHT GIVEN THE username AND THE new_player_height
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
    UPDATES THE PLAYERS WEIGHT GIVEN THE username AND THE new_player_weight
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
    UPDATES THE PLAYERS JERSEY NUMBER GIVEN THE username AND THE new_player_jersey
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE users SET player_jersey = (?) WHERE users.username = (?)', (new_player_jersey, username))
    #username TEXT PRIMARY KEY, password TEXT, team_ids TEXT, player_name TEXT, player_age INT, player_height INT, player_weight INT, player_jersey INT
    db.commit()
    db.close()
    return True

def createPlay(creator, play_name, command_list, editor_list, team_id):
    '''
    CREATES A PLAY AND INSERTS INTO THE DATABASE
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    playid = str(uuid.uuid4())
    c.execute('INSERT INTO plays VALUES (?,?,?,?,?,?)', (creator, play_name, command_list, editor_list, team_id, playid))
    db.commit()
    db.close()
    return True

def getPlay(play_id):
    '''
    RETURNS PLAY command_list
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT command_list FROM plays WHERE play_id = ?', (play_id,))
    select = c.fetchone()
    db.commit()
    db.close()
    return select[0]

def editPlay(play_name, team_id):
    return 'WILL BE IMPLEMETED IN THE FUTURE'

def createTeam(team_name, sport, team_admin):
    '''
    CREATES TEAM AND INSERTS INTO THE DATABASE
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    team_id = str(uuid.uuid4())
    invite_code = str(uuid.uuid4())
    c.execute('INSERT INTO teams VALUES (?,?,?,?,?)', (team_name, sport, team_id, invite_code, team_admin))
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
    if select != None:
        return select[0]
    return None

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
    if select != None:
        return select[0]
    return None

def getPlaysByTeamId(team_id):
    '''
    RETURNS PLAYS THAT MATCH THE GIVEN team_id
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT * FROM plays WHERE plays.team_ids = ?', (str(team_id),))
    plays = c.fetchall()
    db.commit()
    db.close()
    return plays

def getTeamsByUser(username):
    '''
    RETURNS LIST OF TEAM_IDS THAT USER username IS PART OF
    '''
    userInfo = getUser(username)
    #print('userInfo', userInfo)
    #print(userInfo)
    teamsUserIsOn = userInfo[2]
    teamsUserIsOn = teamsUserIsOn.split(',')
    teamsUserIsOn = [x for x in teamsUserIsOn]
    return teamsUserIsOn

def getTeamInfo(team_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    teaminfo = c.execute('SELECT * from teams WHERE team_id = ?', (team_id,))
    teaminfo = teaminfo.fetchone()
    db.commit()
    db.close()
    return teaminfo

def getTeamsIdsUserisAdminOf(username):
    '''
    RETURNS TEAM IDS OF TEAMS USER IS ADMIN OF (ASSUMING ONLY CREATOR IS ADMIN)
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    teams = c.execute('SELECT team_id FROM teams WHERE team_admins = ?', (username,))
    teamsUserIsAdminOf = c.fetchall()
    #print('teamsUserIsAdminOf')
    #print(teamsUserIsAdminOf)
    newlist = [value[0] for value in teamsUserIsAdminOf]
    #print('newlist')
    #print(newlist)
    db.commit()
    db.close()
    return newlist

def getRosterByTeamId(team_id):
    '''
    RETURNS ROSTER OF TEAM GIVEN THE TEAM ID in the format (username, playername)
    (name, age, height, weight, jersey)
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    userbase = c.execute('SELECT username, player_name, player_age, player_height, player_weight, player_jersey, team_ids FROM users')
    userbase = userbase.fetchall()
    newUserbase = []
    for playerInfo in userbase:
        #playerInfo[0] is username
        #playerInfo[1] is player_name
        #playerInfo[2] is player_age
        #playerInfo[3] is player_height
        #playerInfo[4] is player_weight
        #playerInfo[5] is player_jersey
        #playerInfo[6] is teams, comma separated
        teamIDs = playerInfo[6]
        teamIDs = teamIDs.split(',')
        teamIDs.remove('')
        newUserbase.append((playerInfo[0], playerInfo[1], playerInfo[2], playerInfo[3], playerInfo[4], playerInfo[5], teamIDs))

    roster = []
    for player in newUserbase:
        if team_id in player[6]:
            roster.append((player[0], player[1], player[2], player[3], player[4], player[5]))

    #print('this is the userbase')
    #print(newUserbase)
    db.commit()
    db.close()
    return roster

def getInviteByTeamId(team_id):
    '''
    RETURNS INVITE CODE GIVEN TEAM ID
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    code = c.execute('SELECT invite_code FROM teams WHERE team_id = ?', (team_id,))
    returncode = code.fetchone()
    db.commit()
    db.close()
    return returncode[0]

def getTeamIdByInviteCode(joincode):
    '''
    RETURNS TEAM ID GIVEN INVITE CODE
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    code = c.execute('SELECT team_id FROM teams WHERE invite_code = ?', (joincode,))
    returncode = code.fetchone()
    db.commit()
    db.close()
    return returncode[0]

def getTeamAdmin(team_id):
    '''
    RETURNS TEAM ADMIN ASSUMING THAT TEAM CREATOR IS THE SOLE TEAM ADMIN
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    admin = c.execute('SELECT team_admins FROM teams WHERE team_id = ?', (team_id,))
    thesoleadmin = admin.fetchone()
    db.commit()
    db.close()
    return thesoleadmin[0]

def removeFromRoster(playername, team_id):
    '''
    REMOVES PLAYER FROM TEAM_IDS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    teams = getTeamsByUser(playername)
    print('teams')
    print(teams)
    if team_id in teams:
        teams.remove(team_id)
    newroster = ''
    for each in teams:
        newroster = newroster + ',' + each
    c.execute('UPDATE users SET team_ids = ? WHERE username = ?', (newroster, playername))
    c.execute('UPDATE teams SET team_admins = "" WHERE team_id = ? AND team_admins = ?', (team_id, playername))
    db.commit()
    db.close()
    fillNewAdmin(team_id)
    return True

def fillNewAdmin(team_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    roster = getRosterByTeamId(team_id)
    if len(roster) == 0:
        return "there ain't anyone on the team"
    newadmin = roster[0][0] #new admin
    c.execute('UPDATE teams SET team_admins = ? WHERE team_id = ? AND team_admins = ""', (newadmin, team_id))
    db.commit()
    db.close()
    return True

def removePlay(playid, team_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('DELETE FROM plays WHERE play_id = ? AND team_ids = ?', (playid, team_id))
    db.commit()
    db.close()
    return True
