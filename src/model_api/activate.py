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
from activate_class import model_start, off_angle, moves_ZX, fer

# 1. 초기값 설정
start = model_start()

scalar = start[0]
model = start[1]

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