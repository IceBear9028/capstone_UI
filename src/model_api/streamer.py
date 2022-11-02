import datetime
import time

import cv2
import imutils
import platform
import numpy as np
from threading import Thread
from queue import Queue

import mediapipe as mp
# import pygame
from fer import FER
from fer.utils import draw_annotations
# 
from src.model_api.activate_class import model_start, moves_, face_angle_, face_off_, emot_

# 참고할 웹사이트
# http://wandlab.com/blog/?p=94

class Streamer :
    def __init__(self):

        if cv2.ocl.haveOpenCL():
            cv2.ocl.setUseOpenCL(True)
        
        self.capture = None
        self.thread = None
        self.width = 640
        self.height = 360
        self.stat = False
        self.current_time = time.time()
        self.preview_time = time.time()
        self.sec = 0
        self.Q = Queue(maxsize = 128)
        self.started = False
        
        # fps값 조절하는 클래스
        self.fps_prev = 0
        self.fps_setting = 10
        # 단위 : fps

        
        self.models = model_start()

        # mp_face_mesh 는 새로운 모델에서는 사용하지 않음
        # self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_pose = mp.solutions.pose
        self.detector = FER()

        self.passed = 0
        # self.start = pygame.time.get_ticks()
        self.start = datetime.datetime.now()

        self.focus = 0
        self.focus_prob = 0

        self.moving = None
        self.face_angle = None
        self.come_off = None

        #클래스별 집중도 평가에 사용되는 초기값 셋팅 
        # pygame.init()
        emot_.init()
        moves_.init()
        face_angle_.init()
        face_off_.init()


    def run(self, src = 0):
        # 1. 먼저, 카메라를 정지
        self.stop()

        # 2. 웹캠을 통해 이미지 저장
        if platform.system() == 'Windows' :
            self.capture = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        else :
            self.capture = cv2.VideoCapture(src)
        
        # 3. 프레임수를 줄인다
        # 200 -> 200ms = 0.2 초당 1프레임 추출 => 5fps
        #self.capture.set(cv2.CAP_PROP_POS_MSEC, 2000)

        # 3. 이미지를 크기를 재조정
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        # 4. thread 통해서, 동시에 선언한 함수 update()를 실행
        if self.thread is None:
            self.thread = Thread(target=self.update, args = ())
            self.thread.demon = False
            self.thread.start()
        
        self.started = True
        
    def stop(self):
        self.started = False
        
        # capture 변수에 프레임이 저장되어있으면, 정지시킨다.
        if self.capture is not None :
            self.capture.release()
            self.clear()
    
    # Q 자료형에 프레임 한개씩 추가
    def update(self):
        while True:
            if self.started :
                # 1. capture 이용해서 frame 이미지와,
                # 이전 프레임과 현재 프레임이 뽑혔을 때의 시간차이를 구한다.
                time_elapsed = time.time() - self.fps_prev
                # capture 값을 read 하면, (성공여부(bool), frame) 값을 추출한다.
                (grabbed, frame) = self.capture.read()

                # 2. 프레임의 시간차이가 설정한 fps 속도에 만족했을 때 이미지를 Q 자료형에 넣는다.
                # -> fps 속도에 만족하지 않는 경우, 이미지 프레임은 그대로 버려진다
                if time_elapsed > 1./self.fps_setting:
                    self.fps_prev = time.time()
                    if grabbed :
                        self.Q.put(frame)
                # grabbed(성공여부) = True 이면 Queue 자료형에 프레임을 하나씩 추가한다.

    # Q 자료형 담긴 값들 리셋함               
    def clear(self):
        with self.Q.mutex:
            self.Q.queue.clear()
    
    #  read함수 : Q자료형에서 frame 을 읽는다.
    def read(self):
        return self.Q.get()


    def blank (self):
        return np.ones(shape = [self.height, self.width, 3], dtype=np.uint8)

    def bytescode(self):
        if not self.capture.isOpened():
            frame = self.blank()
        
        else:
            frame = imutils.resize(self.read(), width=int(self.width))

            if self.stat:
                cv2.rectangle( frame, (0,0), (120,30), (0,0,0), -1)
                fps = 'FPS : ' + str(self.fps())
                cv2.putText  ( frame, fps, (10,20), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1, cv2.LINE_AA)

        return cv2.imencode('.jpg',frame)[1].tobytes()


    # def focus_result(self):
    #     with self.mp_face_mesh.FaceMesh(max_num_faces = 1, refine_landmarks=True,min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    #         with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    #             if not self.capture.isOpened():
    #                 frame = self.blank()
    #             else:
    #                 frame = self.read()
    #                 if frame.any() == False :
    #                     print("Ignoring empty camera frame.")
    #                     self.capture.release()
    #                     cv2.destroyAllWindows()
                    
    #                 frame.flags.writeable = False
    #                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #                 fm_results = face_mesh.process(frame)
    #                 #pose_results = pose.process(frame)

    #                 frame.flags.writeable = True
    #                 frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    #                 emotions = self.detector.detect_emotions(frame)
    #                 frame = cv2.flip(frame, 1)

    #                 try:
    #                     fer_result = fer.detect(frame, emotions)
    #                     #moving = moves_ZX.detect(pose_results)
    #                     self.come_off, self.face_angle = off_angle.detect(frame, fm_results)

    #                     self.passed = pygame.time.get_ticks() - self.start

    #                     if self.passed > 500:
    #                         plus = [self.moving, self.face_angle, self.come_off]
    #                         row = fer_result + plus
    #                         start = pygame.time.get_ticks()
    #                         self.passed = 0

                            
    #                         fer.init()
    #                         moves_ZX.init()
    #                         off_angle.init()

    #                         try:
    #                             X1 = self.scalar.transform(np.array(row).reshape(1,-1))
    #                             self.focus = self.model.predict(X1)[0]
    #                             self.focus_prob = self.model.predict_proba(X1)[0][1]


    #                             self.current_time = datetime.datetime.now()
    #                             print(self.current_time)
    #                             print(self.focus_prob)
    #                             #print(self.focus)
    #                             #print(self.focus_prob)

    #                             return self.current_time, self.focus_prob
                            
    #                         except Exception as e:
    #                             print("예외가 발생하였습니다.", e)
    #                             self.current_time = datetime.datetime.now()
    #                             self.focus_prob = 0
                                
    #                             return self.current_time, self.focus_prob
                            

    #                 except Exception as e:
    #                     print("예외가 발생하였습니다.", e)
    #                     self.current_time = datetime.datetime.now()
    #                     self.focus_prob = 0
    #                     return self.current_time, self.focus_prob
    #     # self.capture.release()
    #     cv2.destroyAllWindows()
    
    def focus_result(self,mod):
        # global    df_to_save
        try:
            with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose :
                if not self.capture.isOpened():
                    frame = self.blank()
                else:
                # while cap.isOpened():
                    self.current_time = datetime.datetime.now()
                    frame = self.read()
                    if frame.any() == False :
                        print("Ignoring empty camera frame.")
                        self.capture.release()
                        cv2.destroyAllWindows()
                    ######################################## 
                    #각 모듈 불러오기
                    frame.flags.writeable = False
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pose_results = pose.process(frame)
                    frame.flags.writeable = True
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    emotions = self.detector.detect_emotions(frame)
                    ########################################
                    try:
                        fer_result = emot_.detect(emotions)
                        moving = moves_.detect(pose_results)
                        face_angle = face_angle_.detect(pose_results)
                        face_off = face_off_.detect(frame, pose_results)
                    except Exception as e:
                        pass
                    ########################################
                    # self.passed = pygame.time.get_ticks() - self.start # 시간측정
                    distance_t = datetime.datetime.now() - self.start
                    
                    self.passed = int(distance_t.total_seconds() * (10**6))
                    if self.passed > 500 : # 0.5초, 1000 == 1초
                        # self.start = pygame.time.get_ticks()
                        self.start = datetime.datetime.now()
                        self.passed = 0
                        plus = [moving,face_angle,face_off] #탐지한 값들을 List로 합침
                        row = fer_result + plus
                        emot_.init() # 데이터 초기화
                        moves_.init()
                        face_angle_.init()
                        face_off_.init()
                        try:
                            # if how == "extract":
                                #데이터 추출하고 저장하기
                                # row.insert(0,name)
                                # df_to_save = df_to_save.append([row])
                            # if how == "valid":
                            #     #모델로 검증하기
                            #     X1 = np.array(row).reshape(1,-1)
                            #     focus = self.models[mod].predict(X1)[0]
                            #     focus_prob = self.models[mod].predict_proba(X1)[0][1]
                                # valid_row = [name,focus, focus_prob]
                                # df_to_save = df_to_save.append([valid_row])
                            # else :
                            X1 = np.array(row).reshape(1,-1)
                            focus = self.models[mod].predict(X1)[0]
                            self.focus_prob = self.models[mod].predict_proba(X1)[0][1]
                            # self.current_time = datetime.datetime.now()
                                # df_to_save = pd.DataFrame()

                        except Exception as e:
                            focus = 0
                            self.focus_prob = 0
                            # self.current_time = datetime.datetime.now()
                    

                    return self.current_time, self.focus_prob
                            
                    # frame = cv2.flip(frame, 1)
                    
            
                    # if how == 'run':
                    #     # cv2.imshow(f'{name}', frame)
                    #     cv2.putText(frame, str(focus), (90,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                    #     cv2.putText(frame, str(focus_prob), (90,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            self.capture.release()            

        except Exception as e:
            print(e)


    # def fps(self):
        
    #     self.current_time = time.time()
    #     self.sec = self.current_time - self.preview_time
    #     self.preview_time = self.current_time
        
    #     if self.sec > 0 :
    #         fps = round(1/(self.sec),1)
            
    #     else :
    #         fps = 1
            
    #     return fps


    def __exit__(self) :
        print( '* streamer class exit')
        self.capture.release()

    