from dash import html
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output,ctx

# Define the navbar structure
def FocusFigure():

    # layout = html.Div([
    #     dbc.NavbarSimple(
    #         children=[
    #             dbc.NavItem(dbc.NavLink("Page 1", href="/page1")),
    #             dbc.NavItem(dbc.NavLink("Page 2", href="/page2")),
    #         ] ,
    #         brand="Multipage Dash App",
    #         brand_href="/page1",
    #         color="dark",
    #         dark=True,
    #     ), 
    # ])
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

    return layout

       