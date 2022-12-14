from dash import html, Input, Output
import datetime
import time
import numpy as np
import copy

class focus_notice_player:
    def __init__(self):
        # section_num : 영상에 대한 구간 갯수
        self.section_num = 30

        # section_container_width : 영상에 대한
        self.section_container_width = 895

        # elements_number : 집중구간 단위 블록의 갯수
        # section_time : 동영상 구간을 30개로 나누었을 때의 시간
        self.section_time = 0

        # section_style : 집중구간블록을 css로 꾸민다.
        # section의 width 는 section_container_width의 길이에 section_num을 나눈 값
        self.section_style = {
            'display' : 'flex',
            'justify-content' : 'center',
            'background' : '#fff',
            # 'border' : '1px solid red',
            'height' : 'auto',
            'width' : '{0}px'.format(self.section_container_width/self.section_num),
        }

        # section_color : sections_check['section_state'] 값에 따른 색 변화
        # 색 순서 -> 측정x, 학습시간부족, 집중도낮음, 집중도높음
        self.section_color = ['#fff', '#D0D2D8', '#F7B7A8', '#A6E27F']

        # video_length : 학습동영상의 길이
        self.video_length = 0

        # current_video_section : 비디오 색션 확인을 위한 용도
        # -> section_stored 함수에서, 이전 섹션과 이후 섹션 확인하기 위함.\
        self.current_video_section = None

        # clicked_section : section 버튼을 눌렀을 때, 해당 section 버튼의 id 를 저장한다.
        self.clicked_section = None

        # sections : 각 집중구간블록이 담긴 어레이
        # 어레이 형태로 묶어야 html 에서 한번에 랜더링된다.
        self.sections = [
            html.Div(
                id='btn {0}'.format(i),
                children = [html.P('{0}'.format(i + 1), style = {'color' : '#808080', 'font-size' : '8px'})],
                style = self.section_style,
                n_clicks = 0
            ) for i in range(self.section_num)
        ]

        # _time 변수는 self.cal_watching_time() 함수를 작동하는데 사용 
        # -> 이 함수는 section 의 시청시간을 기록하는 기능을 갖는다.
        self.start_time = None
        self.end_time = None
        self.watching_time = None

        self.video_section = None

        # confirm창에서 submit cancel을 누른 값을 저장하는 변수
        self.confirm_data = {'accept' : None, 'cancel' : None}

        self.sections_id = []

        # 생성된 element의 id와 time을 저장하는 리스트
        self.sections_timeline = {}

        # 구간별 동영상 시청시간, 구간 내의 초당 집중도, 최종 구간의 집중
        self.sections_check = {
            'time' : {},
            'prob' : {},
            'section_state' : {},
            'real_time' : {}
        }
        # time : section 별 동영상 시청시간
        # prob : section 내 초당 집중도
        # section_state : 동영상 구간 당 상태를 저장
        #   -> 0 : section에서의 학습을 한번도 안한 상태
        #   -> 1 : section에서의 학습이 완료되지 않은 상태
        #   -> 2 : section에서의 학습완료, 하지만 집중도가 낮음.
        #   -> 3 : section에서의 학습완료, 집중도 충분함.

        # marge_elements_Input : dash에 callback으로 넣을 Input객체를 리스트 형태로 저장
        self.marge_sections_Input = [Input('btn {0}'.format(i), 'n_clicks') for i in range(self.section_num)]
        # self.marge_sections_Input.insert(0,Input('video_player', 'duration'))

        # marge_sections_Output : dash 에 callback으로 넣을 Output 객체를 리스트 형태로 저장
        self.marge_sections_Output = [Output('btn {0}'.format(i), 'style') for i in range(self.section_num)]        

        self.generate_section_TF = False

        # 재상 section의 위치를 저장하는 변수
        self.current_section = "btn 0"


    # generate_element 함수 실행하면 div가 생성된다.
    # 이 함수는 한번만 실행한다(초기값들을 설정하기 위한 함수).
    def generate_section(self, video_length):
        self.section_time = int(video_length /self.section_num);

        for i in range(self.section_num):
            # section_timeline : 각 섹션에 대한 timeline 이 담겨져 있는 딕셔너리
            self.sections_timeline['btn {0}'.format(i)] = self.section_time * i

            # section_check : 각 섹션 내의 초단위로 수업을 들은 여부를 체크하는 딕셔너리
            self.sections_check['time']['btn {0}'.format(i)] = False
            self.sections_check['prob']['btn {0}'.format(i)] = np.array([])
            self.sections_check['section_state']['btn {0}'.format(i)] = 0
            self.sections_check['real_time']['btn {0}'.format(i)] = []

    # section 당 시청한 시간을 계산한다.
    def cal_watching_time(self, on_off):
        if on_off == 'start':
            self.start_time = time.time()
        
        elif on_off == 'end':
            self.end_time = time.time()
        
        elif on_off == 'cal':
            self.watching_time = int(self.end_time - self.start_time)   
    

    # datamanage.data 에서 동영상시간,확률을 받는다.
    def get_time_prob(self, time_list, prob_list):
        time = time_list[len(time_list)-1]
        prob = prob_list[len(prob_list)-1]

        return time,prob


    # 시간초가 들어오고, 어디 구간인지 알려주는 함수
    def find_section_id(self, num, value_type = 'div_id'):
        for i in range(self.section_num):
            for j in range((i*self.section_time),(i+1)*self.section_time):
                if j == num:
                    if value_type == 'div_id':
                        return 'btn {0}'.format(i)
                    elif value_type == 'num':
                        return i

    
    # prob 값이 들어오면, 평균으로 계산해주는 함수
    # 매 프레임마다 영상시간과 확률을 받으면, 이를 section_check 딕션너리에 업데이트
    def section_mean_cal(self, time_list, prob_list):
        time, prob = self.get_time_prob(time_list, prob_list)
        
        # 비디오 section 이 바뀌는 경우
        if self.video_section != self.find_section_id(time):
            # 1. 처음 웹페이지를 열고 플레이어를 재생시킬 때
            if self.video_section == None:
                # 초기 video_section 값이 None 인 경우는 처음 페이지를 열었을 때 밖에 없다.
                # 따라서 초기 한번만 실행되고 이후에는 사용되지 않는다.

                # 처음 video_section 값을 지정해준다.
                self.video_section = 'btn 0'

                # 그리고 시간 측정을 시작한다.
                self.cal_watching_time('start')
            

            # 2. section 의 학습이 끝난경우
            # -> section 의 시간측정을 끝내고, 집중도를 평균으로 구한다.
            else:
                # 시간 기록을 정지한다.
                self.cal_watching_time('end')

                # 시청시간을 최종적으로 계산한다.
                self.cal_watching_time('cal')

                # 이전에 저장되어 있던 watching_time 값을 더해서 section 간 최종 시청한 시간을 저장한다.
                self.sections_check['time'][self.video_section] += self.watching_time

                # 시청시간을 다시 기록한다.
                self.cal_watching_time('start')

                # 마지막으로,이전의 self_video_section 값울 현재 section 저장
                self.video_section = self.find_section_id(time)

        # 비디오 section 이 동일한 경우
        else:
            self.sections_check['time'][self.video_section] = True
            self.sections_check['prob'][self.video_section] = np.insert(self.sections_check['prob'][self.video_section], 0, int(prob*100))
            self.sections_check['real_time'][self.video_section].append(datetime.datetime.now())
    
    # section 의 state를 return 하는 함수
    def save_section_state(self,current_time):
        for section_id, value_time in self.sections_check['time'].items():
            # 먼저 currentTime 값의 div id 랑 section_id 가 같은지 확인
            
                # A. section 당 학습시간이 부족한 경우
                if value_time == False:
                    self.sections_check['section_state'][section_id] = 0

                elif value_time == True or (self.section_time - 1) > value_time: 
                    self.sections_check['section_state'][section_id] = 1

                # B. section 당 학습시간이 충분한 경우
                else:
                    mean = np.mean(self.sections_check['prob'][section_id])
                # section 의 집중확률이 낮은경우
                    if mean < 50:
                        self.sections_check['section_state'][section_id] = 2
                # section 의 집중확률이 높은경우
                    else:
                        self.sections_check['section_state'][section_id] = 3
            

    # section_state 값에 따라 각 section의 style 을 업데이트
    def set_section_style(self, section_state):
        init_style = copy.deepcopy(self.section_style)
        if section_state == 0:
            init_style['background'] = self.section_color[0]

        elif section_state == 1:
            init_style['background'] = self.section_color[1]

        elif section_state == 2:
            init_style['background'] = self.section_color[2]

        elif section_state == 3:
            init_style['background'] = self.section_color[3]

        return init_style
                    
            



        



        
        
        



        
                    