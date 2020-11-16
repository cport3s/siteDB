import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import mysql.connector
import numpy as np
import time
from datetime import datetime
from datetime import timedelta

app = dash.Dash(__name__)

# DB Connection Parameters
dbusername = 'sitedb'
dbpassword = 'BSCAltice.123'
hostip = '172.16.121.41'
dbname = 'ran_pf_data'

graphTitleFontSize = 52

app.layout = html.Div(children=[
    html.H1(
        className='titleHeader',
        children='RAN Ops Dashboard', 
        style={'text-align': 'center'}
    ),
    html.Div(
        className='dropdownFlexContainer',
        children=[
            dcc.Dropdown(
                id='timeFrameDropdown',
                options=[{'label':'1 Day', 'value':'1'}, {'label':'3 Days', 'value':'3'}, {'label':'7 Days', 'value':'7'}, {'label':'30 Days', 'value':'30'}],
                # value var is the default value for the drop down.
                value='3',
                style={'width': '100%', 'font-size': str(graphTitleFontSize) + 'px'}
            ),
            dcc.Dropdown(
                id='dataTypeDropdown',
                options=[
                    {'label':'Call Setup Success Rate', 'value':'Call Setup Success Rate'}, 
                    {'label':'Drop Call Rate', 'value':'Drop Call Rate'}, 
                    {'label':'Assignment Success Rate', 'value':'Assignment Success Rate'}, 
                    {'label':'Location Update Success Rate', 'value':'Location Update Success Rate'}
                    ],
                value='Call Setup Success Rate',
                style={'width': '100%', 'font-size': str(graphTitleFontSize) + 'px'}
            )
        ]
    ),
    html.Div(
        className='graphFlexContainer',
        children=[
            dcc.Graph(
                id='bsc01Graph'
            ),
            dcc.Graph(
                id='bsc02Graph'
            ),
            dcc.Graph(
                id='bsc03Graph'
            ),
            dcc.Graph(
                id='bsc04Graph'
            ),
            dcc.Graph(
                id='bsc05Graph'
            ),
            dcc.Graph(
                id='bsc06Graph'
            ),
            dcc.Graph(
                id='rnc01Graph'
            ),
            dcc.Graph(
                id='rnc02Graph'
            ),
            dcc.Graph(
                id='rnc03Graph'
            ),
            dcc.Graph(
                id='rnc04Graph'
            ),
            dcc.Graph(
                id='rnc05Graph'
            ),
            dcc.Graph(
                id='rnc06Graph'
            ),
            dcc.Graph(
                id='rnc07Graph'
            )
        ]
    ),
    dcc.Interval(
        id='dataUpateInterval', 
        interval=300000, 
        n_intervals=0
    ),
    dcc.Interval(
        id='graphUpateInterval', 
        interval=60000, 
        n_intervals=0
    )
])

# We pass value from the time frame dropdown because it gets updated everytime you change the seleccion on the drop down.
@app.callback([
        Output('bsc01Graph', 'figure'), 
        Output('bsc02Graph', 'figure'), 
        Output('bsc03Graph', 'figure'), 
        Output('bsc04Graph', 'figure'), 
        Output('bsc05Graph', 'figure'), 
        Output('bsc06Graph', 'figure'),
        Output('rnc01Graph', 'figure'), 
        Output('rnc02Graph', 'figure'), 
        Output('rnc03Graph', 'figure'), 
        Output('rnc04Graph', 'figure'), 
        Output('rnc05Graph', 'figure'), 
        Output('rnc06Graph', 'figure'),
        Output('rnc07Graph', 'figure')
    ], 
    [
        # We use the update interval function and both dropdown menus as inputs for the callback
        Input('dataUpateInterval', 'n_intervals'), 
        Input('timeFrameDropdown', 'value'), 
        Input('dataTypeDropdown', 'value')
    ])
