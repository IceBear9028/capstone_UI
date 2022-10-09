import datetime
from turtle import distance

class Datamanage :
    def __init__(self):
        self.data = {
            'real_time' : [],
            'focus_prob' : [],
            #'video_time' : []
        }
        # 시간 초기값 설정
        self.setting_time = 5 * 10^5
        # -> 확률이 나오기까지의 시간 -> 0.5sec 정도 걸림
        self.distance_time = 0
        self.preview_time = datetime.datetime.now()
        self.current_time = 0

        # 집중도값 설정
        self.focus_prob = 0

        # 비디오플레이어 값
        #self.video_time = 0

        # 데이터가 저장되는지 확인하기 위한 코드
        # self.focus

        # 인스턴스 설정 시, preview_time, current_time 을 외부에서 초기값을 설정할 것!

    def start(self):
        self.distance_time = self.current_time - self.preview_time
        self.distance_time = int(self.distance_time.total_seconds() * (10**6))
        print(self.distance_time)
        
        if self.setting_time < self.distance_time : 
            self.data_append()
            print(self.data)
            self.preview_time = self.current_time
        else : pass
    
    def data_append(self):
        self.data['real_time'].append(self.current_time)
        # self.data['video_time'].append(self.video_time)
        self.data['focus_prob'].append(self.focus_prob)
        
        # self.data['focus'].append(self.focus)

    # def data_test(self):
    #     if

# 2022.10.09 오후 6시53분 -> video_time append 하는 기능 제거.