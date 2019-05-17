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
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/auth', methods=["POST"])
def auth():
    user, pwd = request.form['username'], request.form['password']
    if 'confirmpassword' not in request.form:
        returnedStuff = database.getUser(user)
        if returnedStuff == None:
            flash('Incorrect username!')
            return redirect(url_for('login'))
            print(returnedStuff)

        if pwd != returnedStuff[1]:
            flash('Incorrect password!')
            return redirect(url_for('login'))
    else:
        confirmpwd = request.form['confirmpassword']
        returnedStuff = database.getUser(user)
        if returnedStuff == None:
            if pwd != confirmpwd:
                flash('Passwords do not match')
                return redirect(url_for('register'))

        flash('Username is taken')
        return redirect(url_for('register'))

        print('asjdasdnn')

    player_name = request.form['player_name']
    player_age = request.form['player_age']
    player_height = request.form['player_height']
    player_weight = request.form['player_weight']
    player_jersey = request.form['player_jersey']

    database.registerUser(user, pwd, player_name, player_age, player_height, player_weight, player_jersey)

    return redirect(url_for('home'))



if __name__ == '__main__':
    app.debug = True
    app.run()
