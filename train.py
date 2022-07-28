import os
import face_recognition
import pickle
import pandas as pd
images= os.listdir('.\\images')
print(images)
#images=["karthikeya.jpg","vedanta.png","reddy.jpg","chenna.jpeg","ronak.jpeg","vraj.jpeg"]
filename='encodings'
known_face_encodings=[]
try:
    with open('dictionary','rb') as fp:
        d=pickle.load(fp)
except:
    d={}
    filen='dictionary'
    # with open(filen,'wb+') as fp:
    #     pickle.dump(d,fp)
try:
    with open(filename,'rb') as fp:
        dencod=pickle.load(fp)
except:
    dencod={}
for i in images:
    
    c=i.split('_')
    c,e=int(c[0]),c[1]
    try:
        d[c]
    except:
        d[c]=1
        dencod[c]=e,face_recognition.face_encodings(face_recognition.load_image_file('.\\images\\'+i))[0]
with open('dictionary','wb+') as fp:
    pickle.dump(d,fp)
#         known_face_encodings.append(c)
with open(filename,'wb+') as fp:
    pickle.dump(dencod,fp)