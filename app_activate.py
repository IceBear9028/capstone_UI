import plotly
import plotly.graph_objects as go
import math
import numpy as np
from dash_player import DashPlayer
from dash import Dash, dcc, html, Input, Output,ctx, State
from flask import Flask, Response, request
from src.model_api.streamer import Streamer
from src.datastroage.graph_data import Datamanage
from src.web_function.focus_notice import focus_notice_player
import dash_bootstrap_components as dbc

import focus_page 

graph_datamanage = Datamanage()
streamcam = Streamer()
focus_notice = focus_notice_player()

global video_time
video_time = 0
# 0. 필요한 변수들 선언
focus_result = streamcam.focus_prob
# -> 사용자의 집중도 결과를 저장 ()



# 1. 데이터 프레임 불러오기

confirm = 'confirmSection'
graph_figure = 'focus1'
frame = 'webcam_frame'
focus_marking_player = 'focus_marking_player'
interval = 'interval'
video_player = 'video_player'
video_current_time = 'videoCurrentTime'
marking_color_info_container = 'markingColorInfoContainer'

focus_container = 'focusContainer'
current_focus_figure = 'currentFocusFigure'
mean_focus_figure = 'meanFocusFigure'
activate_focus_figure = 'focusFigureActivateBtn'
focus_header = 'focusHeader'
focus_header_child1 = 'focusHeaderChild1'

# section별 그래프 보여주는 기능 이름들
# a. state별로 데이터 수집 & 레이아웃 추가하는 기능
section_focus_prob_board = 'sectionFocusProbBoard'
focus1 = 'focusState 1'
focus2 = 'focusState 2'
focus3 = 'focusState 3'




# 3. 웹 레이아웃 설정
server = Flask(__name__)
app = Dash(__name__, server=server)

# app.scripts.config.serve_locally = True

# 도움받은 사이트 :
# https://community.plotly.com/t/dash-player-custom-component-playing-and-controlling-your-videos-with-dash/12349

