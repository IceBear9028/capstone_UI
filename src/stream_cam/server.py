from flask import Flask
from flask import request
from flask import Response
from flask import stream_with_context
from dash import Dash, dcc, html

from streamer import Streamer

class Webcamserver:
    def __init__(self):
        self.src = request.args.get('src', default = 0, type = 'int')
        #self.stream = Streamer()
        self.layout()

    def layout(self):
        self.app.layout = html.Div(
            children = [],
            style = {
                'width' : '640',
                'height' : '320',
                'background-color' : '#000'
            }
        )