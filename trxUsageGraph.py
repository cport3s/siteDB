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

# DB Connection Parameters
dbusername = 'sitedb'
dbpassword = 'BSCAltice.123'
hostip = '172.16.121.41'
dbname = 'ran_pf_data'

# NE OOS Report Filepath
filePath = "D:\\ftproot\\configuration_files\\NBI_FM\\" + datetime.now().strftime("%Y%m%d") + "\\"
graphTitleFontSize = 24
bscNameList = ['BSC_01_RRA', 'BSC_02_STGO', 'BSC_03_VM', 'BSC_04_VM', 'BSC_05_RRA', 'BSC_06_STGO']
rncNameList = ['RNC_01_RRA', 'RNC_02_STGO', 'RNC_03_VM', 'RNC_04_VM', 'RNC_05_RRA', 'RNC_06_STGO', 'RNC_07_VM']

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
                id='dataTypeDropdown',
                options=[
                    {'label':'TRX Interface Usage', 'value':'TRX Interface Usage'}, 
                    {'label':'NE OOS', 'value':'NE OOS'}
                    #{'label':'Top Worst Reports', 'value':'Top Worst Reports'}, 
                    #{'label':'BSC CS/PS Traffic', 'value':'BSC CS/PS Traffic'}, 
                    #{'label':'BSC Interface Traffic', 'value':'BSC Interface Traffic'},
                    #{'label':'RNC CS/PS Traffic', 'value':'RNC CS/PS Traffic'},
                    #{'label':'RNC Interface Traffic', 'value':'RNC Interface Traffic'},
                ],
                value='TRX Interface Usage',
                style={'width': '100%', 'font-size': str(graphTitleFontSize) + 'px'}
            )
        ]
    ),
    html.Div(
        className='trxGraphFlexContainer',
        children=[
            dcc.Graph(
                id='trxUsageGraph'
            )
        ]
    ),
    html.Div(
        className='topWorstFlexContainer',
        children=[
            html.Div(
                children='Top Worst Report'
            )
        ]
    ),
    dcc.Interval(
        id='dataUpateInterval',
        # Interval is in milliseconds unit 
        interval=3600000, 
        n_intervals=0
    ),
])

# We pass value from the time frame dropdown because it gets updated everytime you change the seleccion on the drop down.
@app.callback(Output('trxUsageGraph', 'figure'), 
        [
            # We use the update interval function and both dropdown menus as inputs for the callback
            Input('dataUpateInterval', 'n_intervals'), 
            Input('dataTypeDropdown', 'value')
        ])
def updateGraphData_bsc(currentInterval, dataTypeDropdown):
    gsmGraphValueConversionDict = {'BSC CS/PS Traffic':'gcstraffic', 'Drop Call Rate':'dcr'}
    umtsGraphValueConversionDict = {'RNC CS/PS Traffic':'ucstraffic', 'Drop Call Rate':'csdropcallrate'}
    # starttime is the current date/time - daysdelta
    # Connect to DB
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    # If selected value on dropdown is.....
    if dataTypeDropdown == 'TRX Interface Usage':
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
        trxUsageGraph = px.bar(ipPoolReportDf, x='neName', y='trxQty', color='ipPoolId', barmode='group')
        # Close DB connection
        pointer.close()
        connectr.close()
        return trxUsageGraph
    if dataTypeDropdown == 'NE OOS':
        # Open CSV File with OOS NEs
        # Construct complete filepath with last file on the filePath var
        currentAlarmFile = filePath + os.listdir(filePath)[-1]
        alarmInformationList = []
        disconnectionCauseDataFrame = {'reason':[], 'reasonQty':[]}
        reasonList = ['Port handshake', 'Connection torn down', 'ssl connections', 'Power supply', 'timed out']
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
                for reason in reasonList:
                    # If the reason is found within the alarm list text
                    if reason in alarmRow:
                        disconnectionCauseDataFrame['reason'].append(reason)
                        disconnectionCauseDataFrame['reasonQty'].append(1)
        OOSdisconnectDf = pd.DataFrame(disconnectionCauseDataFrame, columns = ['reason', 'reasonQty'])
        oosNeGraph = px.bar(OOSdisconnectDf, x='reason', y='reasonQty')
        # Close DB connection
        pointer.close()
        connectr.close()
        return oosNeGraph

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5010')