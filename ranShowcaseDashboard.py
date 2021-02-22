import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import mysql.connector
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
import os
import csv
# Custom libraries
import classes
import styles
import ran_functions
app = dash.Dash(__name__)
server = app.server

# DB Connection Parameters
dbPara = classes.dbCredentials()
ranController = classes.ranControllers()
graphColors = styles.NetworkWideGraphColors()
# Instantiate styles class
gridContainerStyles = styles.gridContainer()
gridelementStyles = styles.gridElement()
graphTitleFontSize = 52

app.layout = html.Div(children=[
    html.H1(
        className='showCasetitleHeader',
        children='RAN Ops Dashboard', 
        style={
            'text-align': 'center',
            'color':'white'
            }
    ),
    html.Div(
        id='gsmGraphGridContainer',
        style=gridContainerStyles.gsmGraphGridContainerStyle,
        children=[
            dcc.Graph(
                id='gsmCsCssr',
                style=gridelementStyles.gsmCsCssrStyle
            ),
            dcc.Graph(
                id='gsmPsCssr',
                style=gridelementStyles.gsmPsCssrStyle
            ),
            dcc.Graph(
                id='gsmCsDcr',
                style=gridelementStyles.gsmCsDcrStyle
            )
        ]
    ),
    html.Div(
        id='umtsGraphGridContainer',
        style=gridContainerStyles.umtsGraphGridContainerStyle,
        children=[
            dcc.Graph(
                id='umtsDcr',
                style=gridelementStyles.umtsDcrStyle
            ),
            dcc.Graph(
                id='hsdpaDcr',
                style=gridelementStyles.hsdpaDcrStyle
            ),
            dcc.Graph(
                id='hsupaDcr',
                style=gridelementStyles.hsupaDcrStyle
            ),
            dcc.Graph(
                id='umtsCssr',
                style=gridelementStyles.umtsCssrStyle
            ),
            dcc.Graph(
                id='hsdpaCssr',
                style=gridelementStyles.hsdpaCssrStyle
            ),
            dcc.Graph(
                id='hsupaCssr',
                style=gridelementStyles.hsupaCssrStyle
            )
        ]
    )
    ,
    html.Div(
        id='lteGraphGridContainer',
        style=gridContainerStyles.lteGraphGridContainerStyle,
        children=[
            dcc.Graph(
                id='lteVolteCssr',
                style=gridelementStyles.lteVolteCssrStyle
            ),
            dcc.Graph(
                id='lteDataCssr',
                style=gridelementStyles.lteDataCssrStyle
            ),
            dcc.Graph(
                id='lteVolteDcr',
                style=gridelementStyles.lteVolteDcrStyle
            ),
            dcc.Graph(
                id='lteDataDcr',
                style=gridelementStyles.lteDataDcrStyle
            )
        ]
    ),
    dcc.Interval(
        id='graphUpateInterval',
        # interval is expressed in milliseconds (evey 30mins)
        interval=1800000, 
        n_intervals=0
    ),
    dcc.Interval(
        id='viewUpateInterval',
        # interval is expressed in milliseconds (evey 1min)
        interval=60000, 
        n_intervals=0
    )
])

# Callback to update the graph data
@app.callback([
        Output('gsmCsCssr', 'figure'),  
        Output('gsmPsCssr', 'figure'), 
        Output('gsmCsDcr', 'figure'),
        Output('umtsCssr', 'figure'),
        Output('hsdpaCssr', 'figure'),
        Output('hsupaCssr', 'figure'),
        Output('umtsDcr', 'figure'),
        Output('hsdpaDcr', 'figure'),
        Output('hsupaDcr', 'figure'),
        Output('lteVolteDcr', 'figure'),
        Output('lteDataDcr', 'figure'),
        Output('lteVolteCssr', 'figure'),
        Output('lteDataCssr', 'figure')
    ],  
    Input('graphUpateInterval', 'n_intervals'))
def updateGraph(currentInterval):
    # starttime is the current date/time - daysdelta
    startTime = 3
    # Connect to DB
    connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    # Create plots
    gsmCsCssr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    gsmPsCssr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    gsmCsDcr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    umtsCssr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    hsdpaCssr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    hsupaCssr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    umtsDcr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    hsdpaDcr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    hsupaDcr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    lteVolteDcr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    lteDataDcr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    lteVolteCssr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    lteDataCssr = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    # Function to populate graph data
    lteVolteCssr, lteDataCssr, lteVolteDcr, lteDataDcr = ran_functions.populateLteGraphs(pointer, startTime, ranController.lteBandList, lteVolteCssr, lteDataCssr, lteVolteDcr, lteDataDcr)
    # Customize graph layout
    lteDataCssr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='4G Data eRAB SSR'
    )
    lteVolteCssr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color,  
        title_font_size=graphTitleFontSize,
        title='4G VoLTE eRAB SSR'
    )
    lteDataDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='4G Data DCR'
    )
    lteVolteDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='4G VoLTE DCR'
    )
    umtsCssr, hsdpaCssr, hsupaCssr, umtsDcr, hsdpaDcr, hsupaDcr = ran_functions.populateUmtsGraphs(pointer, startTime, ranController.rncNameList, umtsCssr, hsdpaCssr, hsupaCssr, umtsDcr, hsdpaDcr, hsupaDcr)
    hsdpaCssr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='HSDPA CSSR'
    )
    hsupaCssr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='HSUPA CSSR'
    )
    umtsCssr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='CS CSSR'
    )
    hsdpaDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='HSDPA DCR'
    )
    hsupaDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='HSUPA DCR'
    )
    umtsDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='CS DCR'
    )
    gsmCsCssr, gsmPsCssr, gsmCsDcr = ran_functions.populateGsmGraphs(pointer, startTime, ranController.bscNameList, gsmCsCssr, gsmPsCssr, gsmCsDcr)
    gsmCsCssr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='2G CS CSSR'
    )
    gsmPsCssr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='2G PS CSSR'
    )
    gsmCsDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        title_font_size=graphTitleFontSize,
        title='2G CS DCR'
    )
    # Close DB connection
    pointer.close()
    connectr.close()
    return gsmCsCssr, gsmPsCssr, gsmCsDcr, umtsCssr, hsdpaCssr, hsupaCssr, umtsDcr, hsdpaDcr, hsupaDcr, lteVolteDcr, lteDataDcr, lteVolteCssr, lteDataCssr

# Callback to update the view
@app.callback([
        Output('gsmGraphGridContainer', 'style'),  
        Output('umtsGraphGridContainer', 'style'), 
        Output('lteGraphGridContainer', 'style'),
    ],  
    Input('viewUpateInterval', 'n_intervals'))
def updateView(currentInterval):
    if currentInterval%3 == 0:
        return {'display':'grid'}, {'display':'none'}, {'display':'none'}
    elif currentInterval%3 == 1:
        return {'display':'none'}, {'display':'grid'}, {'display':'none'}
    elif currentInterval%3 == 2:
        return {'display':'none'}, {'display':'none'}, {'display':'grid'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5015')