import time
import cv2
import imutils
import platform
import numpy as np
from threading import Thread
from queue import Queue

import mediapipe as mp
import pygame
from fer import FER
from fer.utils import draw_annotations
from src.model_api.activate_class import model_start, off_angle, moves_ZX, fer


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

        
        # focus_result() 함수에 사용되는 초기변수들
        self.start = model_start()
        self.scalar = self.start[0]
        self.model = self.start[1]

        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_pose = mp.solutions.pose
        self.detector = FER()

        self.passed = 0
        self.start = pygame.time.get_ticks()

        self.focus = 0
        self.focus_prob = 0

        self.moving = None
        self.face_angle = None
        self.come_off = None

        pygame.init()
        fer.init()
        moves_ZX.init()
        off_angle.init()

    def run(self, src = 0):
        # 1. 먼저, 카메라를 정지
        self.stop()

        # 2. 웹캠을 통해 이미지 저장
        if platform.system() == 'Windows' :
            self.capture = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        else :
            self.capture = cv2.VideoCapture(src)
        
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
        
    def update(self):

        while True:
            if self.started :
                # capture 값을 read 하면, (성공여부(bool), frame) 값을 추출한다.
                (grabbed, frame) = self.capture.read()
                # grabbed(성공여부) = True 이면 Queue 자료형에 프레임을 하나씩 추가한다.
                if grabbed :
                    self.Q.put(frame)
                    
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


    def focus_result(self):
        with self.mp_face_mesh.FaceMesh(max_num_faces = 1, refine_landmarks=True,min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
            with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                if not self.capture.isOpened():
                    frame = self.blank()
                else:
                    frame = self.read()
                    if frame.any() == False :
                        print("Ignoring empty camera frame.")
                        self.capture.release()
                        cv2.destroyAllWindows()
                    
                    frame.flags.writeable = False
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    fm_results = face_mesh.process(frame)
                    pose_results = pose.process(frame)

                    frame.flags.writeable = True
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                    emotions = self.detector.detect_emotions(frame)
                    frame = cv2.flip(frame, 1)

                    try:
                        fer_result = fer.detect(frame, emotions)
                        moving = moves_ZX.detect(pose_results)
                        self.come_off, self.face_angle = off_angle.detect(frame, fm_results)

                        self.passed = pygame.time.get_ticks() - self.start

                        if self.passed > 500:
                            plus = [self.moving, self.face_angle, self.come_off]
                            row = fer_result + plus
                            start = pygame.time.get_ticks()
                            self.passed = 0

                            fer.init()
                            moves_ZX.init()
                            off_angle.init()

                            try:
                                X1 = self.scalar.transform(np.array(row).reshape(1,-1))
                                focus = self.model.predict(X1)[0]
                                focus_prob = self.model.predict_proba(X1)[0][1]

                                print(focus)
                                print(focus_prob)

                            
                            except Exception as e:
                                print("예외가 발생하였습니다.", e)
                            

                    except Exception as e:
                        print("예외가 발생하였습니다.", e)

        # self.capture.release()
        cv2.destroyAllWindows()



    def fps(self):
        
        self.current_time = time.time()
        self.sec = self.current_time - self.preview_time
        self.preview_time = self.current_time
        
        if self.sec > 0 :
            fps = round(1/(self.sec),1)
            
        else :
            fps = 1
            
        return fps

    
                   
    def __exit__(self) :
        print( '* streamer class exit')
        self.capture.release()

    