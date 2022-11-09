from dash import html
from dash import dcc, html

layout = html.Div(
    className = 'focusResultContainer',
    children =[
        html.Div(
            className = 'titleContainer',
            children = [
                html.H2(
                    className = 'title',
                    children = ['집중도그래프확인']
                )
            ]
        ),
        html.Div(
            className = 'graphContainer',
            children = [
                dcc.Graph(
                    id = 'focus1',
                    style = {
                        'border-radius' : '15px', 
                    }
                ),
            ]
        ),
        html.Div(
            className = "focusProbViewContainer",
            children = [
                html.Div(
                    className = 'titleContainer',
                    children = [
                        html.H2(
                            className = 'title',
                            children = ['집중도 현황판']
                        )
                    ]
                ),
                html.Div(
                    className = 'focusProbBoard',
                    children = [
                        html.Img(
                            src = "/video",
                            id = "facePhoto",
                            style = {
                                'border' : '1px solid #ddd',
                                "border-radius" : '10px',
                                'padding' : '5px',
                                'width' : '220px',
                                'box-shadow' :  '0 5px 18px -7px rgb(185, 185, 185)',
                            }
                        ),
                        html.Div(id ='divSpace_0'),
                        html.Div(id ='divSpace_1'),
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
                    ]
                ),
            ],
        ),
    ],
)