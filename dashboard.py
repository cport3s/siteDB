#-----------------------------------------------------------------LIBRARIES-----------------------------------------------------------------#
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import mysql.connector
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
import os
import csv

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    children = [
        html.Div(
            id = "gridContainer",
            style = {"display": "grid", "grid-template": "repeat(2, 1fr) / repeat(4, 1fr)", "color": "white"},
            children = [
                html.Div(
                    className = "gridElement",
                    id = "gridElement1",
                    style = {"border": "1px solid red"},
                    children = [
                        "Element 1",
                        dcc.Graph(
                            id='trxUsageGraph1'
                        )
                    ]
                ),
                html.Div(
                    className = "gridElement",
                    id = "gridElement2",
                    children = [
                        "Element 2",
                        dcc.Graph(
                            id='trxUsageGraph2'
                        )
                    ]
                ),
                html.Div(
                    className = "gridElement",
                    id = "gridElement3",
                    children = [
                        "Element 3",
                        dcc.Graph(
                            id='trxUsageGraph3'
                        )
                    ]
                ),
                html.Div(
                    className = "gridElement",
                    id = "gridElement4",
                    children = [
                        "Element 4",
                        dcc.Graph(
                            id='trxUsageGraph4'
                        )
                    ]
                ),
                html.Div(
                    className = "gridElement",
                    id = "gridElement5",
                    children = [
                        "Element 5",
                        dcc.Graph(
                            id='trxUsageGraph5'
                        )
                    ]
                ),
                html.Div(
                    className = "gridElement",
                    id = "gridElement6",
                    children = [
                        "Element 6",
                        dcc.Graph(
                            id='trxUsageGraph6'
                        )
                    ]
                ),
                html.Div(
                    className = "gridElement",
                    id = "gridElement7",
                    children = [
                        "Element 7",
                        dcc.Graph(
                            id='trxUsageGraph7'
                        )
                    ]
                ),
                html.Div(
                    className = "gridElement",
                    id = "gridElement8",
                    children = [
                        "Element 8",
                        dcc.Graph(
                            id='trxUsageGraph8'
                        )
                    ]
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5005')