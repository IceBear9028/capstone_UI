from dash import html, Input, State

class focus_notice_player:
    def __init__(self):
        # section_num : 영상에 대한 구간 갯수
        self.section_num = 30
        self.section_container_width = 600
        # elements_number : 집중구간 단위 블록의 갯수
        # section_time : 동영상 구간을 30개로 나누었을 때의 시간
        self.section_time = 0

        self.section_color = '#000'

        # section_style : 집중구간블록을 css로 꾸민다.
        # section의 width 는 section_container_width의 길이에 section_num을 나눈 값
        self.section_style = {
            'background' : '#000',
            'border' : '1px solid red',
            'height' : 'auto',
            'width' : '{0}px'.format(self.section_container_width/self.section_num)
        }

        # video_length : 학습동영상의 길이
        self.video_length = 0

        # elements : 각 집중구간블록이 담긴 어레이
        # 어레이 형태로 묶어야 html 에서 한번에 랜더링된다.
        self.sections = [
            html.Div(
                id='{0}_btn'.format(i),
                children = [html.H3('{0}'.format(i))],
                style = self.section_style,
                n_clicks = 0) for i in range(self.section_num)]


        self.sections_id = []

        # 생성된 element의 id와 time을 저장하는 리스트
        self.sections_timeline = {}

        self.sections_check = {}

        # marge_elements_Input : dash에 callback으로 넣을 Input객체를 리스트형태로 모았음.
        self.marge_sections_Input = [Input('{0}_btn'.format(i), 'n_clicks') for i in range(self.section_num)]
        self.marge_sections_Input.insert(0,Input('video_player', 'duration'))

        self.generate_section_TF = False

    # 이전 함수이름 : cal_element_num(self, video_length)

    # generate_element 함수 실행하면 div가 생성된다.
    def generate_section(self, video_length):
        self.section_time = int(video_length /self.section_num);

        for i in range(self.section_num):
            # section_timeline : 각 섹션에 대한 timeline 이 담겨져 있는 딕셔너리
            self.sections_timeline['{0}_btn'.format(i)] = self.section_time * i

            # section_check : 각 섹션 내의 초단위로 수업을 들은 여부를 체크하는 딕셔너리
            self.sections_check['{0}_btn'.format(i)] = {}
            for j in range((i*self.section_time),(i+1)*self.section_time):
                self.sections_check['{0}_btn'.format(i)]['{0}'.format(j)] = {}
                self.sections_check['{0}_btn'.format(i)]['{0}'.format(j)]['TF'] = False
                self.sections_check['{0}_btn'.format(i)]['{0}'.format(j)]['prob'] = None

    # section_check가 모두 True가 되었을 때, 각 section 에 대한 prob의 평균값 추출
    # def section_mean_focus_prob(self, id):
    #     if self.sections_check['{0}_btn'.format(id)].get('')
        




    # 한 프레임에 대한 실시간 video시간과 집중도 prob를 알려줌
    def realtime_data_activate(self, prob, video_time):
        return [prob, video_time]

    # 시간초가 들어오고, 어디 구간인지 알려주는 함수
    def find_section_id(self, num):
        for i in range(self.section_num):
            for j in range((i*self.section_time),(i+1)*self.section_time):
                if j == num:
                    return '{0}_btn'.format(i)
    
    # 영상시간과 확률을 받으면, 이를 section_check 딕션너리에 업데이트
    def section_confirm(self, prob, time):
        video_watch_section = self.find_section_id(time)

        self.sections_check[video_watch_section]['{0}'.format(time)]['TF'] = True
        self.sections_check[video_watch_section]['{0}'.format(time)]['prob'] = prob



        
                    