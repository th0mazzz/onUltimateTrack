import os

from flask import flash, Flask, render_template, redirect, request, session, url_for

from util import database

app = Flask(__name__)
app.secret_key = os.urandom(32)

#DIR = os.path.dirname(__file__)
#DIR += '/'

#DB_FILE = DIR + 'data/borkbook.db'

#print(DB_FILE)

database.create_db()
#database.insert_test_data()

@app.route('/')
def landing():
    if 'username' not in session:
        return render_template('login.html')
    return redirect(url_for('home'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('landing'))
    print(database.getTeamsByUser(session['username']))
    teams = []
    for id in database.getTeamsByUser(session['username']):
        print(id)
        if len(id) > 1:
            teams.append([database.getNameByTeamId(id), id, database.getSportByTeamId(id)])
    return render_template('home.html', username = session['username'], teams= teams)

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

        player_name = request.form['player_name']
        player_age = request.form['player_age']
        player_height = request.form['player_height']
        player_weight = request.form['player_weight']
        player_jersey = request.form['player_jersey']


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
    return render_template('account.html', username = username, name = name, age = age, height = height, weight = weight, jersey = jersey)

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
    print(id)
    name, sport= database.getNameByTeamId(id), database.getSportByTeamId(id)
    roster = database.getRosterByTeamId(id)
    return render_template('team.html', teamID = id, roster = roster)

@app.route('/teamplays', methods=['GET'])
def teamplays():
    if 'username' not in session:
        return redirect(url_for('landing'))
    print(request.args)
    id = request.args['team']
    teamname = database.getNameByTeamId(id)
    plays = database.getPlaysByTeamId(id)
    print(plays)
    return render_template('teamplays.html', plays = plays, teamname = teamname, teamID = id)

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
def play():
    if 'username' not in session:
        return redirect(url_for('landing'))
    return render_template('play.html')

@app.route('/receiveObjects')
def receiveObjects():
    if 'username' not in session:
        return redirect(url_for('landing'))
    print(request.args)
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.debug = True
    app.run()
