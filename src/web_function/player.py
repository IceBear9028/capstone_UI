from dash import html, Input, State

class focus_notice_player:
    def __init__(self):
        # section_num : 영상에 대한 구간 갯수
        self.section_num = 30
        self.section_container_width = 600
        # elements_number : 집중구간 단위 블록의 갯수
        # section_time : 동영상 구간을 30개로 나누었을 때의 시간
        self.section_time = 0


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

        # marge_elements_Input : dash에 callback으로 넣을 Input객체를 리스트형태로 모았음.
        self.marge_sections_Input = [Input('{0}_btn'.format(i), 'n_clicks') for i in range(self.section_num)]
        self.marge_sections_Input.insert(0,Input('video_player', 'duration'))

        self.generate_section_TF = False

    # 이전 함수이름 : cal_element_num(self, video_length)

    # def cal_section_time(self, video_length):
    #     # 이 함수는 generate_element 에 넣어서 실행시킨다.
    #     self.section_time = int(video_length /self.section_num);


    # generate_element 함수 실행하면 div가 생성된다.
    def generate_section(self, video_length):
        self.section_time = int(video_length /self.section_num);

        for i in range(self.section_num):
            self.sections_timeline['{0}_btn'.format(i)] = self.section_time * i
