import time
import cv2
import imutils
import platform
import numpy as np
from threading import Thread
from queue import Queue

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

    