app.layout = html.Div(
    className = "container",
    children = [
        dcc.ConfirmDialog(
            id = confirm,
            message = '영상구간을 다시 재학습할건가요?'
        ),
        dcc.ConfirmDialog(
            id = 'confirmSectionEscape',
            message = '학습이 완료되지 않았습니다. 그래도 다음구간으로 넘어갈까요?'
        ),
        dcc.Interval(
            id = interval,
            disabled = False,
            interval = 1*1000,
            n_intervals= 0,
        ),
        html.Div(
            className = 'playerContainer',
            children = [
                    html.Div(
                        className = 'titleContainer',
                        children = [
                            html.H2(
                                id = 'title',
                                children = ['플레이어']
                            )
                        ]
                    ),
                    html.Div(
                        id = video_current_time,
                        children = []
                    ),
                    DashPlayer(
                        # 도움받은 사이트 :
                        # https://community.plotly.com/t/dash-player-custom-component-playing-and-controlling-your-videos-with-dash/12349
                        id = video_player,
                        # url = "assets/test_Video/JSON프론트엔드2.mp4",
                        # url = "assets/test_Video/뉴진스(NewJeans)'Attention'.mp4",
                        url = "assets/test_Video/실험계획법.mp4",
                        controls = True,
                        width ='900px',
                        height = '490px',
                        style = {
                            'display' : 'flex',
                            'justify-content' : 'center',
                            'align-content' : 'center'
                        }
                    ),
                    html.Div(
                        className = 'foucsMarkingPlayerContainer',
                        children = [
                            html.Div(
                                id = focus_header,
                                children = [
                                    html.Div(
                                        id = focus_header_child1,
                                        children = [
                                            # html.H2(
                                            #     id = 'focusNoticeTitle',
                                            #     children = ['집중도저하구간 확인']
                                            # ),
                                            html.Div(
                                                className = marking_color_info_container,
                                                children = [
                                                    html.Div(
                                                        className = 'Red InfoContainer',
                                                        children = [
                                                            html.Div(className = 'red Color'),
                                                            html.Span(
                                                                className = 'red Info',
                                                                children = ['재학습필요']
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(
                                                        className = 'Green InfoContainer',
                                                        children = [
                                                            html.Div(className = 'green Color'),
                                                            html.Span(
                                                                className = 'green Info',
                                                                children = ['학습완료']
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(
                                                        className = 'Gray InfoContainer',
                                                        children = [
                                                            html.Div(className = 'gray Color'),
                                                            html.Span(
                                                                className = 'gray Info',
                                                                children = ['학습미완료']
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        "집중도 상세보기",
                                        id = activate_focus_figure,
                                        n_clicks = 0,
                                    ),
                                ]
                            ),
                            html.Div(
                                id = focus_marking_player,
                                children = focus_notice.sections,
                                style = {
                                    'background' : '#E9E9E9',
                                    'width' : '{0}px'.format(focus_notice.section_container_width),
                                    'height' : '80px',
                                    'border-radius' : '10px',
                                    # 'border' : '1px solid #D0D2D8',
                                    'padding' : '3px',
                                    'display' : 'flex',
                                    'flex-direction' : 'row',
                                    'justify-content' : 'center',
                                    'box-shadow' : '0 5px 15px -7px rgba(190,190,190,4)',
                                    }
                            ),
                        ]
                    ),
                    html.Img(
                        src = "/video",
                        id = "facePhoto",
                        style = {
                            'width' : '0px',
                            'height' : '0px'
                        }
                    ),
            ]
        ),
        html.Div(
            id = 'focusContainer',
            children = [],
            style = {
                'display' : 'flex',
                'align-content' : 'space-between'
            }
        )
    ]
)
    
# 동영상 프로그레시브 바 추가

# 그린 -> 집중
# 레드 -> 비집중
# 옐로우 -> 진행중 

# 그래프 뜨는것, 구간별로 확인



# section 이동시 알림창 띄어주는 기능구현
@app.callback(
    Output(confirm, 'displayed'),
    Output('confirmSectionEscape', 'displayed'),
    focus_notice.marge_sections_Input
)
def confirm_relearn(*args):
    # 0. section이 선택되었을 때, section의 위치를 저장한다.
    focus_notice.clicked_section = ctx.triggered_id

    # A. section을 선택했을 때, 재학습할지말지 confirm 창을 띄어주는 코드 [situation_A]
    if not type(focus_notice.sections_check['time'][ctx.triggered_id]) == bool:
        # 이미 section의 학습이 끝나서 section_state 를 부여받은 경우에 대해서 재학습 여부를 물어보게 된다.
        if focus_notice.sections_check['section_state'][ctx.triggered_id] == 2 or \
            focus_notice.sections_check['section_state'][ctx.triggered_id] == 3:
            return  True, False

    # B. 현재 section의 학습이 완료되지 않았는데, 다른 section으로 넘어갈지 말지 confirm 창을 띄어주는 코드 [situation_B]
    return  False,True

# focus_notice_player 클래스 기능구현
@app.callback(
    Output(video_player, 'seekTo'),
    Input('video_player', 'duration'),
    Input(confirm, 'submit_n_clicks'),
    Input('confirmSectionEscape', 'submit_n_clicks')
)
def generate_notice(duration_time, situation_A, situation_B):
    # sections_timeline 딕셔너리를 만들기 위한 코드.
    # 한번만 실행하면 되기 때문에 TF 변수에 스위치 역할을 구현한 것.
    global video_time
    if focus_notice.generate_section_TF == False:
        focus_notice.generate_section(duration_time)
        focus_notice.generate_section_TF = True

    else:
        # A,B 상황에 대해서 학습자가 다른 section의 학습을 원할 때 위에서 저장한 section의 위치로 이동한다.
        if situation_A or situation_B :
            return focus_notice.sections_timeline[focus_notice.clicked_section]
        # 다른 section으로 넘어가기를 원치 않을 때 계속 영상을 보게 된다.

#현재의 집중도를 확인하는 기능
@app.callback(
    Output('currentFocus Result', 'children'),
    Output('durationTime Result','children'),
    Input(interval, 'n_intervals')
)
def focus_check(time):
    # focus = graph_datamanage.data['focus_prob'].pop()
    # focus_result = np.trunc(graph_datamanage.data['focus_prob'].pop() * 100)
    # focus_result = round(graph_datamanage.data['focus_prob'].pop(), 2)
    minute, second = np.divmod(time, 60)
    focus = graph_datamanage.data['focus_prob']
    return str(round(focus[-1]*100, 2)) + '%', ' {0}min {1}sec'.format(minute, second)


# section_time 저장 기능 
@app.callback(
    Output(video_current_time, 'children'),
    Input(interval, 'n_intervals'),
    Input(video_player, 'currentTime')
)
def current_time_check(n, current_time):
    global video_time
    video_time = int(current_time)
    focus_notice.section_mean_cal(graph_datamanage.data['video_time'],graph_datamanage.data['focus_prob'])
    focus_notice.save_section_state(current_time)
    # print(focus_notice.sections_check)

    # print(graph_datamanage.data)
    return [html.Span(n)]


# sections_state값에 따른 section 의 style 변경
@app.callback(
    focus_notice.marge_sections_Output,
    Input(interval, 'n_intervals'),
    # Input(video_player, 'currentTime')
)
def update_section(interval):
    global video_time
    current_section = focus_notice.find_section_id(video_time, value_type='num')
    style_list = []
    for state_value in focus_notice.sections_check['section_state'].values():
        style_list.append(focus_notice.set_section_style(state_value))
    
    # 현재 동영상 시간을 받아서, 현재위치의 section을 알리는 style 을 추가한다.
    # style_list[current_section]['border-bottom'] = '5px solid red'
    # style_list[current_section]['box-shadow'] = '0 5px 18px -7px rgba(0,0,0,4)'
    style_list[current_section]['border-bottom'] = '8px solid red'

    # ++ 양끝단의 section을 둥글게 스타일처리하는 코드추가
    # 1. 'btn 0'의 border-radius 추가
    style_list[0]['border-top-left-radius'] = '8px'
    style_list[0]['border-bottom-left-radius'] = '8px'

    # 2, 'btn 29'의 border-radius 추가
    style_list[-1]['border-top-right-radius'] = '8px'
    style_list[-1]['border-bottom-right-radius'] = '8px'

    return style_list


# 버튼 눌렀을 때 페이지 나오게 설정
@app.callback(
    Output(focus_container, 'children'),
    Input(activate_focus_figure, 'n_clicks'),
    #Input(activate_focus_figure, 'pathname'),
)
def activate_focus_figure_page(n):
    # 버튼이 눌리면
    if n%2 == 1:
        return focus_page.layout


# section 의 state 에 따라 그래프 레이아웃을 추가하는 기능
@app.callback(
    Output(section_focus_prob_board, 'children'),
    Input(focus1, 'n_clicks'),
    Input(focus2, 'n_clicks'),
    Input(focus3, 'n_clicks'),
    State(section_focus_prob_board, 'children')
)
def state_show_layout(*args):
    if len(args[-1]) == 2:
        args[-1].pop()
    
    
    args[-1].append(focus_page.graph_layout)
    return args[-1]

convert_to_statenum = {
    focus1 : 1,
    focus2 : 2,
    focus3 : 3
}



# 그래프 속성 설정
@app.callback(
    Output(graph_figure, 'figure'),
    Input(interval, 'n_intervals')
)
def focus_1(num):
    fig = plotly.tools.make_subplots(rows = 1, cols = 1)
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig.append_trace({
        'x' : graph_datamanage.data['real_time'],
        'y' : graph_datamanage.data['focus_prob'],
        'name' : 'focus',
        'type' : 'scatter',
        'mode' : 'lines',
        'marker_color' : '#b4cbf3'
    },1,1)
    fig.append_trace({
        'x' : graph_datamanage.data['real_time'],
        'y' : np.full((1,len(graph_datamanage.data['focus_prob'])),0.5)[0],
        'name' : 'threshold',
        'type' : 'scatter',
        'mode' : 'lines',
        'marker_color' : 'rgb(230,230,230)'
    },1,1)
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )
    fig.update_yaxes(range = [-0.1,1.1])
    # 그래프 margin 제거
    fig['layout'].update(
        margin = dict(l=40, r=20, b=30, t=15 ),        
    )
    return fig



# 5. 웹캠 연결용 서버
@server.route('/video')
def stream():
    src = request.args.get('src', default=0, type = int)
    try :
        return Response(stream_gen( src ) ,
                        mimetype='multipart/x-mixed-replace; boundary=frame' )
    except Exception as e :
        print('[wandlab] ', 'stream error : ',str(e))

def stream_gen( src ):   
    try : 
        streamcam.run( src )
        while True :
            # 1. 갖고온 frame 으로 웹페이지에 넣어줌
            frame = streamcam.bytescode()
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
            # 2. 깆고온 frame 으로 집중도 추출 및 현재시간과 영상시청 시간 기록
            graph_datamanage.current_time, graph_datamanage.focus_prob = streamcam.focus_result()
            graph_datamanage.video_time = video_time
            graph_datamanage.start()
            graph_datamanage.data_cut()
                    
    except GeneratorExit :
        streamcam.stop()


if __name__ == '__main__':
    app.run_server(debug=True)




# $ pip install --upgrade pip
# $ pip install cython
# $ pip install "numpy<17"
# $ pip install imutils
# $ pip install flask
# $ pip install opencv-python
# $ pip install opencv-contrib-python