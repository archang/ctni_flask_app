
from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session
from flask import Response,send_file
import re
import rds_db as db
import datetime
import json
from s3_upload import list_files, download_file, upload_file
from werkzeug.utils import secure_filename
from helpers import *
import sys
from flask_cors import CORS
from config import S3_BUCKET
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
BUCKET = "ctni-bucket"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/upload', methods=['POST'])
def upload_file():

    # A
    #print("hereA", file=sys.stderr)
    file = request.files['file']



    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

    # C.
    if file.filename == "":
    #    print("herec", file=sys.stderr)
        return "Please select a file"

    # D.
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        #print(file.filename, file=sys.stderr)
        output   	  = upload_file_to_s3(file, S3_BUCKET)
        #print("hered", file=sys.stderr)
        return str(output)

    else:
        #print("hereredirect", file=sys.stderr)
        return redirect("/")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

@app.route('/studies', methods=['GET'])
def studies():
    if request.method == 'GET':
        study_list = db.get_studies_scans()
        studiesArr = []

        for study in study_list:
            studiesArr.append({'Study_ID': study[0],
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
        return jsonify(studiesArr)
        #
        # print(details)
        # return(json.dumps({'studies' : studies}, default=str))
        # return(jsonify(details))

@app.route("/storage")
def storage():
    contents = list_files("flaskdrive")
    return render_template('storage.html', contents=contents)

# @app.route("/upload", methods=['POST'])
# def upload():
#     if request.method == "POST":
#         f = request.files['file']
#         f.save(os.path.join(UPLOAD_FOLDER, f.filename))
#         upload_file(f"uploads/{f.filename}", BUCKET)
#
#         return redirect("/storage")