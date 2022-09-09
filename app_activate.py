from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import cv2

class VideoCamera(object):
    

app = Dash(__name__)

app.layout = html.Div(
    className = "main",
    children = [
        html.Video(
            className = 'webCam',
            autoPlay = True,
            muted = 'muted',
        ),
        html.Div(
          className = 'title',
          children = [html.H1("시발람들아")],
          style = {
            'width' : '1500px',
            'justify-content' : 'flex-start',
            'padding-left' : '20px'
          }
        ),
        html.Div(
            className = 'container',
            children = [
                html.Div(
                    className = "graphDiv",
                    children  = [
                        html.Div(className = "graph1"),
                        html.Div(className = "graph2")
                    ]
                ),
                html.Div(
                    className = 'webCamContainer',
                    children = [
                    #     html.Video(
                    #         className = 'webCam',
                    #         autoPlay = True,
                    #         muted = True
                    #     )
                    ],
                    style = {
                        'height' : '500px',
                        'width' : '300px',
                    }
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)