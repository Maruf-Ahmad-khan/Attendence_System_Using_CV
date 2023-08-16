# Face Registration
################################
import cv2
import pandas as pd
import face_recognition as fr
import numpy as np

def register(name):
    fname = 'features.csv'
    try:
        df = pd.read_csv(fname)
    except:
        df = pd.DataFrame({'name':[], 'enc':[]})

    fd = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    vid = cv2.VideoCapture(0)
    counter = 0
    names = []
    feats = []

    while True:
        ack, img = vid.read()
        if ack:
            faces = fd.detectMultiScale(img, 1.2,10,minSize=(150,150))
            if len(faces) == 1:
                x,y,w,h = faces[0]
                face_img = img[y:y+h,x:x+w,:].copy()
                face_enc = fr.face_encodings(face_img)
                if len(face_enc) == 1:
                    counter += 1
                    names += [name]
                    feats += [face_enc[0].tolist()]                
                if counter == 20:
                    f = pd.DataFrame({'name':names, 'enc':feats})
                    df = pd.concat([df,f], axis = 0, ignore_index=True)
                    df.to_csv(fname)
                    break

            cv2.imshow('Preview', img)  # depends on requirement
            key = cv2.waitKey(1)
            if key == ord('x'):
                break
    cv2.destroyAllWindows(); cv2.waitKey(1)
    vid.release()