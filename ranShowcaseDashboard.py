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
import os
import csv
import classes

app = dash.Dash(__name__)
server = app.server

# DB Connection Parameters
dbPara = classes.dbCredentials()

loopCounter = 1
ranController = classes.ranControllers()
graphTitleFontSize = 52

app.layout = html.Div(children=[
    html.H1(
        className='titleHeader',
        children='RAN Ops Dashboard', 
        style={'text-align': 'center'}
    ),
    html.Div(
        className='dropdownFlexContainer',
        id='dropDownContainer',
        children=[
            dcc.Dropdown(
                id='dataTypeDropdown',
                options=[
                    {'label':'CS Call Setup Success Rate', 'value':'CS Call Setup Success Rate'}, 
                    {'label':'PS Call Setup Success Rate', 'value':'PS Call Setup Success Rate'}, 
                    {'label':'CS Drop Call Rate', 'value':'CS Drop Call Rate'}, 
                    {'label':'PS Drop Call Rate', 'value':'PS Drop Call Rate'}, 
                    {'label':'Assignment Success Rate', 'value':'Assignment Success Rate'}, 
                    {'label':'Location Update Success Rate', 'value':'Location Update Success Rate'}
                ],
                value='CS Call Setup Success Rate',
                style={'width': '100%', 'font-size': str(graphTitleFontSize) + 'px', 'text-align': 'center'}
            ),
            dcc.Dropdown(
                id='timeFrameDropdown',
                options=[
                    {'label':'1 Day', 'value':'1'}, 
                    {'label':'3 Days', 'value':'3'}, 
                    {'label':'7 Days', 'value':'7'}, 
                    {'label':'30 Days', 'value':'30'}
                ],
                # value var is the default value for the drop down.
                value='3',
                style={'width': '100%', 'font-size': str(graphTitleFontSize) + 'px', 'text-align': 'center'}
            )
        ]
    ),
    html.Div(
        className='bscGraphFlexContainer',
        id='bscGraphFlexContainer',
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
            )
        ]
    ),
    html.Div(
        className='rncGraphFlexContainer',
        id='rncGraphFlexContainer',
        children=[
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
    html.Div(
        className='trxGraphFlexContainer',
        children=[
            dcc.Graph(
                id='trxUsageGraph'
            ),
            dcc.Graph(
                id='oosNeGraph'
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
        Output('rnc07Graph', 'figure'),
        Output('trxUsageGraph', 'figure'),
        Output('oosNeGraph', 'figure')
    ], 
    [
        # We use the update interval function and both dropdown menus as inputs for the callback
        Input('dataUpateInterval', 'n_intervals'), 
        Input('timeFrameDropdown', 'value'), 
        Input('dataTypeDropdown', 'value')
    ])
def updateGraphData_bsc(currentInterval, timeFrameDropdown, dataTypeDropdown):
    gsmGraphValueConversionDict = {'CS Call Setup Success Rate':'cssr', 'PS Call Setup Success Rate':'edgedlssr', 'CS Drop Call Rate':'dcr', 'PS Drop Call Rate':'edgedldcr', 'Assignment Success Rate':'assignmentsuccessrate', 'Location Update Success Rate':'luupdatesr'}
    umtsGraphValueConversionDict = {'CS Call Setup Success Rate':'csconnectionsuccessrate', 'PS Call Setup Success Rate':'psrtsuccessrate', 'CS Drop Call Rate':'csdropcallrate', 'PS Drop Call Rate':'psdropcallrate', 'Assignment Success Rate':'rrcconnectionsuccessrate', 'Location Update Success Rate':'pagingsuccessrate'}
    bscGraphList = []
    rncGraphList = []
    daysDelta = int(timeFrameDropdown)
    # starttime is the current date/time - daysdelta
    startTime = (datetime.now() - timedelta(days=daysDelta)).strftime("%Y/%m/%d %H:%M:%S")
    # Connect to DB
    connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
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
            plot_bgcolor='#2F2F2F', 
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
            plot_bgcolor='#2F2F2F', 
            paper_bgcolor='#000000', 
            font_color='#FFFFFF', 
            title_font_size=54
        )
        # Color the graph
        fig.update_traces(marker_color='#17FF00')
        # Append the current graph to the graph list
        rncGraphList.append(fig)
        queryRaw.clear()
    tempDataFrame = {'neName':[], 'ipPoolId':[], 'trxQty':[]}
    # Loop through BSC Names
    for ne in bscNameList:
        # Loop through Ip Pool ID range (10 - 12)
        for ippool in range(10,13):
            tempDataFrame['neName'].append(ne)
            # Must change ippool to string for the bar chart to display in group mode.
            tempDataFrame['ipPoolId'].append(str(ippool))
            pointer.execute('SELECT trxqty FROM ran_pf_data.trx_usage_data where lastupdate >= \'' + datetime.now().strftime("%Y/%m/%d") + '\' and nename = \'' + ne + '\' and ippoolid = ' + str(ippool) + ' order by lastupdate desc;')
            queryPayload = pointer.fetchone()
            # Must check if query result is empty, to full with 0
            if queryPayload:
                # Take the latest value on the DB
                tempDataFrame['trxQty'].append(queryPayload[0])
            else:
                tempDataFrame['trxQty'].append(0)
    ipPoolReportDf = pd.DataFrame(tempDataFrame, columns = ['neName', 'ipPoolId', 'trxQty'])
    trxUsageGraph = px.bar(ipPoolReportDf, x='neName', y='trxQty', color='ipPoolId', barmode='group', template='simple_white', height=700)
    trxUsageGraph.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=54,
        font_size=30,
        title='TRX Load per Interface'
    )
    # Set Y Axes Range
    trxUsageGraph.update_yaxes(range=[0, 3000])
    # Open CSV File with OOS NEs
    # Construct complete filepath with last file on the filePath var
    currentAlarmFile = neOosReportfilePath + os.listdir(neOosReportfilePath)[-1]
    alarmInformationList = []
    disconnectionCauseDataFrame = {'reason':[], 'reasonQty':[]}
    reasonDict = {'Port handshake':'Transmission', 'Connection torn down':'Transmission', 'ssl connections':'Transmission', 'Power supply':'Power', 'timed out':'Transmission'}
    disconnectionCauseDict = {'Port handshake':0, 'Connection torn down':0, 'ssl connections':0, 'Power supply':0, 'timed out':0}
    with open(currentAlarmFile) as csvfile:
            lineList = csv.reader(csvfile)
            for alarmRow in lineList:
                # Alarm Name field is located on the column 8 of the csv file
                if alarmRow[8] == 'NE Is Disconnected':
                    # Location information field is located on column 17 of the csv file
                    alarmInformationList.append(alarmRow[17])
            # Loop through alarm list
            for alarmRow in alarmInformationList:
                # Loop through dictionary keys
                for reason in reasonDict.keys():
                    # If the reason is found within the alarm list text
                    if reason in alarmRow:
                        disconnectionCauseDict[reason] += 1
    disconnectionCauseDataFrame['reason'] = [k for k in disconnectionCauseDict.keys()]
    disconnectionCauseDataFrame['reasonQty'] = [v for v in disconnectionCauseDict.values()]
    OOSdisconnectDf = pd.DataFrame(disconnectionCauseDataFrame, columns = ['reason', 'reasonQty'])
    oosNeGraph = px.bar(OOSdisconnectDf, x='reason', y='reasonQty', height=700)
    oosNeGraph.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF',
        title_font_size=54,
        font_size=30, 
        title='NE Out of Service'
    )
    # Close DB connection
    pointer.close()
    connectr.close()
    return bscGraphList[0], bscGraphList[1], bscGraphList[2], bscGraphList[3], bscGraphList[4], bscGraphList[5], rncGraphList[0], rncGraphList[1], rncGraphList[2], rncGraphList[3], rncGraphList[4], rncGraphList[5], rncGraphList[6], trxUsageGraph, oosNeGraph

@app.callback([
        Output('bscGraphFlexContainer', 'style'),  
        Output('rncGraphFlexContainer', 'style'), 
        Output('trxUsageGraph', 'style'),
        Output('oosNeGraph', 'style'),
        Output('dropDownContainer', 'style')
    ],  
    Input('graphUpateInterval', 'n_intervals'))
def hideGraph(currentInterval):
    if currentInterval%3 == 1:
        return {'display':'flex'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'flex'}
    elif currentInterval%3 == 2:
        return {'display':'none'}, {'display':'grid'}, {'display':'none'}, {'display':'none'}, {'display':'flex'}
    elif currentInterval%3 == 0:
        return {'display':'none'}, {'display':'none'}, {'display':'inline'}, {'display':'inline'}, {'display':'none'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5015')