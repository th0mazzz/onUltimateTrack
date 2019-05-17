import os

from flask import flash, Flask, render_template, redirect, request, session, url_for
from util import database

app = Flask(__name__)
app.secret_key = os.urandom(32)

DIR = os.path.dirname(__file__)
DIR += '/'

DB_FILE = DIR + 'data/borkbook.db'
#database.create_db()

@app.route('/')
def landing():
    return render_template(DIR + 'login.html')




if __name__ == '__main__':
    app.debug = True
    app.run()
