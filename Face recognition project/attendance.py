# Face Recognition
################################
import cv2
import pandas as pd
import numpy as np
import face_recognition as fr

def attendance():
    fname = 'features.csv'
    at_file = 'attendance.csv'
    try:
        at = pd.read_csv(at_file)
    except:
        at = pd.DataFrame({'name':[],'timestamp':[]})

    try:
        df = pd.read_csv(fname)
    except:
        print('Face Database not found. Halt')
    else:
        fd = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        vid = cv2.VideoCapture(0)
        count = 0
        old_name = ''
        while True:
            ack, img = vid.read()
            if ack:
                faces = fd.detectMultiScale(img, 1.2,10,minSize=(150,150))
                if len(faces) == 1:
                    x,y,w,h = faces[0]
                    face_img = img[y:y+h,x:x+w,:].copy()
                    face_enc = fr.face_encodings(face_img)
                    if len(face_enc) == 1:
                        feats_data = df['enc'].apply(lambda x:eval(x)).values.tolist()
                        matches = fr.compare_faces(face_enc, np.array(feats_data))
                        if True in matches:
                            match_ind = matches.index(True)
                            name = df['name'][match_ind]
                        else:
                            name = 'Unknown'
                        if old_name == name:
                            count += 1
                        else:
                            count == 1
                            old_name = name
                        if count > 5 and name != 'Unknown':
                            from datetime import datetime as dt
                            new_at = pd.DataFrame(
                                {'name':[name],'timestamp':[str(dt.now())]})
                            at = pd.concat(
                                [at,new_at],ignore_index=True, axis=0
                            )
                            at.to_csv(at_file,index=False)
                            print('Attendance Captured')
                            break

                        cv2.putText(img, name,(150,150),
                            cv2.FONT_HERSHEY_PLAIN, 5, (0,0,255),15
                        )                    

                cv2.imshow('Preview', img)  # depends on requirement
                key = cv2.waitKey(1)
                if key == ord('x'):
                    break
        cv2.destroyAllWindows(); cv2.waitKey(1)
        vid.release()