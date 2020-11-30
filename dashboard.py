import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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

app = dash.Dash(__name__)
server = app.server

# DB Connection Parameters
dbusername = 'sitedb'
dbpassword = 'BSCAltice.123'
hostip = '172.16.121.41'
dbname = 'ran_pf_data'

loopCounter = 1
bscNameList = ['BSC_01_RRA', 'BSC_02_STGO', 'BSC_03_VM', 'BSC_04_VM', 'BSC_05_RRA', 'BSC_06_STGO']
rncNameList = ['RNC_01_RRA', 'RNC_02_STGO', 'RNC_03_VM', 'RNC_04_VM', 'RNC_05_RRA', 'RNC_06_STGO', 'RNC_07_VM']
neOosReportfilePath = "D:\\ftproot\\configuration_files\\NBI_FM\\" + datetime.now().strftime("%Y%m%d") + "\\"
graphTitleFontSize = 18

app.layout = html.Div(children=[
    html.Div(
        className = 'titleHeaderContainer',
        children = [
            html.H1(
                id = 'dashboardTitle',
                children = 'RAN Ops Dashboard'
            ),
            dcc.Tabs(
                id = 'tabsContainer',
                value = 'Engineering Dashboard',
                children = [
                    dcc.Tab(label = 'Engineering Dashboard', value = 'Engineering Dashboard'),
                    dcc.Tab(label = 'Top Worst Reports', value = 'Top Worst Reports')
                ]
            )
        ]
    ),
    html.Div(
        id = 'graphGridContainer',
        children = [
            html.Div(
                id = 'dataTypeDropdownGridElement',
                children = [
                    dcc.Dropdown(
                        id = 'dataTypeDropdown',
                        options = [
                            {'label':'CS Call Setup Success Rate', 'value':'CS Call Setup Success Rate'}, 
                            {'label':'PS Call Setup Success Rate', 'value':'PS Call Setup Success Rate'}, 
                            {'label':'CS Drop Call Rate', 'value':'CS Drop Call Rate'}, 
                            {'label':'PS Drop Call Rate', 'value':'PS Drop Call Rate'}, 
                            {'label':'Assignment Success Rate', 'value':'Assignment Success Rate'}, 
                            {'label':'Location Update Success Rate', 'value':'Location Update Success Rate'}
                        ],
                        value = 'CS Call Setup Success Rate',
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
                            {'label':'1 Day', 'value':'1'}, 
                            {'label':'3 Days', 'value':'3'}, 
                            {'label':'7 Days', 'value':'7'}, 
                            {'label':'30 Days', 'value':'30'}
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
            html.Div(
                className = 'gridElement',
                id = 'bscGraphContainer',
                children = [
                    'BSC Graph',
                    dcc.Graph(
                        id = 'bscGraph'
                    )
                ]
            ),
            html.Div(
                className = 'gridElement',
                id = 'oosNeGraphContainer',
                children = [
                    'NE OOS',
                    dcc.Graph(
                        id = 'oosNeGraph'
                    )
                ]
            ),
            html.Div(
                className = 'gridElement',
                id = 'rncGraphContainer',
                children = [
                    'RNC Graph',
                    dcc.Graph(
                        id = 'rncGraph'
                    )
                ]
            ),
            html.Div(
                className = 'gridElement',
                id = 'trxGraphContainer',
                children = [
                    'TRX Utilization',
                    dcc.Graph(
                        id = 'trxUsageGraph'
                    )
                ]
            ),
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
        Output('bscGraph', 'figure'), 
        Output('rncGraph', 'figure'), 
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
    daysDelta = int(timeFrameDropdown)
    # starttime is the current date/time - daysdelta
    startTime = (datetime.now() - timedelta(days=daysDelta)).strftime("%Y/%m/%d %H:%M:%S")
    # Connect to DB
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    # Instantiate the plots
    bscfig = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    rncfig = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    for bsc in bscNameList:
        pointer.execute('SELECT ' + gsmGraphValueConversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'' + bsc + '\' and lastupdate >= \'' + startTime + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        df = pd.DataFrame({dataTypeDropdown:queryPayload[:,0], 'Time':queryPayload[:,1]})
        # Add trace to the plot
        bscfig.add_trace(go.Scatter(x=df["Time"], y=df[dataTypeDropdown], name=bsc))
        queryRaw.clear()
    # Set Graph background colores & title font size
    bscfig.update_layout(
        plot_bgcolor='#2F2F2F', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=graphTitleFontSize
    )
    for rnc in rncNameList:
        pointer.execute('SELECT ' + umtsGraphValueConversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.rnc_performance_data where nename = \'' + rnc + '\' and lastupdate >= \'' + startTime + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        df = pd.DataFrame({ dataTypeDropdown:queryPayload[:,0], 'Time':queryPayload[:,1] })
        rncfig.add_trace(go.Scatter(x=df["Time"], y=df[dataTypeDropdown], name=rnc))
        queryRaw.clear()
    # Set Graph background colores & title font size
    rncfig.update_layout(
        plot_bgcolor='#2F2F2F', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=graphTitleFontSize
    )
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
    trxUsageGraph = px.bar(ipPoolReportDf, x='neName', y='trxQty', color='ipPoolId', barmode='group', template='simple_white')
    trxUsageGraph.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=graphTitleFontSize,
        font_size=graphTitleFontSize,
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
    oosNeGraph = px.pie(OOSdisconnectDf, names='reason', values='reasonQty')
    oosNeGraph.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF',
        title_font_size=graphTitleFontSize,
        font_size=graphTitleFontSize, 
        title='NE Out of Service'
    )
    oosNeGraph.update_traces(textinfo='value')
    # Close DB connection
    pointer.close()
    connectr.close()
    return bscfig, rncfig, trxUsageGraph, oosNeGraph

@app.callback(Output('graphGridContainer', 'style'), Input('tabsContainer', 'value'))
def showTabContent(currentTab):
    if currentTab == 'Engineering Dashboard':
        return {'display':'grid'}
    else:
        return {'display':'none'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5006')