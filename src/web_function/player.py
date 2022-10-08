from dash import html

class focus_notice_player:
    def __init__(self):
        # elements_number : 집중구간 단위 블록의 갯수
        self.elements_number = 0

        # elements_number : 집중구간 단위 블록의 넓이
        self.element_width = 0

        # video_length : 학습동영상의 길이
        self.video_length = 0

        # elements : 각 집중구간블록이 담긴 어레이
        # 어레이 형태로 묶어야 html 에서 한번에 랜더링된다.
        self.elements = []

        # element_style : 집중구간블록을 css로 꾸민다.
        self.element_style = {
            'background' : '#000',
            'border' : '1px solid red',
            'height' : 'auto',
            'width' : '10px'
        }

    def cal_element_num(self, video_length):
        # 집중블록의 개수 = 전체영상길이 / 10초
        # 이 함수는 generate_element 에 넣어서 실행시킨다.
        return int(video_length / 10);


    # generate_element 함수 실행하면 div가 생성된다.
    def generate_element(self, video_length):
        self.elements_number = self.cal_element_num(video_length)

        for i in range(self.elements_number):
            self.elements.append(
                html.Div(
                    className = 'focus_element',
                    children = [html.Span(str(i))],
                    style = self.element_style
                )
            )
