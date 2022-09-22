import pickle as pkl
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

with open('model.pkl','rb') as f:
    pickle = pkl.load(f)
    scalar = pickle[1]
    model = pickle[0]

class off_angle: 
    def init():
        global off_records, angle_records
        off_records = [0]
        angle_records = []

    def detect(image, face_mesh_results):
        for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
            for id, lm in enumerate(face_landmarks.landmark):
                shape = image.shape
                landmark_x = int(lm.x * shape[1])
                landmark_y = int(lm.y * shape[0])
                if id == 1 :
                    Nose=[landmark_x,landmark_y]
                if id == 127 :
                    Head_L=[lm.x,lm.y]
                if id == 356 :
                    Head_R=[lm.x,lm.y]
        off_distance = abs(Nose[0]-shape[1]/2)
        off_records.append(off_distance)
        come_off = max(off_records)-min(off_records)
        
        
        x_cord = abs(Head_L[0]-Head_R[0])
        z_cord = abs(Head_L[1]-Head_R[1])
        angle = round(math.atan2(x_cord/z_cord,2),2)*90-50
        if angle >90:
            angle = 90
        if angle < 0 :
            angle = 0
        angle_records.append(angle)
        face_angle = round(sum(angle_records)/len(angle_records))

        
        return come_off, face_angle

class moves_ZX:
    def init():
        global mX_start,rX_start, list_xX, list_yX, movement_recordX
        mX_start = pygame.time.get_ticks()
        rX_start = pygame.time.get_ticks()
        list_xX, list_yX, movement_recordX = [],[],[0]
        for k in range (33):
            list_xX.append(0)
            list_yX.append(0)


    def detect(results):
        global mX_start
        mX_passed = pygame.time.get_ticks() - mX_start
        if mX_passed > 50: 
            movement = 0
            delta = 0
            num_landmark = 0
            i=0
            for id, lm in enumerate(results.pose_landmarks.landmark):
                if lm.visibility > 0.7:
                    num_landmark +=1
                    delta_x = lm.x - list_xX[id]
                    delta_y = lm.y - list_yX[id]
                    delta = math.sqrt((delta_x * delta_x) + (delta_y * delta_y)) * 100
                    movement += delta
                else:
                    delta = 0
                del list_xX[id],list_yX[id]
                list_xX.insert(id,lm.x)
                list_yX.insert(id,lm.y)
            movement = movement/ num_landmark
            mX_passed = 0
            mX_start = pygame.time.get_ticks()
            movement_recordX.append(movement)
        if len(movement_recordX) == 2: # 영상별로 첫 번째 움직임 데이터는 불필요하여 삭제
            del movement_recordX[0]
            movement_recordX.append(0)
        movingX = round(sum(movement_recordX)/len(movement_recordX),3)
        return movingX
                            #movement = rou

class fer:
    def init():
        global angry_list, disgust_list, fear_list, happy_list, sad_list, surprise_list, neutral_list,emotion_list
        angry_list = [0]
        disgust_list = [0]
        fear_list = [0]
        happy_list = [0]
        sad_list = [0]
        surprise_list = [0]
        neutral_list = [0]
        emotion_list = [0,0,0,0,0,0,0]
        
    def detect(frame,emotions):
        try:
            for idx, data in enumerate(emotions[0]['emotions']):
                emotion=emotions[0]['emotions'][data]
                del emotion_list[idx]
                emotion_list.insert(idx,emotion)
            if emotion_list[6] != 0:
                angry_list.append(emotion_list[0])
                disgust_list.append(emotion_list[1])
                fear_list.append(emotion_list[2])
                happy_list.append(emotion_list[3])
                sad_list.append(emotion_list[4])
                surprise_list.append(emotion_list[5])
                neutral_list.append(emotion_list[6])
        except IndexError:
            pass
        if sum(neutral_list) == 0:
            fer_result = [0,0,0,0,0,0,0]
        else :
            fer_result = [sum(angry_list)/len(angry_list),sum(disgust_list)/len(disgust_list),sum(fear_list)/len(fear_list),sum(happy_list)/len(happy_list),sum(sad_list)/len(sad_list),sum(surprise_list)/len(surprise_list),sum(neutral_list)/len(neutral_list)]
        return fer_result

###################################################

import cv2
import numpy as np
import mediapipe as mp
import itertools
import math
import glob,os
import csv
import pygame
from fer import FER
from fer.utils import draw_annotations

cap = cv2.VideoCapture(0)
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic
detector = FER()

passed = 0
start = pygame.time.get_ticks()
pygame.init()
fer.init()
moves_ZX.init()
off_angle.init()
focus = 0
focus_prob = 0 
#try:   
with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose :
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                cap.release()
                cv2.destroyAllWindows()
            ######################################## 
            #각 모듈 불러오기
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            fm_results = face_mesh.process(image)
            pose_results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            emotions = detector.detect_emotions(image)
            image = cv2.flip(image, 1)
            ########################################
            #데이터 추출
            try:
                fer_result = fer.detect(image,emotions)
                moving = moves_ZX.detect(pose_results)
                come_off , face_angle = off_angle.detect(image, fm_results)
            
            except Exception as e:

                    print("예외가 발생했습니다.", e)
            ########################################
            passed = pygame.time.get_ticks() - start # 시간측정
            if passed > 500 : # 2초, 1000 == 1초
                plus = [moving, face_angle,come_off] #탐지한 값들을 List로 합침
                row = fer_result + plus
                start = pygame.time.get_ticks()
                passed = 0
                fer.init() # 2초간의 데이터 초기화
                moves_ZX.init()
                off_angle.init()
                try:
                    X1 = scalar.transform(np.array(row).reshape(1,-1))
                    focus = model.predict(X1)[0]
                    focus_prob = model.predict_proba(X1)[0][1]

                except Exception as e:

                    print("예외가 발생했습니다.", e)

            # Make Detections

            cv2.putText(image, 'CLASS'
                                , (95,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

            cv2.putText(image, str(focus)
                        , (90,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

            # Display Probability
            cv2.putText(image, 'PROB'
                        , (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(round(focus_prob ,2))
                        , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow('Blink', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
#except Exception as e:
    #print("예외가 발생했습니다.", e)  
#except Exception as e:
#print("예외가 발생했습니다.", e)                
cap.release()
cv2.destroyAllWindows()