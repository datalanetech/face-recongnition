import face_recognition
import cv2
import pytz
import pickle
import csv
import numpy as np
from datetime import datetime
import os
import time 
from datetime import datetime
now = datetime.now()
y=now.strftime("%Y")
m=now.strftime("%m")
d=now.strftime("%d")
date=d+"-"+m+"-"+y
video_capture = cv2.VideoCapture(0)
d = {}
with open('encodings', 'rb') as fr:
    try:
        while True:
            d=pickle.load(fr)
    except EOFError:
        pass
known_face_encodings=[]
known_face_names=[]
for i in d:
    try:
        name1=d[i][0][:d[i][0].index('.')]
    except:
        name1=d[i][0]
    known_face_names.append(name1)
    known_face_encodings.append(d[i][1])
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
d=dict()
y=0
while True:
    #y=y+1
    if y==3:
        y=0
    ret, frame = video_capture.read()
    try:
        small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
        rgb_small_frame = small_frame[:, :, ::-1]
        if y%3==0:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index] and (0.5>np.min(face_distances)):
                    name = known_face_names[best_match_index]
                else:
                    name="Unknown"
                if name not in d:
                    d[name]=1 
                else:
                    d[name]=d[name]+1
                    if d[name]==3:
                        d[name]=0
                        file1=open(date+' Register','a')
                        file1.write(name+'\n')
                        file1.close()

                face_names.append([name,1-np.min(face_distances)])
        
        process_this_frame = not process_this_frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 1
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            right *= 1
            bottom *= 1
            left *= 1

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name[0]+' '+str((name[1])*100)[:4], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        pass
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
lines=[]
for i in d:
    lines.append(i)

writeFile.close()