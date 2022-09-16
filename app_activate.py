from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import cv2
from flask import Flask, Response

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
    className="main",
    children=[
        html.Div(
            className='title',
            children=[html.H1("focus-capstone")],
            style={
                'width': '1500px',
                'justify-content': 'flex-start',
                'padding-left': '20px'
            }
        ),
        html.Div(
            className='container',
            children=[
                html.Div(
                    className = 'webCamContainer',
                    children = [
                        html.Div(
                            style = {
                                'width' : '100%',
                                'height' : '100%'
                            }
                        )
                    ]
                ),
                html.Div(
                    className="graphDiv",
                    children=[
                        html.Div(
                            className="graph1",
                            children = [
                                dcc.Graph(
                                    id = graph_id_1,
                                    style = {
                                        'width':'90%',
                                        'height' : '80%',
                                    }
                                )
                            ]
                            ),
                        html.Div(
                            className="graph2",
                            children = [
                                dcc.Graph(
                                    id = graph_id_2,
                                    style = {
                                        'width' : '90%',
                                        'height' : '80%'
                                    }
                                )
                            ]
                            ),
                        html.Div(
                            className  = 'graph3',
                            children = []
                        ),
                        
                    ]
                ),
            ]
        )
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
