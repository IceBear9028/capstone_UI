import plotly
from dash_player import DashPlayer
from dash import Dash, dcc, html, Input, Output, State,ctx
from dash.exceptions import PreventUpdate
from flask import Flask, Response, request, stream_with_context
from src.model_api.streamer import Streamer
from src.datastroage.data_api import Datamanage
from src.web_function.player import focus_notice_player

datamanage = Datamanage()
streamcam = Streamer()
focus_notice = focus_notice_player()

global video_time

# 0. 필요한 변수들 선언
focus_result = streamcam.focus_prob
test = '시발'
# -> 사용자의 집중도 결과를 저장 ()



# 1. 데이터 프레임 불러오기

# 2. 그래프 저장
graph_id_1 = 'focus1'
graph_id_2 = 'focus2'
frame = 'webcam_frame'


focus_marking_player = 'focus_marking_player'
interval = 'interval'

# 3. 웹 레이아웃 설정
server = Flask(__name__)
app = Dash(__name__, server=server)

# app.scripts.config.serve_locally = True

app.layout = html.Div(
    className = "container",
    children = [
        html.Div(
            className = 'videoPlayer',
            children = [
                html.Div(
                    id = 'video_currentTime',
                    children = []
                ),
                html.Div(
                    id = 'videoFunction',
                    children = [
                        html.Button('앞으로5초', id = 'videoForward'),
                        html.Button('뒤로5초', id = 'videoBackward')
                    ]
                ),
                DashPlayer(
                    # 도움받은 사이트 :
                    # https://community.plotly.com/t/dash-player-custom-component-playing-and-controlling-your-videos-with-dash/12349
                    id = 'player',
                    url = "assets/test_Video/JSON프론트엔드2.mp4",
                    controls = True,
                ),
                dcc.Checklist(
                    id = 'test_check',
                    options = [
                        {"label" : "playing", "value" : "playing"},
                    ]
                ),
                html.Div(
                    id = focus_marking_player,
                    children = [],
                    style = {
                        'background' : '#fff',
                        'width' : '1000px',
                        'height' : '350px',
                        'border' : '1px solid red',
                        'display' : 'flex',
                        'flex-direction' : 'row',
                        'justify-content' : 'flex-start'
                        }
                )
            ]
        ),
        html.Div(id = 'test'),
        html.Div(
            className = 'graphContainer',
            children =[
                dcc.Graph(id = graph_id_1),
                dcc.Interval(
                    id = interval,
                    disabled = False,
                    interval = 1*1000,
                    n_intervals= 0
                ),          
            ]
        ),
        html.Div(
            className = "realtimeFocus",
            children = [
                html.Img(src = "/video")
            ]
        ),
        html.Div(
            id = 'focus',
            children = [
                html.Div(
                    id = 'realtime_focus_result',
                    children = []
                )
            ]
        )
    ]
)
# 참고할 웹사이트
# http://wandlab.com/blog/?p=94


# 4. 그래프 속성 설정
@app.callback(
    Output(graph_id_1, 'figure'),
    Input(interval, 'n_intervals')
)
def focus_1(num):
    fig = plotly.tools.make_subplots(rows = 1, cols = 1)
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x' : datamanage.data['real_time'],
        'y' : datamanage.data['focus_prob'],
        'name' : 'focus',
        'type' : 'scatter'
    },1,1)
    return fig

# test 체크리스트 -> play, pause
@app.callback(
    Output('player', 'playing'),
    Input('test_check', 'value')
)
def play_pause_function(value):
    return "playing" in value


# 현재 playtime 을 확인하는 기능.
@app.callback(
    Output('video_currentTime', 'children'),
    Input('player', 'currentTime')
)
def current_time_check(value):
    global video_time
    video_time = int(value)
    return [html.Span(value)]

# 특정 시간대로 playtime 변경
@app.callback(
    Output('player', 'seekTo'),
    Input('videoForward', 'n_clicks'),
)
def video_forward(n_click):
    if 'videoForward' == ctx.triggered_id:
        time = 300
    return time

# playtime 받기
# @app.callback(
#     Input('player', 'currentTime')
# )
# def graphData_input_video_currentTime(time):
#     video_time = time
#     return video_time
    

#현재의 집중도를 확인하는 기능
@app.callback(
    Output('focus', 'children'),
    Input(interval, 'n_intervals')
)
def focus_check(n):
    focus = datamanage.data['focus_prob']
    return [html.H1(str(focus[-1]))]


@app.callback(
    Output(focus_marking_player, 'children'),
    Input(interval, 'n_intervals')
)
def focus_player(n):
        # box_list = []
        for i in range(n):
            # box_list.append(
            #     html.Div(id = '{0}_box'.format(i),
            #                 children = [], 
            #                 style = {
            #                     'background' : '#000',
            #                     'border' : '1px solid red',
            #                     'height' : 'auto',
            #                     'width' : '10px'
            #                     })
            # )
            focus_notice.generate_element(number = i)
        return focus_notice.elements



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
            
            # frame = streamcam.bytescode()
            # # 1. 갖고온 frame 으로 웹페이지에 넣어줌
            # yield (b'--frame\r\n'
            #       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
            # 2. 깆고온 frame 으로 집중도 추출
            datamanage.current_time, datamanage.focus_prob = streamcam.focus_result()
            datamanage.video_time = video_time
            datamanage.start()

            ## 여기다가, 프레임을 넣어주는 기능을 작성할 것 
                    
    except GeneratorExit :
        #print( '[wandlab]', 'disconnected stream' )
        streamcam.stop()

# @app.callback(
#     Output(component_id = 'focus_result', component_property='children'),
#     Input(focus_result, 'value')
# )
# def update_focus(input):
#     return f'Output : {input}'


if __name__ == '__main__':
    app.run_server(debug=True)



# $ pip install --upgrade pip
# $ pip install cython
# $ pip install "numpy<17"
# $ pip install imutils
# $ pip install flask
# $ pip install opencv-python
# $ pip install opencv-contrib-python