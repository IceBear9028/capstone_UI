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
                            children = [
                                html.I(
                                    className = "fa-solid fa-arrow-trend-up",
                                    style = {
                                        'margin-right' : '5px'
                                    }
                                ),
                                ' 구간별 집중도그래프']
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
                                    className = 'elementContainer',
                                    children = [
                                        html.Div(
                                            id = 'focusState_1',
                                            children = [
                                                html.I(
                                                    className = "fa-solid fa-reply",
                                                    style = {'font-size' : '20px', 'color' : '#6f6f6f'}
                                                    ),
                                                html.Span(
                                                    id = 'state1Title BTN',
                                                    children = [
                                                        '학습미완료']
                                                )
                                            ]
                                        ), 
                                        html.Div(
                                            id = 'focusState_2',
                                            children = [
                                                html.I(
                                                    className = "fa-solid fa-face-tired",
                                                    style = {'font-size' : '20px','color' : '#6f6f6f'}
                                                    ),
                                                html.Span(
                                                    id = 'state2Title BTN',
                                                    children = [
                                                        '재학습필요']
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            id = 'focusState_3',
                                            children = [
                                                html.I(
                                                    className = "fa-solid fa-face-smile",
                                                    style = {
                                                        'font-size' : '20px',
                                                        'color' : '#6f6f6f',
                                                        }
                                                    ),
                                                html.Span(
                                                    id = 'state3Title BTN',
                                                    children = [
                                                        '  학습완료']
                                                )
                                            ]
                                        ),
                                    ]
                                ),
                                html.Div(
                                    className = 'dropdownContainer',
                                    children = [
                                        html.Span(
                                            id = 'dropdownHeader',
                                            children = ['구간 선택']
                                        ),
                                        dcc.Dropdown(
                                            id = 'stateSectionDrop',
                                            style = {
                                                'width' : '140px',
                                                'border-radius' : '10px',
                                                'border' : '0px',
                                                'background-color' : 'rgb(220, 220, 220)'
                                            }
                                        )
                                    ]
                                ),
                            ]
                        ),
                        # 그래프, section 선택창이 띄어지는 구간
                        # -> 여기에 'graph_layout' 레이아웃이 추가된다.
                        # state 눌렀을 때 기본 레이아웃
                        
                        html.Div(
                            id = 'focusStateGraphContainer',
                            children = [
                                dcc.Graph(
                                    id = 'sectionFocusGraph',
                                    style = {
                                        'width': '510px',
                                        'height' : '310px'
                                    }
                                )
                            ]
                        ),                       
                    ]
                ),
                html.Div(
                    className = 'titleContainer',
                    children = [
                        html.H2(
                            className = 'title',
                            children = [
                                html.I(
                                    className = "fa-solid fa-repeat",
                                    style = {
                                        'margin-right' : '5px'
                                    }
                                ),
                                ' 실시간 집중도']
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
                                        'border' : '1px solid rgb(240, 240, 240)',
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
                                                    children = ['총학습시간 :']
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
                        html.Div(
                            className = 'graphContainer',
                            children = [
                                dcc.Graph(
                                    id = 'focus1',
                                    style = {
                                        'border-radius' : '8px',
                                        'height' : '230px',
                                        'width' : '410px',
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
