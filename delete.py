import os
import pickle

images= os.listdir('.\\images')
n=len(images)
imaged={}
for i in range(n):
    imaged[int(images[i].split('_')[0])]=1

with open('dictionary','rb') as fp:
    d=pickle.load(fp)
with open('encodings','rb') as fp:
    data=pickle.load(fp)
newd={}
newdata={}
for i in d:
    try:
        imaged[i]
        newd[i]=d[i]
        newdata[i]=data[i]
    except:
        print(i)
        pass
with open('dictionary','wb+') as fp:
    pickle.dump(newd,fp)
with open('encodings','wb+') as fp:
    pickle.dump(newdata,fp)