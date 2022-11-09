import plotly
import numpy as np
from dash_player import DashPlayer
from dash import Dash, dcc, html, Input, Output,ctx
from flask import Flask, Response, request
from src.model_api.streamer import Streamer
from src.datastroage.graph_data import Datamanage
from src.web_function.focus_notice import focus_notice_player

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
current_focus_figure = 'currentFocusFigure'
mean_focus_figure = 'meanFocusFigure'


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
        html.Div(
            className = 'playerContainer',
            children = [
                    html.Div(
                        className = 'titleContainer',
                        children = [
                            html.H2(
                                id = 'title',
                                children = ['동영상 플레이어']
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
                        url = "assets/test_Video/뉴진스(NewJeans)'Attention'.mp4",
                        controls = True,
                        width ='900px',
                        height = '500px',
                        style = {
                            'display' : 'flex',
                            'justify-content' : 'center',
                            'align-content' : 'center'
                        }
                    ),
                    html.Div(
                        className = 'foucsMarkingPlayerContainer',
                        children = [
                            html.H2(
                                id = 'aaa',
                                children = ['집중도저하구간 확인']
                            ),
                            html.Div(
                                id = focus_marking_player,
                                children = focus_notice.sections,
                                style = {
                                    'background' : '#fff',
                                    'width' : '{0}px'.format(focus_notice.section_container_width),
                                    'height' : '80px',
                                    'border-radius' : '10px',
                                    'border' : '1px solid #D0D2D8',
                                    'padding' : '7px',
                                    'display' : 'flex',
                                    'flex-direction' : 'row',
                                    'justify-content' : 'center'
                                    }
                            ),
                        ]
                    )
                ]
            ),
        html.Div(
            className = 'focusResultContainer',
            children =[    
                dcc.Graph(id = graph_figure),
                dcc.Interval(
                    id = interval,
                    disabled = False,
                    interval = 1*1000,
                    n_intervals= 0
                ),
                html.Div(
                    className = "focusProbView",
                    children = [
                        html.Img(
                            src = "/video",
                            id = "facePhoto",
                            style = {
                                'border' : '1px solid #ddd',
                                "border-radius" : '10px',
                                'padding' : '5px',
                                'width' : '200px'
                            }
                        ),
                        html.Div(
                            className = 'focusFigureContainer',
                            children = [
                                html.Div(
                                    id = current_focus_figure,
                                    children = []
                                ),
                                html.Div(
                                    id = mean_focus_figure,
                                    children = []
                                )
                            ]
                        ),
                    ],
                ),
            ],
        )
    ]
)
    
# 동영상 프로그레시브 바 추가

# 그린 -> 집중
# 레드 -> 비집중
# 옐로우 -> 진행중 

# 그래프 뜨는것, 구간별로 확인

# 4. 그래프 속성 설정
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
        'type' : 'scatter'
    },1,1)
    fig.update_yaxes(range = [-0.1,1.1])

    return fig



#현재의 집중도를 확인하는 기능
@app.callback(
    Output(current_focus_figure, 'children'),
    Input(interval, 'n_intervals')
)
def focus_check(n):
    focus = graph_datamanage.data['focus_prob']
    return [html.H1(str(round(focus[-1], 3)))]

# 버튼을 눌렀을 때, 집중도를 다시 측정할지 말지 뜨는 알림창
@app.callback(
    Output(confirm, 'displayed'),
    focus_notice.marge_sections_Input
)
def confirm_relearn(*args):
    # section을 선택했을 때, 재학습할지말지 확인하는 코드
    if not type(focus_notice.sections_check['time'][ctx.triggered_id]) == bool:
        return True
    return False


# focus_notice_player 클래스 기능구현
@app.callback(
    Output(video_player, 'seekTo'),
    focus_notice.marge_sections_Input,
)
def generate_notice(*args):
    # sections_timeline 딕셔너리를 만들기 위한 코드.
    # 한번만 실행하면 되기 때문에 TF 변수에 스위치 역할을 구현한 것.
    if focus_notice.generate_section_TF == False:
        focus_notice.generate_section(args[0])
        focus_notice.generate_section_TF = True

    else:
        # 학습시간을 만족하지만 재학습을 하고싶은 경우
        if focus_notice.sections_check['section_state'] == 2 or \
            focus_notice.sections_check['section_state'] == 3 :
            # 기존 학습한 기록을 리셋한다(학습시간,프레임당 집중도).
            focus_notice.sections_check['time'][ctx.triggered_id] = True
            focus_notice.sections_check['prob'][ctx.triggered_id] = np.array([])

        return focus_notice.sections_timeline[ctx.triggered_id]


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
    focus_notice.save_section_state()
    print(focus_notice.sections_check)
    return [html.Span(n)]


# sections_state값에 따른 section 의 style 변경
@app.callback(
    focus_notice.marge_sections_Output,
    Input(interval, 'n_intervals')
)
def update_section(interval):
    style_list = []
    for state_value in focus_notice.sections_check['section_state'].values():
        style_list.append(focus_notice.set_section_style(state_value))
    return style_list


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