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

# DB Connection Parameters
dbusername = 'sitedb'
dbpassword = 'BSCAltice.123'
hostip = '172.16.121.41'
dbname = 'ran_pf_data'

# NE OOS Report Filepath
neOosReportfilePath = "D:\\ftproot\\configuration_files\\NBI_FM\\" + datetime.now().strftime("%Y%m%d") + "\\"
topWorstFilePath = "D:\\ftproot\\BSC\\top_worst_report\\"
graphTitleFontSize = 24
bscNameList = ['BSC_01_RRA', 'BSC_02_STGO', 'BSC_03_VM', 'BSC_04_VM', 'BSC_05_RRA', 'BSC_06_STGO']
rncNameList = ['RNC_01_RRA', 'RNC_02_STGO', 'RNC_03_VM', 'RNC_04_VM', 'RNC_05_RRA', 'RNC_06_STGO', 'RNC_07_VM']

current2GTopWorstDcrFile = ""
current2GTopWorstCssrFile = ""
current3GTopWorstFile = ""
current4GTopWorstFile = ""
topWorstCurrentDate = datetime.now().strftime("%Y%m%d")
for file in os.listdir(topWorstFilePath):
    if topWorstCurrentDate and "2G" and "CSSR" in file:
        current2GTopWorstCssrFile = file
    if topWorstCurrentDate and "2G" and "DCR" in file:
        current2GTopWorstDcrFile = file
    if topWorstCurrentDate and "3G" in file:
        current3GTopWorstFile = file
    if topWorstCurrentDate and "LTE" in file:
        current4GTopWorstFile = file

current3GTopWorstDataframe = pd.read_excel(topWorstFilePath + current3GTopWorstFile)
topWorst3GHsdpaCssrDataframe = current3GTopWorstDataframe.filter(items=['RNC Name', 'NodeB Name', 'Cell Name', 'HSDPA CSSR(%)', 'Date'])
topWorst3GHsdpaCssrDataframe = topWorst3GHsdpaCssrDataframe.nsmallest(10, 'HSDPA CSSR(%)')
topWorst3GHsdpaCssrColumns = [{'name': i, 'id': i} for i in topWorst3GHsdpaCssrDataframe.columns]

topWorst3GHsupaCssrDataframe = current3GTopWorstDataframe.filter(items=['RNC Name', 'NodeB Name', 'Cell Name', 'HSUPA CSSR(%)', 'Date'])
topWorst3GHsupaCssrDataframe = topWorst3GHsupaCssrDataframe.nsmallest(10, 'HSUPA CSSR(%)')
topWorst3GHsupaCssrColumns = [{'name': i, 'id': i} for i in topWorst3GHsupaCssrDataframe.columns]

topWorst3GUmtsCssrDataframe = current3GTopWorstDataframe.filter(items=['RNC Name', 'NodeB Name', 'Cell Name', 'Speech CSSR', 'Date'])
topWorst3GUmtsCssrDataframe = topWorst3GUmtsCssrDataframe.nsmallest(10, 'Speech CSSR')
topWorst3GUmtsCssrColumns = [{'name': i, 'id': i} for i in topWorst3GUmtsCssrDataframe.columns]

topWorst3GHsdpaDcrDataframe = current3GTopWorstDataframe.filter(items=['RNC Name', 'NodeB Name', 'Cell Name', 'HSDPA DCR(%)', 'Date'])
topWorst3GHsdpaDcrDataframe = topWorst3GHsdpaDcrDataframe.nlargest(10, 'HSDPA DCR(%)')
topWorst3GHsdpaDcrColumns = [{'name': i, 'id': i} for i in topWorst3GHsdpaDcrDataframe.columns]

topWorst3GHsupaDcrDataframe = current3GTopWorstDataframe.filter(items=['RNC Name', 'NodeB Name', 'Cell Name', 'HSUPA DCR(%)', 'Date'])
topWorst3GHsupaDcrDataframe = topWorst3GHsupaDcrDataframe.nlargest(10, 'HSUPA DCR(%)')
topWorst3GHsupaDcrColumns = [{'name': i, 'id': i} for i in topWorst3GHsupaDcrDataframe.columns]

