from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import cv2
from flask import Flask, Response, request

from src import stream_webcam as sw

streamer = sw.Streamer()

# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)

#     def __del__(self):
#         self.video.release()
#         cv2.destroyAllWindows()

#     def get_frame(self):
#         sucess, image = self.video.read()
#         ret, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()

# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# def video_feed():
#     return Response(gen(VideoCamera()), 
#                     mimetype='multipart/x-mixed-replace; boundary=frame'
#     )

# 1. 데이터 프레임 불러오기

# 2. 그래프 저장
graph_id_1 = 'focus1'
graph_id_2 = 'focus2'


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


if __name__ == '__main__':
    app.run_server(debug=True)


# $ pip install --upgrade pip
# $ pip install cython
# $ pip install "numpy<17"
# $ pip install imutils
# $ pip install flask
# $ pip install opencv-python
# $ pip install opencv-contrib-python