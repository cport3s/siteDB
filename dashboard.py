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
graphTitleFontSize = 52

app.layout = html.Div(children=[
    html.H1(
        className = 'titleHeader',
        children = 'RAN Ops Dashboard'
    ),
    html.Div(
        id = 'graphGridContainer',
        children = [
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

## We pass value from the time frame dropdown because it gets updated everytime you change the seleccion on the drop down.
#@app.callback([
#        Output('bsc01Graph', 'figure'), 
#        Output('bsc02Graph', 'figure'), 
#        Output('bsc03Graph', 'figure'), 
#        Output('bsc04Graph', 'figure'), 
#        Output('bsc05Graph', 'figure'), 
#        Output('bsc06Graph', 'figure'),
#        Output('rnc01Graph', 'figure'), 
#        Output('rnc02Graph', 'figure'), 
#        Output('rnc03Graph', 'figure'), 
#        Output('rnc04Graph', 'figure'), 
#        Output('rnc05Graph', 'figure'), 
#        Output('rnc06Graph', 'figure'),
#        Output('rnc07Graph', 'figure'),
#        Output('trxUsageGraph', 'figure'),
#        Output('oosNeGraph', 'figure')
#    ], 
#    [
#        # We use the update interval function and both dropdown menus as inputs for the callback
#        Input('dataUpateInterval', 'n_intervals'), 
#        Input('timeFrameDropdown', 'value'), 
#        Input('dataTypeDropdown', 'value')
#    ])
#def updateGraphData_bsc(currentInterval, timeFrameDropdown, dataTypeDropdown):
#    gsmGraphValueConversionDict = {'Call Setup Success Rate':'cssr', 'Drop Call Rate':'dcr', 'Assignment Success Rate':'assignmentsuccessrate', 'Location Update Success Rate':'luupdatesr'}
#    umtsGraphValueConversionDict = {'Call Setup Success Rate':'csconnectionsuccessrate', 'Drop Call Rate':'csdropcallrate', 'Assignment Success Rate':'rrcconnectionsuccessrate', 'Location Update Success Rate':'pagingsuccessrate'}
#    bscGraphList = []
#    rncGraphList = []
#    daysDelta = int(timeFrameDropdown)
#    # starttime is the current date/time - daysdelta
#    startTime = (datetime.now() - timedelta(days=daysDelta)).strftime("%Y/%m/%d %H:%M:%S")
#    # Connect to DB
#    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
#    # Connection must be buffered when executing multiple querys on DB before closing connection.
#    pointer = connectr.cursor(buffered=True)
#    for bsc in bscNameList:
#        pointer.execute('SELECT ' + gsmGraphValueConversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'' + bsc + '\' and lastupdate >= \'' + startTime + '\';')
#        queryRaw = pointer.fetchall()
#        queryPayload = np.array(queryRaw)
#        # Transform the query payload into a dataframe
#        df = pd.DataFrame({ dataTypeDropdown:queryPayload[:,0], 'Time':queryPayload[:,1] })
#        fig = px.bar(df, x="Time", y=dataTypeDropdown, title=bsc)
#        # Set Graph background colores & title font size
#        fig.update_layout(
#            plot_bgcolor='#2F2F2F', 
#            paper_bgcolor='#000000', 
#            font_color='#FFFFFF', 
#            title_font_size=54
#        )
#        # Color the graph
#        fig.update_traces(marker_color='#17FF00')
#        # Append the current graph to the graph list
#        bscGraphList.append(fig)
#        queryRaw.clear()
#    for rnc in rncNameList:
#        pointer.execute('SELECT ' + umtsGraphValueConversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.rnc_performance_data where nename = \'' + rnc + '\' and lastupdate >= \'' + startTime + '\';')
#        queryRaw = pointer.fetchall()
#        queryPayload = np.array(queryRaw)
#        # Transform the query payload into a dataframe
#        df = pd.DataFrame({ dataTypeDropdown:queryPayload[:,0], 'Time':queryPayload[:,1] })
#        fig = px.bar(df, x="Time", y=dataTypeDropdown, title=rnc)
#        # Set Graph background colores & title font size
#        fig.update_layout(
#            plot_bgcolor='#2F2F2F', 
#            paper_bgcolor='#000000', 
#            font_color='#FFFFFF', 
#            title_font_size=54
#        )
#        # Color the graph
#        fig.update_traces(marker_color='#17FF00')
#        # Append the current graph to the graph list
#        rncGraphList.append(fig)
#        queryRaw.clear()
#    tempDataFrame = {'neName':[], 'ipPoolId':[], 'trxQty':[]}
#    # Loop through BSC Names
#    for ne in bscNameList:
#        # Loop through Ip Pool ID range (10 - 12)
#        for ippool in range(10,13):
#            tempDataFrame['neName'].append(ne)
#            # Must change ippool to string for the bar chart to display in group mode.
#            tempDataFrame['ipPoolId'].append(str(ippool))
#            pointer.execute('SELECT trxqty FROM ran_pf_data.trx_usage_data where lastupdate >= \'' + datetime.now().strftime("%Y/%m/%d") + '\' and nename = \'' + ne + '\' and ippoolid = ' + str(ippool) + ' order by lastupdate desc;')
#            queryPayload = pointer.fetchone()
#            # Must check if query result is empty, to full with 0
#            if queryPayload:
#                # Take the latest value on the DB
#                tempDataFrame['trxQty'].append(queryPayload[0])
#            else:
#                tempDataFrame['trxQty'].append(0)
#    ipPoolReportDf = pd.DataFrame(tempDataFrame, columns = ['neName', 'ipPoolId', 'trxQty'])
#    trxUsageGraph = px.bar(ipPoolReportDf, x='neName', y='trxQty', color='ipPoolId', barmode='group', template='simple_white', height=700)
#    trxUsageGraph.update_layout(
#        plot_bgcolor='#000000', 
#        paper_bgcolor='#000000', 
#        font_color='#FFFFFF', 
#        title_font_size=54,
#        font_size=30,
#        title='TRX Load per Interface'
#    )
#    # Set Y Axes Range
#    trxUsageGraph.update_yaxes(range=[0, 3000])
#    # Open CSV File with OOS NEs
#    # Construct complete filepath with last file on the filePath var
#    currentAlarmFile = neOosReportfilePath + os.listdir(neOosReportfilePath)[-1]
#    alarmInformationList = []
#    disconnectionCauseDataFrame = {'reason':[], 'reasonQty':[]}
#    reasonDict = {'Port handshake':'Transmission', 'Connection torn down':'Transmission', 'ssl connections':'Transmission', 'Power supply':'Power', 'timed out':'Transmission'}
#    disconnectionCauseDict = {'Port handshake':0, 'Connection torn down':0, 'ssl connections':0, 'Power supply':0, 'timed out':0}
#    with open(currentAlarmFile) as csvfile:
#            lineList = csv.reader(csvfile)
#            for alarmRow in lineList:
#                # Alarm Name field is located on the column 8 of the csv file
#                if alarmRow[8] == 'NE Is Disconnected':
#                    # Location information field is located on column 17 of the csv file
#                    alarmInformationList.append(alarmRow[17])
#            # Loop through alarm list
#            for alarmRow in alarmInformationList:
#                # Loop through dictionary keys
#                for reason in reasonDict.keys():
#                    # If the reason is found within the alarm list text
#                    if reason in alarmRow:
#                        disconnectionCauseDict[reason] += 1
#    disconnectionCauseDataFrame['reason'] = [k for k in disconnectionCauseDict.keys()]
#    disconnectionCauseDataFrame['reasonQty'] = [v for v in disconnectionCauseDict.values()]
#    OOSdisconnectDf = pd.DataFrame(disconnectionCauseDataFrame, columns = ['reason', 'reasonQty'])
#    oosNeGraph = px.bar(OOSdisconnectDf, x='reason', y='reasonQty', height=700)
#    oosNeGraph.update_layout(
#        plot_bgcolor='#000000', 
#        paper_bgcolor='#000000', 
#        font_color='#FFFFFF',
#        title_font_size=54,
#        font_size=30, 
#        title='NE Out of Service'
#    )
#    # Close DB connection
#    pointer.close()
#    connectr.close()
#    return bscGraphList[0], bscGraphList[1], bscGraphList[2], bscGraphList[3], bscGraphList[4], bscGraphList[5], rncGraphList[0], rncGraphList[1], rncGraphList[2], rncGraphList[3], rncGraphList[4], rncGraphList[5], rncGraphList[6], trxUsageGraph, oosNeGraph
#
#@app.callback([
#        Output('bscGraphFlexContainer', 'style'),  
#        Output('rncGraphFlexContainer', 'style'), 
#        Output('trxUsageGraph', 'style'),
#        Output('oosNeGraph', 'style'),
#        Output('dropDownContainer', 'style')
#    ],  
#    Input('graphUpateInterval', 'n_intervals'))
#def hideGraph(currentInterval):
#    if currentInterval%3 == 1:
#        return {'display':'flex'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'flex'}
#    elif currentInterval%3 == 2:
#        return {'display':'none'}, {'display':'grid'}, {'display':'none'}, {'display':'none'}, {'display':'flex'}
#    elif currentInterval%3 == 0:
#        return {'display':'none'}, {'display':'none'}, {'display':'inline'}, {'display':'inline'}, {'display':'none'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5006')