from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session
from flask import Response,send_file
import re
import rds_db as db
import datetime
import json

app = Flask(__name__)

def is_float(val):
    try:
        num = float(val)
        return num
    except ValueError:
        return val



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

@app.route('/users', methods=['GET'])
def users():
    if request.method == 'GET':
        details = db.get_account()
        for detail in details:
            var = detail
        return(jsonify(details))

@app.route('/studies', methods=['GET'])
def studies():
    if request.method == 'GET':
        study_list = db.get_studies_scans()
        studies=[]

        for study in study_list:
            studies.append({'Study_ID': study[0],
                        "Study_Description": study[1],
                        "Study_Name": study[2],
                        "Study_Rating": study[3],
                        "Study_Comments": study[4],
                        "Scan_ID": study[5],
                        "Scan_Name" : study[6],
                        "Scan_Time": str(study[7]),
                        "FOV": study[8],
                        "Echotime": is_float(study[9]),
                        "Repetitiontime": is_float(study[10]),
                        "Nrepetition": is_float(study[11]),
                        "SpatResol": study[12],
                        "SliceThick": is_float(study[13]),
                        "NSlice": is_float(study[14]),
                        "SliceGap": is_float(study[15]),
                        "SliceDistance": is_float(study[16]),
                        "SliceOrient": study[17],
                            "Study_Owner" : study[18],
                        })
        return jsonify(studies)
        #
        # print(details)
        # return(json.dumps({'studies' : studies}, default=str))
        # return(jsonify(details))

# @app.route('/users',methods=['GET'])
# def users():
#     from sqlalchemy.orm import scoped_session, sessionmaker, Query
#     db_session = scoped_session(sessionmaker(bind=engine))
#     return(jsonify(db_session.Account.query.all()))
#     item_list=[]
#     for item in db_session.query(Account.User_ID, Account.Username,Account.Role).all():
#         item_list+=item
#     return(jsonify(item_list))
#
# @app.route('/scans',methods=['GET'])
# def scans():
#     from sqlalchemy.orm import scoped_session, sessionmaker, Query
#     db_session = scoped_session(sessionmaker(bind=engine))
#     # return(jsonify(db_session.Account.query.all()))
#     item_list = db_session.query(Scan.Scan_ID, Scan.SliceOrient).all()
#     items = []
#     #
#     for item in item_list:
#         items.append({'Scan_ID:' : item.Scan_ID, 'SliceOrient' : item.SliceOrient})
#
#     return(jsonify({'scan' : items}))
#     # return jsonify(item_list)
#     # return jsonify(Scan.metadata.tables['scan'].columns.keys())
