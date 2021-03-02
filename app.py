from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session
import rds_db as db
from werkzeug.utils import secure_filename
from helpers import *
from flask_cors import CORS
from config import S3_BUCKET
import os

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
BUCKET = "ctni-bucket"

# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
#
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_float(val):
    try:
        num = float(val)
        return num
    except ValueError:
        return val

@app.route('/upload', methods=['POST'])
def upload_file():

<<<<<<< HEAD
    # A
    #print("hereA", file=sys.stderr)
=======
>>>>>>> bdc9f8b63ffdf868e807a9ba6a5626016b984a4f
    file = request.files['file']

    if file.filename == "":
<<<<<<< HEAD
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
=======
        return "Please select a file"

    # if file and allowed_file(file.filename):
    file.filename = secure_filename(file.filename)
    output   	  = upload_file_to_s3(file, S3_BUCKET)
    return jsonify(file.filename)
>>>>>>> bdc9f8b63ffdf868e807a9ba6a5626016b984a4f

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
            studiesArr.append({
                        'Study_ID': study[0],
                        "Study_Owner": study[1],
                        "Study_Description": study[2],
                        "Study_Name": study[3],
                        "Study_Rating": study[4],
                        "Study_Comments": study[5],
                        "Scan_ID": study[6],
                        "Scan_Name" : study[7],
                        "Scan_Time": str(study[8]),
                        "FOV": study[9],
                        "Echotime": is_float(study[10]),
                        "Repetitiontime": is_float(study[11]),
                        "Nrepetition": is_float(study[12]),
                        "SpatResol": study[13],
                        "SliceThick": is_float(study[14]),
                        "NSlice": is_float(study[15]),
                        "SliceGap": is_float(study[16]),
                        "SliceDistance": is_float(study[17]),
                        "SliceOrient": study[18]
                        })
<<<<<<< HEAD
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
=======
        return jsonify(studiesArr)
>>>>>>> bdc9f8b63ffdf868e807a9ba6a5626016b984a4f
