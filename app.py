from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session, send_file
import rds_db as db
from werkzeug.utils import secure_filename
from helpers import *
from parse import *
from flask_cors import CORS
from config import S3_BUCKET
import sys

import os

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
BUCKET = "ctni-bucket"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'html'}
names = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_float(val):
    try:
        num = float(val)
        return num
    except ValueError:
        return val


@app.route('/upload', methods=['POST'])
def upload_file():

    upload_dir = "upload_cache"

    file = request.files['file']
    if file.filename == "":
        print("herea", file=sys.stderr)
        return "Please select a file"

    # if file and allowed_file(file.filename):
    if file:
        # file.filename = secure_filename(file.filename)
        # print(file.filename,file=sys.stderr)
        # print("hereb", file=sys.stderr)

        path_to_file = os.path.join(upload_dir, file.filename)
        file.save(path_to_file)
        print(upload_dir+"/"+file.filename,file=sys.stderr)
        if file.filename == "method":
            print("about to execute methodFile",file=sys.stderr)
            methodFile(path_to_file)


        return "Fi"

@app.route('/groups',methods=['GET'])
def groups():
    if request.method == 'GET':
        groups_list = db.get_groups()
        return jsonify(groups_list)

@app.route('/download', methods=['POST'])
def download_file():
    if request.method == 'POST':
        studiesgrabbed=request.get_data()
        json_data = json.loads(studiesgrabbed)
        global names
        names=json_data
        print("hello back", names)



        # study_name = "Study_ID"
        #
        #
        # for i in (json_data):
        #     print(i)
        #     names.append(i[study_name])

        print("hey you names", json_data)
        return jsonify("hi")

@app.route('/email', methods=['POST'])
def email():
    if request.method == 'POST':
        groupdata=request.get_data()
        GD_json_data = json.loads(groupdata)
        print("json back",GD_json_data)
        # GD_string = groupdata.decode()
        #print("hello back email", type(email_string))
        email_string=GD_json_data[0]

        UG_string=GD_json_data[1]

        print("eeee", UG_string)
        user_id = db.get_user_id_from_email(email_string)
        user_group = db.get_user_groupid_from_UG(UG_string)
        print("gotcha UG", user_group[0][0])
        print("gotcha",user_id[0][0])
        global names
        print("Namesss", names)
        db.update_user_studies_from_email(int(user_id[0][0]),names)
        db.update_UG_studies_from_UG(int(user_group[0][0]),names)
        print("hey you email", email_string)
        return jsonify("hi")



# @app.route("/download/<filename>", methods=['GET'])
# def download(filename):
#     if request.method == 'GET':
#         output = download_file(filename, BUCKET)
#
#         return send_file(output, as_attachment=True)

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
                "Scan_Name": study[6],
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
@app.route('/groups', methods=['GET'])
def groups():
    if request.method == 'GET':
        groups_list = db.get_groups()


        groupsarr = []

        for group in groups_list:
            groupsarr.append(group[0])
        return jsonify(groupsarr)
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
