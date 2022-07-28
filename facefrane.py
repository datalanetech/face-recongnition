import cv2
import face_recognition
import pytz
import pickle
import csv
import numpy as np
from datetime import datetime
import os
import time  # This is required to include time module.

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        images= os.listdir('./images')
        data ={}
with open('./encodings', 'rb') as fr:
    try:
        data=pickle.load(fr)
    except EOFError:
        pass
known_face_encodings=[]
known_face_names=[]
for i in data:
    known_face_names.append(data[i][0][:-4])
    known_face_encodings.append(data[i][1])

        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()