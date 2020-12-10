from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session
from flask import Response,send_file
import re
import rds_db as db
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST':
        User_ID = request.form['User_ID']
        Username = request.form['Username']
        Password = request.form['Password']
        Role = request.form['Role']
        Blocked = request.form['Blocked']
        db.insert_account(User_ID, Username, Password, Role,Blocked)
        details = db.get_account()
        #print(details)
        for detail in details:
            var = detail
        return render_template('register.html', var=var)



@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    #if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
       # username = request.form['username']
        #password = request.form['password']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        #account = cursor.fetchone()
        #if account:
        #    session['loggedin'] = True
        #    session['id'] = account['id']
        #    session['username'] = account['username']
        #    msg = 'Logged in successfully !'
        #    return render_template('index.html', msg = msg)
        #else:
        #    msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)



@app.route('/about')
def about():
    return render_template('about.html')