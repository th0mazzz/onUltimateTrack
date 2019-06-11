#! /usr/bin/env python
import os, json

from flask import flash, Flask, render_template, redirect, request, session, url_for

from util import database

app = Flask(__name__)
app.secret_key = "doa9jwdoiawjmdoawidnmawlmd90123u10293u819jADIOJOAKJmxnoiJAOAJDOIJDNOMZKOAJsyEET"

#DIR = os.path.dirname(__file__)
#DIR += '/'

#DB_FILE = DIR + 'data/borkbook.db'

#print(DB_FILE)

database.create_db()
#database.insert_test_data()

@app.route('/')
def landing():
    if 'username' not in session:
        return render_template('login.html', loggedin = "nope")
    return redirect(url_for('home'))

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', loggedin = "nope")

@app.route('/register')
def register():
    return render_template('register.html', loggedin = "nope")

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('landing'))
    #print(database.getTeamsByUser(session['username']))
    teams = []
    for id in database.getTeamsByUser(session['username']):
        print(id)
        teamname = database.getNameByTeamId(id)
        teamsport = database.getSportByTeamId(id)
        if len(id) > 1 and teamname != None and teamsport != None:
            teams.append([teamname, id, teamsport])
    username = session['username']

    print('printing')
    teamsUserIsAdminOf = database.getTeamsIdsUserisAdminOf(username)
    adminTeams = []

    if teamsUserIsAdminOf != None:
        for id in teamsUserIsAdminOf:
            print('id')
            print(id)
            teamname = database.getNameByTeamId(id)
            teamsport = database.getSportByTeamId(id)
            if len(id) > 1 and teamname != None and teamsport != None:
                adminTeams.append([teamname, id, teamsport])

    return render_template('home.html', username = username, teams= teams, adminTeams = adminTeams)

@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect(url_for('landing'))
    session.pop('username', None)
    flash('Successfully logged out!')
    return redirect(url_for('landing'))

@app.route('/auth', methods=["POST"])
def auth():
    user, pwd = request.form['username'], request.form['password']
    returnedStuff = database.getUser(user)
    if returnedStuff == None:
        flash('Incorrect username!')
        return redirect(url_for('landing'))
        print(returnedStuff)

    if pwd != returnedStuff[1]:
        flash('Incorrect password!')
        return redirect(url_for('landing'))
    session['username'] = user
    return redirect(url_for('home'))

@app.route('/auth2', methods=['POST'])
def auth2():
    user, pwd = request.form['username'], request.form['password']
    confirmpwd = request.form['confirmpassword']
    returnedStuff = database.getUser(user)
    if returnedStuff == None:
        if pwd != confirmpwd:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        player_name = request.form['player_name'].strip()
        player_age = request.form['player_age'].strip()
        player_height = request.form['player_height'].strip()
        player_weight = request.form['player_weight'].strip()
        player_jersey = request.form['player_jersey'].strip()

        if player_name == "":
            player_name = "N/A"
        if player_age == "":
            player_age = "N/A"
        if player_height == "":
            player_height = "N/A"
        if player_weight == "":
            player_weight = "N/A"
        if player_jersey == "":
            player_jersey = "N/A"

        database.registerUser(user, pwd, player_name, player_age, player_height, player_weight, player_jersey)

        session['username'] = user
        return redirect(url_for('home'))

    flash('Username is taken')
    return redirect(url_for('register'))

@app.route('/account', methods=['GET'])
def account():
    if 'username' not in session:
        return redirect(url_for('landing'))
    username = session['username']
    userInfo = database.getUser(username)
    #(username, password, team_ids, player_name, player_age, player_height, player_weight, player_jersey)
    print(userInfo)
    name, age, height, weight, jersey = userInfo[3], userInfo[4], userInfo[5], userInfo[6], userInfo[7]
    return render_template('account.html', username = username, name = name, age = age, height = height, weight = weight, jersey = jersey, isownacc = 'yes')

@app.route('/viewing_account', methods=['GET'])
def viewing_account():
    if 'username' not in session:
        return redirect(url_for('landing'))
    view_username = request.args['username']
    if view_username == session['username']:
        return redirect(url_for('account'))
    userInfo = database.getUser(request.args['username'])
    name, age, height, weight, jersey = userInfo[3], userInfo[4], userInfo[5], userInfo[6], userInfo[7]
    return render_template('account.html', username = view_username, name = name, age = age, height = height, weight = weight, jersey = jersey)

