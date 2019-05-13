from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/auth', methods=["POST"])
def auth():
    return "this is supposed to authenticate user"
if __name__ == '__main__':
    app.debug = True
    app.run()
