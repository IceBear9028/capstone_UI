from dash import html
from dash import dcc, html

layout = html.Div(
    className = 'focusResultContainer',
    children =[    
        dcc.Graph(id = 'focus1'),
        html.Div(
            className = "focusProbView",
            children = [
                html.Img(
                    src = "/video",
                    id = "facePhoto",
                    style = {
                            'border' : '1px solid #ddd',
                            "border-radius" : '10px',
                            'padding' : '5px',
                            'width' : '200px'
                        }
                ),
                html.Div(
                    className = 'focusFigureContainer',
                    children = [
                        html.Div(
                            id = 'currentFocusFigure',
                            children = []
                        ),
                        html.Div(
                            id = "meanFocusFigure",
                            children = []
                        )
                    ]
                ),
            ],
        ),
    ],
)