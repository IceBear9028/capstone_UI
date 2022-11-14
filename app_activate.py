import plotly
import numpy as np
from dash_player import DashPlayer
from dash import Dash, dcc, html, Input, Output,ctx, State
from flask import Flask, Response, request
from src.model_api.streamer import Streamer
from src.datastroage.graph_data import Datamanage
from src.web_function.focus_notice import focus_notice_player
import dash_bootstrap_components as dbc

import focus_page 

graph_datamanage = Datamanage()
streamcam = Streamer()
focus_notice = focus_notice_player()

global video_time
video_time = 0
focus_result = streamcam.focus_prob
# -> 사용자의 집중도 결과를 저장 ()



# 1. 데이터 프레임 불러오기

confirm = 'confirmSection'
graph_figure = 'focus1'
frame = 'webcam_frame'
focus_marking_player = 'focus_marking_player'
interval = 'interval'
video_player = 'video_player'
video_current_time = 'videoCurrentTime'
marking_color_info_container = 'markingColorInfoContainer'

focus_container = 'focusContainer'
current_focus_figure = 'currentFocusFigure'
mean_focus_figure = 'meanFocusFigure'
activate_focus_figure = 'focusFigureActivateBtn'
focus_header = 'focusHeader'
focus_header_child1 = 'focusHeaderChild1'

# section별 그래프 보여주는 기능 이름들
# a. state별로 데이터 수집 & 레이아웃 추가하는 기능
section_focus_prob_board = 'sectionFocusProbBoard'
focus1 = 'focusState_1'
focus2 = 'focusState_2'
focus3 = 'focusState_3'
section_focus_graph = 'sectionFocusGraph'

dropdown = 'stateSectionDrop'


# state 의 sectoin 버튼 아이디를 section 의 숫자로 바꾸기 위한 딕셔너리
convert_trigeredid_to_num = {}
for i in range(30):
    convert_trigeredid_to_num['btn {0}'.format(i)] = i

# state의  secton 버튼 아이디를 section 의 
convert_to_statenum = {
    focus1 : 1,
    focus2 : 2,
    focus3 : 3
}

# state 값을 색으로 변환
convert_state_to_color = {
    1 : '#D0D2D8',
    2 : '#E1876B',
    3 : '#A6DB76'
}

# state 버튼 id를 style 에 맞는 색으로 변환
convert_id_to_style_color = {
    focus1 : '#D0D2D8',
    focus2 : '#F7C4B5',
    focus3 : '#B2E492'
}
#EDB29F

# 3. 웹 레이아웃 설정
server = Flask(__name__)
app = Dash(__name__, server=server, external_stylesheets=[dbc.icons.FONT_AWESOME])
# font awesome 을 사용하려면 외부 스타일시트를 dbc로 다운받는다.


# 도움받은 사이트 :
# https://community.plotly.com/t/dash-player-custom-component-playing-and-controlling-your-videos-with-dash/12349

