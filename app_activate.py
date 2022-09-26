import time
from dash import Dash, dcc, html, Input, Output, dash_table,State
import plotly.express as px
import cv2
from flask import Flask, Response, request, stream_with_context
from src.model_api.streamer import Streamer

streamcam = Streamer()

# 0. 필요한 변수들 선언
focus_result = streamcam.focus_prob
test = '시발'
# -> 사용자의 집중도 결과를 저장 ()



# 1. 데이터 프레임 불러오기

# 2. 그래프 저장
graph_id_1 = 'focus1'
graph_id_2 = 'focus2'
frame = 'webcam_frame'

# 3. 웹 레이아웃 설정
server = Flask(__name__)
app = Dash(__name__, server=server)

app.layout = html.Div(
    className = "container",
    children = [
        html.Div(
        ),
        html.Div(),
        html.Div(
            className = 'graphContainer',
            children =[
                dcc.Graph(id = graph_id_1)
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
                    children = [
                        str(focus_result)
                    ]
                ),
                dcc.Interval(
                    id = 'interval-component',
                    interval = 1*1000,
                    n_intervals = 0
                )
            ]
        )
    ]
)
# 참고할 웹사이트
# http://wandlab.com/blog/?p=94
@app.callback(
    Output(component_id='focus',component_property='children'),
    Input(component_id='interval-component', component_property='n_intervals'),
    State(component_id = 'realtime_focus_result', component_property='value')
)
def interval_text(n):
    text = streamcam.focus_prob
    return

# 4. 그래프 속성 설정
@app.callback(
    Output(graph_id_1, 'figure')
)
def focus_1():
    fig = px.line()
    fig.update_layout(
        margin = dict(l=10,r=10, t=10, b=10),
        
    )

# 최종 집중확률 결과 표시


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
            # 1. 갖고온 frame 으로 웹페이지에 넣어줌
            # yield (b'--frame\r\n'
            #       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
            # 2. 깆고온 frame 으로 집중도 추출
            streamcam.focus_result()

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