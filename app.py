from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session, send_file
import rds_db as db
from werkzeug.utils import secure_filename
from helpers import *
from flask_cors import CORS
from config import S3_BUCKET
from s3_upload import *

import os

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
BUCKET = "ctni-bucket"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_float(val):
    try:
        num = float(val)
        return num
    except ValueError:
        return val

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     file = request.files['file']
#     if file.filename == "":
#         return "Please select a file"
#
#     if file and allowed_file(file.filename):
#         file.filename = secure_filename(file.filename)
#         output = upload_file_to_s3(file, S3_BUCKET)
#         return str(output)
#
#     else:
#         return redirect("/")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

@app.route('/studies/<email>/<auth0id>', methods=['GET'])
def studies(email, auth0id):
    print("App.py",email)

    if request.method == 'GET':
        study_list = db.get_studies_scans(email)
        db.insert_account(email, auth0id)
        studiesArr = []

        for study in study_list:
            studiesArr.append({
                        'Study_ID': study[0],
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
                        "SliceOrient": study[17]
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

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)

        return redirect("/storage")
