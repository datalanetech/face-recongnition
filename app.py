# -*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, render_template, request, session, g, Response
import json
import sys
import os
import sqlite3
import capture as cap
app = Flask(__name__)
#------------------------------------------------------------------
#------------------------------------------------------------------
import face_recognition
import cv2
import pytz
import pickle
import csv
import numpy as np
from datetime import datetime
import os
import time as t # This is required to include time module.
now = datetime.now()
y=now.strftime("%Y")
m=now.strftime("%m")
d=now.strftime("%d")
date=d+"-"+m+"-"+y

IST=pytz.timezone('Asia/Calcutta')
dtm=str(datetime.now(IST))
time=dtm[11:16]
current_time=int(time[-2:])
print(time)
images= os.listdir('./images')
# print(images)
data ={}
with open('./encodings', 'rb') as fr:
    try:
        data=pickle.load(fr)
    except EOFError:
        pass
known_face_encodings=[]
known_face_names=[]
for i in data:
    known_face_names.append(str(i) + ' ' + data[i][0][:-4])
    known_face_encodings.append(data[i][1])
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
d=dict()

#-----------------------------------------------------------------
#-----------------------------------------------------------------

#---------------sqlite---------------------------------------#
# check if the database exist, if not create the table and insert a few lines of data
DATABASE = "./database.db"


if not os.path.exists(DATABASE):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, name VARCHAR, empid VARCHAR);")
    conn.commit()
    cur.execute("INSERT INTO users VALUES('1', 'Nidhin Harilal', '4');")
    cur.execute("INSERT INTO users VALUES('2', 'Param Goswami', '6');")
    conn.commit()
    conn.close()


# helper method to get the database since calls are per thread,
# and everything function is a new thread when called
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# helper to close
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def first():
    
    cur = get_db().cursor()
    res = cur.execute("select * from Sheet2")
    
    return render_template("index.html", users=res)
#--------------------------------------------------------------------------------------------
def gen():
    images= os.listdir('./images')
    print("gen()")
    data ={}
    with open('./encodings', 'rb') as fr:
        try:
            data=pickle.load(fr)
        except EOFError:
            pass
    known_face_encodings=[]
    known_face_names=[]
    for i in data:
        known_face_names.append(str(i) + ' ' + data[i][0][:-4])
        known_face_encodings.append(data[i][1])
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    d=dict()
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    while True:
            
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                #print(face_distances,type(face_distances))
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                if name not in d:
                    d[name]=1
                else:
                    d[name]=d[name]+1
                    if (d[name]==4) :
                        file1=open(date+' Register','a')
                        file1.write(name +'\n')
                        file1.close()
                face_names.append(name)

        process_this_frame = not process_this_frame

        font                   = cv2.FONT_HERSHEY_DUPLEX
        bottomLeftCornerOfText = (30,450)
        fontScale              = 0.65
        fontColor              = (255,255,255)
        lineType               = 2
        st="Hello "
        for facename in face_names:
            ve=''
            try:
                ve=facename[facename.index(' ')+1:]
            except:
                ve=facename

            st+=ve+' '+','

        cv2.putText(frame,st, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



#-------------------------------------------------------------
@app.route("/new/<name>", methods=['GET', 'POST'])
def second(name):
    print("New!!")
    # video_capture.release()
    # cv2.destroyAllWindows()


    cur = get_db().cursor()
    res = cur.execute("select * from Sheet2 ")
    cap.start(name)    
    print("picture taken!")
    import subprocess
    subprocess.call("script.sh", shell=True)
    t.sleep(2)
    print("back to app.py after train!")
    return redirect(url_for('first'))



#_-------------------------videfeed
@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
#--------------------------new Employee

@app.route('/entry',  methods=['GET', 'POST'])
def newentry():
    import subprocess
    subprocess.call('entry.sh', shell=True)
    return redirect(url_for('first'))

#---------------------------New Page index2
@app.route('/video')
def newpage():
    cv2.destroyAllWindows()
    print("video")
    return render_template("index2.html")
# ======== Main ============================================================== #
if __name__ == "__main__":
    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    app.run(debug=True, use_reloader=True)