def updateGraphData_bsc(currentInterval, timeFrameDropdown, dataTypeDropdown):
    bscNameList = ['BSC_01_RRA', 'BSC_02_STGO', 'BSC_03_VM', 'BSC_04_VM', 'BSC_05_RRA', 'BSC_06_STGO']
    rncNameList = ['RNC_01_RRA', 'RNC_02_STGO', 'RNC_03_VM', 'RNC_04_VM', 'RNC_05_RRA', 'RNC_06_STGO', 'RNC_07_VM']
    gsmGraphValueConversionDict = {'Call Setup Success Rate':'cssr', 'Drop Call Rate':'dcr', 'Assignment Rate':'assignmentsuccessrate', 'Location Update Success Rate':'luupdatesr'}
    umtsGraphValueConversionDict = {'Call Setup Success Rate':'csconnectionsuccessrate', 'Drop Call Rate':'csdropcallrate', 'Assignment Rate':'rrcconnectionsuccessrate', 'Location Update Success Rate':'pagingsuccessrate'}
    bscGraphList = []
    rncGraphList = []
    daysDelta = int(timeFrameDropdown)
    # starttime is the current date/time - daysdelta
    startTime = (datetime.now() - timedelta(days=daysDelta)).strftime("%Y/%m/%d %H:%M:%S")
    # Connect to DB
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    for bsc in bscNameList:
        pointer.execute('SELECT ' + gsmGraphValueConversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'' + bsc + '\' and lastupdate >= \'' + startTime + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        df = pd.DataFrame({ dataTypeDropdown:queryPayload[:,0], 'Time':queryPayload[:,1] })
        fig = px.bar(df, x="Time", y=dataTypeDropdown, title=bsc)
        # Set Graph background colores & title font size
        fig.update_layout(
            plot_bgcolor='#000000', 
            paper_bgcolor='#000000', 
            font_color='#FFFFFF', 
            title_font_size=54
        )
        # Color the graph
        fig.update_traces(marker_color='#17FF00')
        # Append the current graph to the graph list
        bscGraphList.append(fig)
        queryRaw.clear()
    for rnc in rncNameList:
        pointer.execute('SELECT ' + umtsGraphValueConversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.rnc_performance_data where nename = \'' + rnc + '\' and lastupdate >= \'' + startTime + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        df = pd.DataFrame({ dataTypeDropdown:queryPayload[:,0], 'Time':queryPayload[:,1] })
        fig = px.bar(df, x="Time", y=dataTypeDropdown, title=rnc)
        # Set Graph background colores & title font size
        fig.update_layout(
            plot_bgcolor='#000000', 
            paper_bgcolor='#000000', 
            font_color='#FFFFFF', 
            title_font_size=54
        )
        # Color the graph
        fig.update_traces(marker_color='#17FF00')
        # Append the current graph to the graph list
        rncGraphList.append(fig)
        queryRaw.clear()
    # Close DB connection
    pointer.close()
    connectr.close()
    return bscGraphList[0], bscGraphList[1], bscGraphList[2], bscGraphList[3], bscGraphList[4], bscGraphList[5], rncGraphList[0], rncGraphList[1], rncGraphList[2], rncGraphList[3], rncGraphList[4], rncGraphList[5], rncGraphList[6]

@app.callback([
        Output('bsc01Graph', 'style'), 
        Output('bsc02Graph', 'style'), 
        Output('bsc03Graph', 'style'), 
        Output('bsc04Graph', 'style'), 
        Output('bsc05Graph', 'style'), 
        Output('bsc06Graph', 'style'), 
        Output('rnc01Graph', 'style'), 
        Output('rnc02Graph', 'style'), 
        Output('rnc03Graph', 'style'), 
        Output('rnc04Graph', 'style'), 
        Output('rnc05Graph', 'style'), 
        Output('rnc06Graph', 'style'), 
        Output('rnc07Graph', 'style')
    ], 
    [
        Input('graphUpateInterval', 'n_intervals')
    ])
def hideGraph(currentInterval):
    if currentInterval%2 == 0:
        return {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}
    else:
        return {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5006')