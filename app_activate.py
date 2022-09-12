from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import cv2
from flask import Flask, Response

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        sucess, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed():
    return Response(gen(VideoCamera()), 
                    mimetype='multipart/x-mixed-replace; boundary=frame'
    )

server = Flask(__name__)
app = Dash(__name__, server=server)

app.layout = html.Div(
    className="main",
    children=[
        html.Div(
            className='title',
            children=[html.H1("시발람들아")],
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
                    className="graphDiv",
                    children=[
                        html.Div(
                            className="graph1",
                            children = [
                                html.H1("그래프1")
                            ]
                            ),
                        html.Div(
                            className="graph2",
                            children = [
                                html.H1("그래프2")
                            ]
                            )
                    ]
                ),
                html.Img(
                    src = './video_feed',
                    style = {
                        'width' : '400px',
                        'height' : '280px'
                    }
                )
            ]
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
