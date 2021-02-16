import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import mysql.connector
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
import os
import csv
import classes
import coreNetwork_functions

app = dash.Dash(__name__, title='Core Network Dashboard')
server = app.server

# DB Connection Parameters
dbPara = classes.coreDbCredentials()

# Styles
graphTitleFontSize = 14
tabbedMenuStyle = {'background-color': 'black', 'color': 'white', 'border-bottom-color': 'black'}
tabbedMenuSelectedStyle = {'background-color': 'grey', 'color': 'white', 'border-bottom-color': 'black', 'border-top-color': 'white'}

app.layout = html.Div(
    children=[
        # Header & tabbed menu
        html.Div(
            className = 'titleHeaderContainer',
            children = [
                html.H1(
                    id = 'dashboardTitle',
                    children = 'Core Network Dashboard'
                ),
                dcc.Tabs(
                    id = 'tabsContainer',
                    value = 'MME Event Logs',
                    style = {'height':'45px'},
                    children = [
                        dcc.Tab(
                            label = 'MME Event Logs', 
                            value = 'MME Event Logs', 
                            style = tabbedMenuStyle,
                            selected_style = tabbedMenuSelectedStyle
                        ),
                        dcc.Tab(
                            label = 'Top Events', 
                            value = 'Top Events', 
                            style = tabbedMenuStyle,
                            selected_style = tabbedMenuSelectedStyle
                        )
                    ]
                )
            ]
        ),
        html.Div(
            id = 'dataTypeDropdownGridElement',
            children = [
                dcc.Dropdown(
                    id = 'dataTypeDropdown',
                    value = 'All',
                    style = {
                        'width': '100%', 
                        'font-size': str(graphTitleFontSize) + 'px', 
                        'text-align': 'center'
                    }
                )
            ]
        ),
        html.Div(
            id = 'timeFrameDropdownGridElement',
            children = [
                dcc.Dropdown(
                    id='timeFrameDropdown',
                    options=[
                        {'label':'1 Hour', 'value':'1'}, 
                        {'label':'3 Hours', 'value':'3'}, 
                        {'label':'8 Hours', 'value':'8'}, 
                        {'label':'24 Hours', 'value':'24'}
                    ],
                    # value var is the default value for the drop down.
                    value='1',
                    style={
                        'width': '100%', 
                        'font-size': str(graphTitleFontSize) + 'px', 
                        'text-align': 'center'
                    }
                )
            ]
        ),
        # MME Event Log
        html.Div(
            id = 'graphGridContainer',
            children = [
                # Graphs
                html.Div(
                    className = 'gridElement',
                    id = 'mmePieGraphGridContainer',
                    children = [
                        'MME Logs',
                        dcc.Graph(
                            id = 'mmeSessionEventsPie'
                        )
                    ]
                )
            ]
        ),
        # Top Worst Reports Tab
        html.Div(
            id = 'datatableGridContainer',
            children = [
                html.Div(
                    className = 'datatableGridElement',
                    children = [
                        html.H3('Top APN per Event'),
                        dash_table.DataTable(
                            id = 'eventDataTable',
                            style_header = {
                                'backgroundColor':'black',
                                'color':'white'
                                },
                            style_cell = {
                                'backgroundColor':'black',
                                'color':'white'
                            }
                        )
                    ]
                )
            ]
        ),
        # Network Check Tab
        html.Div(
            id = 'networkCheckGridContainer'
        ),
        # Graph Insight Tab (WIP)
        html.Div(
            id = 'graphInsightContainer'
        ),
        dcc.Interval(
            id='graphUpateInterval',
            # interval is expressed in milliseconds
            interval=120000, 
            n_intervals=0
        )
    ]
)

# We pass value from the time frame dropdown because it gets updated everytime you change the seleccion on the drop down.
@app.callback(
    [
        Output('mmeSessionEventsPie', 'figure'),
        Output('dataTypeDropdown', 'options'),
        Output('eventDataTable', 'columns'),
        Output('eventDataTable', 'data')
    ]
    , 
    [
        # We use the update interval function and tabbed menu to trigger callback
        Input('graphUpateInterval', 'n_intervals'), 
        Input('tabsContainer', 'value'), 
        Input('timeFrameDropdown', 'value'), 
        Input('dataTypeDropdown', 'value')
    ]
)
def updateGraphData_bsc(currentInterval, selectedTab, timeFrameDropdown, dataTypeDropdown):
    # Calculate the start time based on the dropdown time frame
    hoursDelta = int(timeFrameDropdown)
    startTime = (datetime.now() - timedelta(hours=hoursDelta)).strftime("%Y/%m/%d %H:%M:%S")
    # Connect to DB
    connectr = mysql.connector.connect(user=dbPara.dbUsername, password=dbPara.dbPassword, host=dbPara.dbServerIp, database=dbPara.schema)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    dropDownDict = {}
    mmeSessionEventsPie = {}
    eventDict = [{"":""}]
    if selectedTab == 'MME Event Logs':
        # Dropdown list is generated based upon the selected tab from the tabbed menu
        dropDownDict = coreNetwork_functions.getApnDropdownList(pointer, startTime)
        # Call the graph function
        mmeSessionEventsPie = coreNetwork_functions.logEventDistributionQuery(pointer, graphTitleFontSize, dataTypeDropdown, startTime)
    if selectedTab == 'Top Events':
        # Dropdown list is generated based upon the selected tab from the tabbed menu
        dropDownDict, eventList = coreNetwork_functions.getEventDropdownList(pointer, startTime)
        # Generate datatable dictionary based upon dataTypeDropdown
        eventDict = coreNetwork_functions.topEventsQuery(pointer, dataTypeDropdown, startTime, eventList)
    # Close DB connection
    pointer.close()
    connectr.close()
    return mmeSessionEventsPie, dropDownDict, [{'name':dataTypeDropdown, 'id':dataTypeDropdown}, {'name':'Occurrencies', 'id':'Occurrencies'}], eventDict

# Callback to hide/display selected tab
@app.callback([
    Output('graphGridContainer', 'style'),
    Output('datatableGridContainer', 'style'), 
    Output('networkCheckGridContainer', 'style'),
    Output('graphInsightContainer', 'style')
    ], 
    Input('tabsContainer', 'value')
)
def showTabContent(currentTab):
    if currentTab == 'MME Event Logs':
        return {'display':'grid'}, {'display':'none'}, {'display':'none'}, {'display':'none'}
    elif currentTab == 'Top Events':
        return {'display':'none'}, {'display':'grid'}, {'display':'none'}, {'display':'none'}
    elif currentTab == 'Network Check':
        return {'display':'none'}, {'display':'none'}, {'display':'grid'}, {'display':'none'}
    else:
        return {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'inline'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5010')
