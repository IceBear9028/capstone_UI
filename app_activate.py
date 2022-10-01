import plotly
from dash import Dash, dcc, html, Input, Output, dash_table,State
import plotly.express as px
from flask import Flask, Response, request, stream_with_context
from src.model_api.streamer import Streamer
from src.datastroage.data_api import Datamanage

datamanage = Datamanage()
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
        html.Div(id = 'test'),
        html.Div(
            className = 'graphContainer',
            children =[
                dcc.Graph(id = graph_id_1),
                dcc.Interval(
                    id = 'interval-component',
                    disabled = False,
                    interval = 1*1000,
                    n_intervals= 0
                ),
                dcc.Interval(
                    id = 'test-component',
                    disabled = False,
                    interval = 1*10000,
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
    Input('interval-component', 'n_intervals')
)
def focus_1(num):
    fig = plotly.tools.make_subplots(rows = 1, cols = 1)
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x' : datamanage.data['time'],
        'y' : datamanage.data['focus_prob'],
        'name' : 'focus',
        'type' : 'scatter'
    },1,1)
    return fig
         


# 최종 집중확률 결과 표시
# => 여기 작동안함, 왜??????
@app.callback(
    Output('realtime_focus_result', 'children'),
    Input('test-component', 'n_intervals')
)
def focus_print():
    # focus_result_list = datamanage.data['focus_prob']
    # focus_result = focus_result_list[len(focus_result_list)-1]
    test = 'hello_world_fuck'
    return html.Span('focus_result : {0}'.format(test))




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
            datamanage.current_time, datamanage.focus_prob = streamcam.focus_result()
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