@app.route('/update_account_info', methods=['POST'])
def update_account_info():
    if 'username' not in session:
        return redirect(url_for('landing'))
    name, age, height, weight, jersey = request.form['newname'], request.form['newage'], request.form['newheight'], request.form['newweight'], request.form['newjersey']
    username = session['username']
    database.changePlayerName(username, name)
    database.changePlayerAge(username, age)
    database.changePlayerHeight(username, height)
    database.changePlayerWeight(username, weight)
    database.changePlayerJersey(username, jersey)

    return redirect(url_for('account'))

@app.route('/jointeam', methods=["POST"])
def jointeam():
    if 'username' not in session:
        return redirect(url_for('landing'))
    id = database.getTeamIdByInviteCode(request.form['joincode'])
    print('this is yo id: ' + str(id))
    database.addTeamToUser(session['username'], id)
    return redirect(url_for('home'))

@app.route('/create_team', methods=['POST'])
def create_team():
    if 'username' not in session:
        return redirect(url_for('landing'))
    team, sport = request.form['teamname'], request.form['sport']
    database.createTeam(team, sport, session['username'])
    return redirect(url_for('home'))

@app.route('/team', methods=['GET'])
def team():
    if 'username' not in session:
        return redirect(url_for('landing'))
    id = request.args['team']
    teamAdmin = database.getTeamAdmin(id)
    print('teamadmin:', teamAdmin)
    #print(id)
    #print('testing remove from roster')
    #database.removeFromRoster('a', '42c5a762-8637-4400-b53e-cbb9cca81995')
    name, sport= database.getNameByTeamId(id), database.getSportByTeamId(id)
    roster = database.getRosterByTeamId(id)

    print('roster', str(roster))
    print(str(roster[0][0]) == teamAdmin)

    invitecode = database.getInviteByTeamId(id)
    return render_template('team.html', teamID = id, teamname = name, invitecode = invitecode, sport = sport, roster = roster, teamAdmin = teamAdmin, currentUser = session['username'])

@app.route('/teamplays', methods=['GET'])
def teamplays():
    if 'username' not in session:
        return redirect(url_for('landing'))
    print(request.args)
    id = request.args['team']
    teamAdmin = database.getTeamAdmin(id)
    teamname = database.getNameByTeamId(id)
    plays = database.getPlaysByTeamId(id)
    print(plays)
    return render_template('teamplays.html', plays = plays, teamname = teamname, teamID = id, teamAdmin = teamAdmin, currentUser = session['username'])

@app.route('/createplay', methods=['GET'])
def createplay():
    if 'username' not in session:
        return redirect(url_for('landing'))
    id = request.args['team']
    return render_template('createplay.html', teamID = id)

@app.route('/writePlay', methods=['GET'])
def writePlay():
    if 'username' not in session:
        return redirect(url_for('landing'))
    id = request.args['team']
    playname = request.args['playname']
    database.createPlay(session['username'], playname, '', session['username'], id)
    return redirect(url_for('teamplays', team = id))

@app.route('/play')
def sendPlay():
    if 'username' not in session:
        return redirect(url_for('landing'))
    id = request.args['team']
    playid = request.args['playid']
    playname = request.args['play']
    commands = database.getPlay(playid).split('STOP')
    print(commands.pop())
    print('----------')
    for x in range(len(commands)):
        # if command is circle
        if commands[x][0] == "{" :
            commands[x] = json.loads(commands[x])
    print(commands)
    return render_template('play.html', commands = commands, play=playname, teamID = id)

@app.route('/removePlay')
def removePlay():
    if 'username' not in session:
        return redirect(url_for('landing'))
    playid, teamid = request.args['playid'], request.args['teamID']
    database.removePlay(playid, teamid)
    return redirect(url_for('teamplays', team = teamid))

@app.route('/receiveObjects')
def receiveObjects():
    if 'username' not in session:
        return redirect(url_for('landing'))
    # command_list is delimited by keyword 'STOP'
    command_list = ""
    for key in request.args:
        if key != 'id' and key != 'name':
            if key[0:4] == 'path':
                command_list += request.args[key] + 'STOP'
            if key[0:5] == 'click':
                command_list += request.args[key] + 'STOP'
    print(command_list)
    print("--------------------------")
    id = request.args['id']
    playname = request.args['name']
    database.createPlay(session['username'], playname, command_list, session['username'], id)
    return 'it worked'

@app.route('/removePlayer')
def removePlayer():
    if 'username' not in session:
        return redirect(url_for('landing'))
    print(request.args)
    database.removeFromRoster(request.args['username'], request.args['teamID'])
    if session['username'] == request.args['username']:
        return redirect(url_for('home'))
    return redirect(url_for('team', team = request.args['teamID']))


if __name__ == '__main__':
    app.debug = True
    app.run()
