from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import cv2
from flask import Flask, Response, request, stream_with_context
from src.stream_cam.streamer import Streamer

streamcam = Streamer()

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
        html.Div(),
        html.Div(
            className = "realtimeFocus",
            children = [
                html.Img(src = "/video")
            ]
        ),
    ]
)
# 참고할 웹사이트
# http://wandlab.com/blog/?p=94

# 4. 그래프 속성 설정
@app.callback(
    Output(graph_id_1, 'figure')
)
def focus_1():
    fig = px.line()
    fig.update_layout(
        margin = dict(l=10,r=10, t=10, b=10),
        
    )

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
            
            frame = streamcam.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                    
    except GeneratorExit :
        #print( '[wandlab]', 'disconnected stream' )
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