app.layout = html.Div(
    className = "container",
    children = [
        # 폰트 사용을 위한 외부 js 파일 다운
        # html.Script(
        #     src = "https://kit.fontawesome.com/abfbdf2860.js",
        #     crossOrigin = "anonymous"
        # ),
        dcc.ConfirmDialog(
            id = confirm,
            message = '영상구간을 다시 재학습할건가요?'
        ),
        dcc.ConfirmDialog(
            id = 'confirmSectionEscape',
            message = '학습이 완료되지 않았습니다. 그래도 다음구간으로 넘어갈까요?'
        ),
        dcc.Interval(
            id = interval,
            disabled = False,
            interval = 1*1000,
            n_intervals= 0,
        ),
        html.Div(
            className = 'playerContainer',
            children = [
                    html.Div(
                        className = 'titleContainer',
                        children = [
                            html.H2(
                                id = 'title',
                                children = [
                                    html.I(
                                        className = "fa-solid fa-film",
                                        ),
                                    ' Focus Player'
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        id = video_current_time,
                        children = []
                    ),
                    DashPlayer(
                        # 도움받은 사이트 :
                        # https://community.plotly.com/t/dash-player-custom-component-playing-and-controlling-your-videos-with-dash/12349
                        id = video_player,
                        # url = "assets/test_Video/JSON프론트엔드2.mp4",
                        url = "assets/test_Video/뉴진스(NewJeans)'Attention'.mp4",
                        # url = "assets/test_Video/실험계획법.mp4",
                        controls = True,
                        width ='900px',
                        height = '490px',
                        style = {
                            'display' : 'flex',
                            'justify-content' : 'center',
                            'align-content' : 'center'
                        }
                    ),
                    html.Div(
                        className = 'foucsMarkingPlayerContainer',
                        children = [
                            html.Div(
                                id = focus_header,
                                children = [
                                    html.Div(
                                        id = focus_header_child1,
                                        children = [
                                            # html.H2(
                                            #     id = 'focusNoticeTitle',
                                            #     children = ['집중도저하구간 확인']
                                            # ),
                                            html.Div(
                                                className = marking_color_info_container,
                                                children = [
                                                    html.Div(
                                                        className = 'Red InfoContainer',
                                                        children = [
                                                            html.Div(className = 'red Color'),
                                                            html.Span(
                                                                className = 'red Info',
                                                                children = ['재학습필요']
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(
                                                        className = 'Green InfoContainer',
                                                        children = [
                                                            html.Div(className = 'green Color'),
                                                            html.Span(
                                                                className = 'green Info',
                                                                children = ['학습완료']
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(
                                                        className = 'Gray InfoContainer',
                                                        children = [
                                                            html.Div(className = 'gray Color'),
                                                            html.Span(
                                                                className = 'gray Info',
                                                                children = ['학습미완료']
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        children = [
                                            html.I(
                                                className = "fa-solid fa-magnifying-glass",
                                                style = {'color':'#fff', 'font-size' : '15px','margin-right' : '10px'}
                                            ),
                                            "집중도 상세보기"],
                                        id = activate_focus_figure,
                                        n_clicks = 0,
                                    ),
                                ]
                            ),
                            html.Div(
                                id = focus_marking_player,
                                children = focus_notice.sections,
                                style = {
                                    'background' : '#E9E9E9',
                                    'width' : '{0}px'.format(focus_notice.section_container_width),
                                    'height' : '80px',
                                    'border-radius' : '10px',
                                    # 'border' : '1px solid #D0D2D8',
                                    'padding' : '3px',
                                    'display' : 'flex',
                                    'flex-direction' : 'row',
                                    'justify-content' : 'center',
                                    'box-shadow' : '0 5px 15px -7px rgba(190,190,190,4)',
                                    }
                            ),
                        ]
                    ),
                    html.Img(
                        src = "/video",
                        id = "facePhoto",
                        style = {
                            'width' : '0px',
                            'height' : '0px'
                        }
                    ),
            ]
        ),
        html.Div(
            id = 'focusContainer',
            children = [],
            style = {
                'display' : 'flex',
                'align-content' : 'space-between'
            }
        )
    ]
)
    
# 동영상 프로그레시브 바 추가

# 그린 -> 집중
# 레드 -> 비집중
# 옐로우 -> 진행중 

# 그래프 뜨는것, 구간별로 확인



# section 이동시 알림창 띄어주는 기능구현
@app.callback(
    Output(confirm, 'displayed'),
    Output('confirmSectionEscape', 'displayed'),
    focus_notice.marge_sections_Input
)
def confirm_relearn(*args):
    # 0. section이 선택되었을 때, section의 위치를 저장한다.
    focus_notice.clicked_section = ctx.triggered_id

    # A. section을 선택했을 때, 재학습할지말지 confirm 창을 띄어주는 코드 [situation_A]
    if not type(focus_notice.sections_check['time'][ctx.triggered_id]) == bool:
        # 이미 section의 학습이 끝나서 section_state 를 부여받은 경우에 대해서 재학습 여부를 물어보게 된다.
        if focus_notice.sections_check['section_state'][ctx.triggered_id] == 2 or \
            focus_notice.sections_check['section_state'][ctx.triggered_id] == 3:
            return  True, False

    # B. 현재 section의 학습이 완료되지 않았는데, 다른 section으로 넘어갈지 말지 confirm 창을 띄어주는 코드 [situation_B]
    return  False,True

# focus_notice_player 클래스 기능구현
@app.callback(
    Output(video_player, 'seekTo'),
    Input('video_player', 'duration'),
    Input(confirm, 'submit_n_clicks'),
    Input('confirmSectionEscape', 'submit_n_clicks')
)
def generate_notice(duration_time, situation_A, situation_B):
    # sections_timeline 딕셔너리를 만들기 위한 코드.
    # 한번만 실행하면 되기 때문에 TF 변수에 스위치 역할을 구현한 것.
    global video_time
    if focus_notice.generate_section_TF == False:
        focus_notice.generate_section(duration_time)
        focus_notice.generate_section_TF = True

    else:
        # A,B 상황에 대해서 학습자가 다른 section의 학습을 원할 때 위에서 저장한 section의 위치로 이동한다.
        if situation_A or situation_B :
            # 재학습하는 것이기 때문에, 해당 section 에 대해서 모두 초기화를 시킨다.
            focus_notice.sections_check['time'][focus_notice.clicked_section] = False
            focus_notice.sections_check['prob'][focus_notice.clicked_section] = np.array([])
            focus_notice.sections_check['section_state'][focus_notice.clicked_section] = 0
            focus_notice.sections_check['real_time'][focus_notice.clicked_section] = []

            # 그리고 해당 section 으로 넘어간다.
            return focus_notice.sections_timeline[focus_notice.clicked_section]
            
        # 다른 section으로 넘어가기를 원치 않을 때 계속 영상을 보게 된다.

#현재의 집중도를 확인하는 기능
@app.callback(
    Output('currentFocus Result', 'children'),
    Output('durationTime Result','children'),
    Input(interval, 'n_intervals')
)
def focus_check(time):
    # focus = graph_datamanage.data['focus_prob'].pop()
    # focus_result = np.trunc(graph_datamanage.data['focus_prob'].pop() * 100)
    # focus_result = round(graph_datamanage.data['focus_prob'].pop(), 2)
    minute, second = np.divmod(time, 60)
    focus = graph_datamanage.data['focus_prob']
    return str(round(focus[-1]*100, 2)) + '%', ' {0}min {1}sec'.format(minute, second)


# section_time 저장 기능 
@app.callback(
    Output(video_current_time, 'children'),
    Input(interval, 'n_intervals'),
    Input(video_player, 'currentTime')
)
def current_time_check(n, current_time):
    global video_time
    video_time = int(current_time)
    focus_notice.section_mean_cal(graph_datamanage.data['video_time'],graph_datamanage.data['focus_prob'])
    focus_notice.save_section_state(current_time)

    return [html.Span(n)]


# sections_state값에 따른 section 의 style 변경
@app.callback(
    focus_notice.marge_sections_Output,
    Input(interval, 'n_intervals'),
    # Input(video_player, 'currentTime')
)
def update_section(interval):
    global video_time
    current_section = focus_notice.find_section_id(video_time, value_type='num')
    style_list = []
    for state_value in focus_notice.sections_check['section_state'].values():
        style_list.append(focus_notice.set_section_style(state_value))
    
    # 현재 동영상 시간을 받아서, 현재위치의 section을 알리는 style 을 추가한다.
    # style_list[current_section]['border-bottom'] = '5px solid red'
    # style_list[current_section]['box-shadow'] = '0 5px 18px -7px rgba(0,0,0,4)'
    style_list[current_section]['border-bottom'] = '8px solid red'

    # ++ 양끝단의 section을 둥글게 스타일처리하는 코드추가
    # 1. 'btn 0'의 border-radius 추가
    style_list[0]['border-top-left-radius'] = '8px'
    style_list[0]['border-bottom-left-radius'] = '8px'

    # 2, 'btn 29'의 border-radius 추가
    style_list[-1]['border-top-right-radius'] = '8px'
    style_list[-1]['border-bottom-right-radius'] = '8px'

    return style_list


# 버튼 눌렀을 때 페이지 나오게 설정
@app.callback(
    Output(focus_container, 'children'),
    Input(activate_focus_figure, 'n_clicks'),
    #Input(activate_focus_figure, 'pathname'),
)
def activate_focus_figure_page(n):
    # 버튼이 눌리면
    if n%2 == 1:
        return focus_page.layout

# state 버튼을 눌렀을 때 해당되는 section 이 dropdown 에 업데이트
@app.callback(
    Output(dropdown, 'options'),
    Input(focus1, 'n_clicks'),
    Input(focus2, 'n_clicks'),
    Input(focus3, 'n_clicks'),
)
def dropdown_activate(n1, n2, n3):
    clicked_state = convert_to_statenum[ctx.triggered_id]
    options = []
    for key,value in focus_notice.sections_check['section_state'].items():
        if value == clicked_state:
            options.append({'label' : '{} section'.format(convert_trigeredid_to_num[key] + 1), 'value' : key})

    return options


# 그리고 버튼이 눌리는 효과 스타일 업데이트로 설정
@app.callback(
    Output(focus1, 'style'),
    Output(focus2, 'style'),
    Output(focus3, 'style'),
    Input(focus1, 'n_clicks'),
    Input(focus2, 'n_clicks'),
    Input(focus3, 'n_clicks'),
    # State(focus1, 'style'),
    # State(focus2, 'style'),
    # State(focus3, 'style'),
)
def state_button_style_update(*args):
    # 1. 처음 모든 버튼들의 스타일음 담는 리스트를 만든다.
    # ++ 순서는 Input이 먼저 적힌 순서
    button_style_list = [None, None, None]

    # 2. 눌린 버튼에 적용할 스타일 값에 대한 리스트에 넣을 위치를 찾는다.
    # ++ 버튼이 눌린 아이디에 맞는 state 를 알려주는 딕셔너리 재사용
    change_btn_location = convert_to_statenum[ctx.triggered_id] - 1
    
    # 3. 눌린 버튼의 style을 리스트에 업데이트 한다.
    button_style_list[change_btn_location] = {
        'background-color' : convert_id_to_style_color[ctx.triggered_id]}

    # 4. 최종적으로 적용된 스타일이 담긴 리스트를 return 한다.
    return button_style_list

# dropdown에 선택한 section 의 데이터를 그래프로 plot
@app.callback(
    Output(section_focus_graph, 'figure'),
    Input(dropdown, 'value')
)
def show_graph_section(value):
    # 1. 해당 section 의 state에 해당하는 색을 찾는다.
    color = convert_state_to_color[focus_notice.sections_check['section_state'][value]]

    # 2. 그래프에 해당 색을 입힌다.
    fig = plotly.tools.make_subplots(rows = 1, cols = 1)
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig.append_trace({
        'x' : focus_notice.sections_check['real_time'][value],
        'y' : focus_notice.sections_check['prob'][value],
        'name' : 'focus',
        'type' : 'scatter',
        'mode' : 'lines',
        'marker_color' : color
    },1,1)
    fig.append_trace({
        'x' : focus_notice.sections_check['real_time'][value],
        'y' : np.full((1,len(focus_notice.sections_check['real_time'][value])),50)[0],
        'name' : 'threshold',
        'type' : 'scatter',
        'mode' : 'lines',
        'marker_color' : 'rgb(230,230,230)'
    },1,1)
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )
    fig.update_yaxes(range = [-10,105])
    # 그래프 margin 제거
    fig['layout'].update(
        margin = dict(l=40, r=20, b=30, t=15 ),        
    )
    return fig
    

# 그래프 속성 설정
@app.callback(
    Output(graph_figure, 'figure'),
    Input(interval, 'n_intervals')
)
def focus_1(num):
    fig = plotly.tools.make_subplots(rows = 1, cols = 1)
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig.append_trace({
        'x' : graph_datamanage.data['real_time'],
        'y' : graph_datamanage.data['focus_prob'],
        'name' : 'focus',
        'type' : 'scatter',
        'mode' : 'lines',
        'marker_color' : '#b4cbf3'
    },1,1)
    fig.append_trace({
        'x' : graph_datamanage.data['real_time'],
        'y' : np.full((1,len(graph_datamanage.data['focus_prob'])),0.5)[0],
        'name' : 'threshold',
        'type' : 'scatter',
        'mode' : 'lines',
        'marker_color' : 'rgb(230,230,230)'
    },1,1)
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )
    fig.update_yaxes(range = [-0.1,1.1])
    # 그래프 margin 제거
    fig['layout'].update(
        margin = dict(l=40, r=20, b=30, t=15 ),        
    )
    return fig



# 5. 웹캠 연결용 서버
@server.route('/video')
def stream():
    src = request.args.get('src', default=0, type = int)
    try :
        return Response(stream_gen( src ) ,
                        mimetype='multipart/x-mixed-replace; boundary=frame' )
    except Exception as e :
        print('[wandlab] ', 'stream error : ',str(e))
def stream_gen( src ):   
    try : 
        streamcam.run( src )
        while True :
            # 1. 갖고온 frame 으로 웹페이지에 넣어줌
            frame = streamcam.bytescode()
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
            # 2. 깆고온 frame 으로 집중도 추출 및 현재시간과 영상시청 시간 기록
            # print(focus_notice.sections_check)
            graph_datamanage.current_time, graph_datamanage.focus_prob = streamcam.focus_result()
            graph_datamanage.video_time = video_time
            graph_datamanage.start()
            graph_datamanage.data_cut()
                    
    except GeneratorExit :
        streamcam.stop()


# 최종 서버 돌아감
if __name__ == '__main__':
    app.run_server(debug=True)




# $ pip install --upgrade pip
# $ pip install cython
# $ pip install "numpy<17"
# $ pip install imutils
# $ pip install flask
# $ pip install opencv-python
# $ pip install opencv-contrib-python