import os

from flask import Flask, render_template, redirect, request, session, url_for
from util import database

app = Flask(__name__)
app.secret_key = os.urandom(32)

DB_FILE = 'data/borkbook.db'
database.create_db()

@app.route('/')
def landing():
    return render_template('base.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/auth', methods=["POST"])
def auth():

if __name__ == '__main__':
    app.debug = True
    app.run()