#topWorst3GUmtsDcrDataframe = current3GTopWorstDataframe.filter(items=['RNC Name', 'NodeB Name', 'Cell Name', 'Speech DCR(%)', 'Date'])
#topWorst3GUmtsDcrDataframe = topWorst3GUmtsDcrDataframe.nlargest(10, 'Speech DCR(%)')
#topWorst3GUmtsDcrColumns = [{'name': i, 'id': i} for i in topWorst3GUmtsDcrDataframe.columns]

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
                    {'label':'NE OOS', 'value':'NE OOS'},
                    {'label':'Top Worst Reports', 'value':'Top Worst Reports'}
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
        style={'display':'flex', 'width':'100%', 'flex-direction':'column'},
        children=[
            dcc.Graph(
                id='trxUsageGraph'
            )
        ]
    ),
    html.Div(
        className='topWorstFlexContainer',
        style={'width':'100%'},
        children=[
            #'Top Worst HSDPA CSSR',
            dash_table.DataTable(
                id='topWorst3GHsdpaCssrTable',
                columns=topWorst3GHsdpaCssrColumns,
                data=topWorst3GHsdpaCssrDataframe.to_dict('records')
            ),
            #'Top Worst HSUPA CSSR',
            dash_table.DataTable(
                id='topWorst3GHsupaCssrTable',
                columns=topWorst3GHsupaCssrColumns,
                data=topWorst3GHsupaCssrDataframe.to_dict('records')
            ),
            #'Top Worst UMTS Speech CSSR',
            dash_table.DataTable(
                id='topWorst3GUmtsCssrTable',
                columns=topWorst3GUmtsCssrColumns,
                data=topWorst3GUmtsCssrDataframe.to_dict('records')
            ),
            #'Top Worst HSDPA DCR',
            dash_table.DataTable(
                id='topWorst3GHsdpaDcrTable',
                columns=topWorst3GHsdpaDcrColumns,
                data=topWorst3GHsdpaDcrDataframe.to_dict('records')
            ),
            #'Top Worst HSUPA DCR',
            dash_table.DataTable(
                id='topWorst3GHsupaDcrTable',
                columns=topWorst3GHsupaDcrColumns,
                data=topWorst3GHsupaDcrDataframe.to_dict('records')
            #),
            #'Top Worst UMTS Speech DCR',
            #dash_table.DataTable(
            #    id='topWorst3GUmtsDcrTable',
            #    columns=topWorst3GUmtsDcrColumns,
            #    data=topWorst3GUmtsDcrDataframe.to_dict('records')
            )
        ]
    ),
    dcc.Interval(
        id='dataUpateInterval',
        # Interval is in milliseconds unit 
        interval=3600000, 
        n_intervals=0
    )
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
        trxUsageGraph = px.bar(ipPoolReportDf, x='neName', y='trxQty', color='ipPoolId', barmode='group', template='simple_white')
        trxUsageGraph.update_layout(
            plot_bgcolor='#000000', 
            paper_bgcolor='#000000', 
            font_color='#FFFFFF', 
            title_font_size=54,
            title='TRX Load per Interface',
            font_size=36
        )
        # Set Y Axes Range
        trxUsageGraph.update_yaxes(range=[0, 3000])
        # Close DB connection
        pointer.close()
        connectr.close()
        return trxUsageGraph
    if dataTypeDropdown == 'NE OOS':
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
        oosNeGraph = px.bar(OOSdisconnectDf, x='reason', y='reasonQty')
        # Close DB connection
        pointer.close()
        connectr.close()
        return oosNeGraph

#@app.callback(Output('topWorstTable', 'columns'), Input('dataTypeDropdown', 'value'))
#def topWorstCalculator(dataTypeDropdown):
#    if dataTypeDropdown == 'Top Worst Reports':
#        current2GTopWorstDcrFile = ""
#        current2GTopWorstCssrFile = ""
#        current3GTopWorstFile = ""
#        current4GTopWorstFile = ""
#        topWorstCurrentDate = datetime.now().strftime("%Y%m%d")
#        for file in os.listdir(topWorstFilePath):
#            if topWorstCurrentDate and "2G" and "CSSR" in file:
#                current2GTopWorstCssrFile = file
#            if topWorstCurrentDate and "2G" and "DCR" in file:
#                current2GTopWorstDcrFile = file
#            if topWorstCurrentDate and "3G" in file:
#                current3GTopWorstFile = file
#            if topWorstCurrentDate and "LTE" in file:
#                current4GTopWorstFile = file
#        current3GTopWorstDataframe = pd.read_excel(topWorstFilePath + current3GTopWorstFile, index_col='Cell Name')
#        current3GTopWorstColumns = [{'name': i, 'id': i} for i in current3GTopWorstDataframe.columns]
#        return current3GTopWorstColumns


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5010')