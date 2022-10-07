from dash import Dash, dcc, html, Input, Output, State,ctx

class focus_notice_player:
    def __init__(self):
        self.elements_number = 0
        self.element_width = 0
        self.video_length = 0
        self.elements = []
        self.element_style = {
            'background' : '#000',
            'border' : '1px solid red',
            'height' : 'auto',
            'width' : '10px'
        }
    def generate_element(self, number):
        self.elements.append(
            html.Div(
                className = 'focus_element',
                children = [html.Span(str(number))],
                style = self.element_style
            )
        )
