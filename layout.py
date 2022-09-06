from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)

app.layout = html.Div(
    className = "main",
    children = [
        html.Div(
            className = "webCamDiv",
            children = []
        ),
        html.Div(
            className = "graphDiv",
            children  = [
                html.Div(),
                html.Div()
            ]
        )
    ]
)
