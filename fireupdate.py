import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import time
import os
import pickle
now=datetime.now()
y=now.strftime("%Y")
m=now.strftime("%m")
d=now.strftime("%d")
date=d+"-"+m+"-"+y
data = {}
with open('encodings', 'rb') as fr:
    try:
        while True:
            data=pickle.load(fr)
    except EOFError:
        pass
known_face_names=[]
t={}
for i in data:
    try:
        print(data[i][0])
        name1=data[i][0][:data[i][0].index('.')]
    except:
        name1=data[i][0]
    known_face_names.append(name1)
cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://attendance-system-b1445.firebaseio.com/'})
file = open('newtest.txt','a')
file.close()
file = open('newtest.txt','r')
a=file.readline(1)
print(a)
if a!=date:
    file.close()
    file = open('newtest.txt','w')  
    file.write(date)
    file.close()
    ter=date+' Register'
    ref = db.reference(ter)
    for i in known_face_names:
        if not i in t:
            t[i]='Absent'
    ref.update(t)
else:
    file.close()
time.sleep(5)
file1=open(date+' Register','r')
while True:
    d={}
    face_names=file1.readlines()
    for i in face_names:
        print(i,len(i))
        if i!='\n' or i[:-1]!='Unknown':
            d[i[:-1]]=['Present','Outside']
    

    ter=date+' Register'
    if len(d)>0:
        print(d)
        d.pop('Unknown',None)
    if len(d)>0 :
        ref = db.reference(ter)
        ref.update(d)