from dash import html
from dash import dcc, html

layout = html.Div(
    className = 'focusResultContainer',
    children =[
        html.Div(
            className = "focusProbViewContainer",
            children = [
                html.Div(
                    className = 'titleContainer',
                    children = [
                        html.H2(
                            className = 'title',
                            children = ['집중도 그래프']
                        )
                    ]
                ),
                # section 마다의 집중도를 보여주는 보드(위에 보드)
                html.Div(
                    id = 'sectionFocusProbBoard',
                    children = [
                        # section의 학습상태의 메뉴바 화면
                        html.Div(
                            className = 'focusStateMenuBar',
                            children = [
                                html.Div(
                                    id = 'focusState 1',
                                    children = [
                                        html.Span(
                                            id = 'state1Title',
                                            children = ['학습미완료']
                                        )
                                    ]
                                ), 
                                html.Div(
                                    id = 'focusState 2',
                                    children = [
                                        html.Span(
                                            id = 'state2Title',
                                            children = ['재학습필요']
                                        )
                                    ]
                                ),
                                html.Div(
                                    id = 'focusState 3',
                                    children = [
                                        html.Span(
                                            id = 'state3Title',
                                            children = ['학습완료']
                                        )
                                    ]
                                ),
                                dcc.Dropdown(
                                    id = 'stateSectionDrop',  
                                )
                            ]
                        ),
                        # 그래프, section 선택창이 띄어지는 구간
                        # -> 여기에 'graph_layout' 레이아웃이 추가된다.
                        # state 눌렀을 때 기본 레이아웃
                        
                        html.Div(
                            className = 'focusStateGraphContainer',
                            children = [
                                dcc.Graph(
                                    id = 'sectionFocusGraph',
                                    style = {
                                        'width': '550px',
                                        'height' : '250px'
                                    }
                                ),
                                # 여기 div 에 state값에 따라 들어가는 레이아웃이 달라진다.
                                # html.Div(
                                #     id = 'sectionBox',
                                #     children = []
                                # )
                            ]
                        ),                       
                    ]
                ),
                html.Div(
                    className = 'titleContainer',
                    children = [
                        html.H2(
                            className = 'title',
                            children = ['집중도 그래프']
                        )
                    ]
                ),
                html.Div(
                    # 실시간 학습자 집중도를 보여주는 보드(아래 보드)
                    className = 'focusProbBoard',
                    children = [
                        html.Div(
                            className = 'currentElementContainer',
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
                                    },
                                ),
                                html.Div(
                                    className = 'focusFigureContainer',
                                    children = [
                                        html.Div(
                                            id = 'currentFocusFigure',
                                            children = [
                                                html.H3(
                                                    id = 'currentFocus Index',
                                                    children = ['현재집중도 :']
                                                ),
                                                html.H3(
                                                    id = 'currentFocus Result',
                                                    children = []
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            id = "durationTimeFigure",
                                            children = [
                                                html.H3(
                                                    id = 'durationTime Index',
                                                    children = ['학습시간 :']
                                                ),
                                                html.H3(
                                                    id = 'durationTime Result',
                                                    children = []
                                                )
                                            ]
                                        )
                                    ]
                                ),
                            ]
                        ),
                        html.Div(id ='divSpace_0'),
                        html.Div(id ='divSpace_1'),
                        html.Div(
                            className = 'graphContainer',
                            children = [
                                dcc.Graph(
                                    id = 'focus1',
                                    style = {
                                        'border-radius' : 10,
                                        'height' : '220px',
                                        'width' : '390px',
                                    }
                                ),
                            ]
                        ),
                    ]
                ),
            ],
        ),
    ],
)


# 1. state= 1일때 레이아웃
