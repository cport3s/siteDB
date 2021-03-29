import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import mysql.connector
import numpy as np
import time
from datetime import datetime, timedelta
import os
import csv
import classes
import ranEngDashboardStyles as styles
import ran_functions

app = dash.Dash(__name__, title='RAN-Ops Engineering Dashboard')
server = app.server

# DB Connection Parameters
dbPara = classes.dbCredentials()
# Data
ranController = classes.ranControllers()
topWorstFilePath = "D:\\ftproot\\BSC\\top_worst_report\\"

# Styles
tabStyles = styles.headerStyles()
engDashboardStyles = styles.engDashboardTab()
graphSyles = styles.graphStyles()
dataTableStyles = styles.topWorstTab()
networkCheckStyles = styles.networkCheckTab()
graphColors = styles.NetworkWideGraphColors()
graphInsightStyles = styles.graphInsightTab()
txCheckStyles = styles.txCheckTab()

#rows = []
graphTitleFontSize = 18

app.layout = html.Div(children=[
    # Header & tabbed menu
    html.Div(
        style = tabStyles.headerFlexContainer,
        children = [
            html.H2(
                id = 'dashboardTitle',
                children = 'RAN-Ops Engineering Dashboard',
                style = tabStyles.dashboardTitle
            ),
            dcc.Tabs(
                id = 'tabsContainer',
                value = 'Engineering Dashboard',
                children = [
                    dcc.Tab(
                        label = 'Engineering Dashboard', 
                        value = 'Engineering Dashboard', 
                        style = tabStyles.tabStyle,
                        selected_style = tabStyles.tabSelectedStyle
                    ),
                    dcc.Tab(
                        label = 'Top Worst Report', 
                        value = 'Top Worst Report', 
                        style = tabStyles.tabStyle,
                        selected_style = tabStyles.tabSelectedStyle
                    ),
                    dcc.Tab(
                        label = 'Network Check', 
                        value = 'Network Check', 
                        style = tabStyles.tabStyle,
                        selected_style = tabStyles.tabSelectedStyle
                    ),
                    dcc.Tab(
                        label = 'Graph Insight', 
                        value = 'Graph Insight', 
                        style = tabStyles.tabStyle,
                        selected_style = tabStyles.tabSelectedStyle
                    ),
                    dcc.Tab(
                        label = 'Tx Status', 
                        value = 'Tx Status', 
                        style = tabStyles.tabStyle,
                        selected_style = tabStyles.tabSelectedStyle
                    )
                ]
            )
        ]
    ),
    # Engineering Dashboard Tab
    html.Div(
        id = 'graphGridContainer',
        style = engDashboardStyles.graphGridContainerStyle,
        children = [
            html.Div(
                id = 'dataTypeDropdownGridElement',
                style = engDashboardStyles.dataTypeDropdownGridElement,
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
                        value = 'PS Drop Call Rate',
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
                style = engDashboardStyles.timeFrameDropdownGridElement,
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
                style = engDashboardStyles.bscGraphContainer,
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
                style = engDashboardStyles.rncGraphContainer,
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
                style = engDashboardStyles.trxGraphContainer,
                children = [
                    'TRX Utilization',
                    dcc.Graph(
                        id = 'trxUsageGraph'
                    )
                ]
            ),
        ]
    ),
    # Top Worst Reports Tab
    html.Div(
        id = 'outerTopWorstReportFlexContainer',
        style = dataTableStyles.outerTopWorstReportFlexContainer,
        children = [
            # Inner Tab Container
            dcc.Tabs(
                id = 'innerTopWorstTabContainer',
                value = 'Daily Report',
                style = dataTableStyles.innerTopWorstTabContainer,
                children = [
                    dcc.Tab(
                        label = 'Daily Report',
                        value = 'Daily Report',
                        style = tabStyles.tabStyle,
                        selected_style = tabStyles.tabSelectedStyle
                    ),
                    dcc.Tab(
                        label = 'Records',
                        value = 'Records',
                        style = tabStyles.tabStyle,
                        selected_style = tabStyles.tabSelectedStyle
                    )
                ]
            ),
            # Daily Top Worst Reports
            html.Div(
                id = 'datatableGridContainer', 
                style = dataTableStyles.datatableGridContainer,
                children = [
                    html.Div(
                        className = 'datatableGridElement',
                        children = [
                            html.H3('Top Worst LTE eRAB SR'),
                            dash_table.DataTable(
                                id = 'topWorst4GeRabSrTable',
                                style_header = dataTableStyles.style_header,
                                style_cell = dataTableStyles.style_cell
                            )
                        ]
                    ),
                    html.Div(
                        className = 'datatableGridElement',
                        children = [
                            html.H3('Top Worst LTE DCR'),
                            dash_table.DataTable(
                                id='topWorst4GDcrTable',
                                style_header = dataTableStyles.style_header,
                                style_cell = dataTableStyles.style_cell
                            )
                        ]
                    ),
                    html.Div(
                        className = 'datatableGridElement',
                        children = [
                            html.H3('Top Worst 3G PS CSSR'),
                            dash_table.DataTable(
                                id = 'topWorst3GPsCssrTable',
                                style_header = dataTableStyles.style_header,
                                style_cell = dataTableStyles.style_cell
                            )
                        ]
                    ),
                    html.Div(
                        className = 'datatableGridElement',
                        children = [
                            html.H3('Top Worst 3G CS CSSR'),
                            dash_table.DataTable(
                                id='topWorst3GCsCssrTable',
                                style_header = dataTableStyles.style_header,
                                style_cell = dataTableStyles.style_cell
                            )
                        ]
                    ),
                    html.Div(
                        className = 'datatableGridElement',
                        children = [
                            html.H3('Top Worst 3G PS DCR'),
                            dash_table.DataTable(
                                id='topWorst3GPsDcrTable',
                                style_header = dataTableStyles.style_header,
                                style_cell = dataTableStyles.style_cell
                            )
                        ]
                    ),
                    html.Div(
                        className = 'datatableGridElement',
                        children = [
                            html.H3('Top Worst 3G CS DCR'),
                            dash_table.DataTable(
                                id='topWorst3GCsDcrTable',
                                style_header = dataTableStyles.style_header,
                                style_cell = dataTableStyles.style_cell
                            )
                        ]
                    ),
                    html.Div(
                        className = 'datatableGridElement',
                        children = [
                            html.H3('Top Worst GSM CSSR'),
                            dash_table.DataTable(
                                id='topWorst2GSpeechCssrTable',
                                style_header = dataTableStyles.style_header,
                                style_cell = dataTableStyles.style_cell
                            )
                        ]
                    ),
                    html.Div(
                        className = 'datatableGridElement',
                        children = [
                            html.H3('Top Worst GSM DCR'),
                            dash_table.DataTable(
                                id='topWorst2GSpeechDcrTable',
                                style_header = dataTableStyles.style_header,
                                style_cell = dataTableStyles.style_cell
                            )
                        ]
                    )
                ]
            ),
            # Top Reports Records
            html.Div(
                id = 'topReportRecordGridContainer',
                style = dataTableStyles.topWorstRecordGridContainer,
                children = [
                    html.Div(
                        children = [
                            html.H3('LTE eRAB SR Records'),
                            html.Button('Add Entry', id = 'topWorst4GeRabSrRercordTableClicks', n_clicks = 0),
                            dash_table.DataTable(
                                id = 'topWorst4GeRabSrRercordTable',
                                style_header = dataTableStyles.style_header,
                                columns = [{'name': '', 'id': ''}],
                                #data = [{'': ''}],
                                include_headers_on_copy_paste = True,
                                editable = True,
                                row_deletable = True
                            ),
                            html.Button('Submit', id = 'topWorst4GeRabSrRercordTableSubmit', n_clicks = 0),
                            html.H3('LTE DCR Records'),
                            html.Button('Add Entry', id = 'topWorst4GDcrRercordTableClicks', n_clicks = 0),
                            dash_table.DataTable(
                                id = 'topWorst4GDcrRercordTable',
                                style_header = dataTableStyles.style_header,
                                columns = [{'name': '', 'id': ''}],
                                #data = [{'': ''}],
                                include_headers_on_copy_paste = True,
                                editable = True,
                                row_deletable = True
                            ),
                            html.Button('Submit', id = 'topWorst4GDcrRercordTableSubmit', n_clicks = 0),
                            html.H3('3G PS CSSR Records'),
                            dash_table.DataTable(
                                id = 'topWorst3GPsCssrRecordTable',
                                style_header = dataTableStyles.style_header,
                                columns = [{'name': '', 'id': ''}],
                                data = [{'': ''}],
                                include_headers_on_copy_paste = True,
                                editable = True,
                                row_deletable = True
                            ),
                            html.H3('3G CS CSSR Records'),
                            dash_table.DataTable(
                                id = 'topWorst3GCsCssrRecordTable',
                                style_header = dataTableStyles.style_header,
                                columns = [{'name': '', 'id': ''}],
                                data = [{'': ''}],
                                include_headers_on_copy_paste = True,
                                editable = True,
                                row_deletable = True
                            ),
                            html.H3('3G PS DCR Records'),
                            dash_table.DataTable(
                                id = 'topWorst3GPsDcrRecordTable',
                                style_header = dataTableStyles.style_header,
                                columns = [{'name': '', 'id': ''}],
                                data = [{'': ''}],
                                include_headers_on_copy_paste = True,
                                editable = True,
                                row_deletable = True
                            ),
                            html.H3('3G CS DCR Records'),
                            dash_table.DataTable(
                                id = 'topWorst3GCsDcrRecordTable',
                                style_header = dataTableStyles.style_header,
                                columns = [{'name': '', 'id': ''}],
                                data = [{'': ''}],
                                include_headers_on_copy_paste = True,
                                editable = True,
                                row_deletable = True
                            ),
                            html.H3('GSM CSSR Records'),
                            dash_table.DataTable(
                                id = 'topWorst2GSpeechCssrRecordTable',
                                style_header = dataTableStyles.style_header,
                                columns = [{'name': '', 'id': ''}],
                                data = [{'': ''}],
                                include_headers_on_copy_paste = True,
                                editable = True,
                                row_deletable = True
                            ),
                            html.H3('GSM DCR Records'),
                            dash_table.DataTable(
                                id = 'topWorst2GSpeechDcrRecordTable',
                                style_header = dataTableStyles.style_header,
                                columns = [{'name': '', 'id': ''}],
                                data = [{'': ''}],
                                include_headers_on_copy_paste = True,
                                editable = True,
                                row_deletable = True
                            )
                        ]
                    )
                ]
            )
        ]
    ),
    # Network Check Tab
    html.Div(
        id = 'networkCheckGridContainer',
        style = networkCheckStyles.networkCheckGridContainer,
        children = [ 
            html.Div(
                className = 'networkCheckGridElement',
                id = 'cssrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'lteDataCssrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'volteCssrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'lteVolteCssrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'dcrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'lteDataDcrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'volteDcrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'lteVolteDcrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'hsdpaCssrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'hsdpaCssrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'hsupaCssrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'hsupaCssrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'umtsCssrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'umtsCssrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'hsdpaDcrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'hsdpaDcrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'hsupaDcrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'hsupaDcrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'umtsDcrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'umtsDcrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'gsmCsCssrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'gsmCsCssrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'gsmPsDcrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'gsmPsCssrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'gsmCsDcrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'gsmCsDcrNetworkWideGraph'
                    )
                ]
            )
        ]
    ),
    # Graph Insight Tab
    html.Div(
        id = 'graphInsightFlexContainer',
        style = graphInsightStyles.graphInsightFlexContainer,
        children = [
            html.Div(
                id = 'graphInsightDropdownContainer',
                style = graphInsightStyles.graphInsightDropdownContainer,
                children = [
                    dcc.Dropdown(
                        id = 'graphInsightRat',
                        style = graphInsightStyles.graphInsightRat,
                        options = [
                            {'label':'GSM', 'value':'GSM'},
                            {'label':'UMTS', 'value':'UMTS'},
                            {'label':'LTE', 'value':'LTE'}
                        ],
                        value = 'LTE'
                    ),
                    dcc.Dropdown(
                        id = 'graphInsightGraphType',
                        style = graphInsightStyles.graphInsightGraphType,
                        value = 'None'
                    )
                ]
            ),
            html.Div(
                id = 'graphInsightGraphContainer',
                style = graphInsightStyles.graphInsightGraphContainer,
                children = [
                    dcc.Graph(
                        id = 'graphInsightGraph'
                    )
                ]
            )
        ]
    ),
    # Tx Check Tab
    html.Div(
        id = 'txCheckGridContainer',
        style = txCheckStyles.txCheckGridContainer,
        children = [
            dcc.Graph(
                id = 'umtsNetworkPacketLossGraph'
            ),
            dcc.Graph(
                id = 'umtsNetworkDelayGraph'
            ),
            dcc.Graph(
                id = 'gsmNetworkPacketLossGraph'
            ),
            dcc.Graph(
                id = 'gsmNetworkDelayGraph'
            )
        ]
    ),
    dcc.Interval(
        id='dataUpateInterval', 
        interval=300000, 
        n_intervals=0
    )
])

# Callback to update Engineering Dashboard Tab
@app.callback(
    [
        Output('bscGraph', 'figure'), 
        Output('rncGraph', 'figure'), 
        Output('trxUsageGraph', 'figure')
    ], 
    [
        # We use the update interval function and both dropdown menus as inputs for the callback
        Input('dataUpateInterval', 'n_intervals'),
        Input('tabsContainer', 'value'),
        Input('timeFrameDropdown', 'value'), 
        Input('dataTypeDropdown', 'value')
    ]
)
def updateEngDashboardTab(currentInterval, selectedTab, timeFrameDropdown, dataTypeDropdown):
    # Connect to DB
    connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    if selectedTab == 'Engineering Dashboard':
        # Instantiate the plots
        bscHighRefresh = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
        rncHighRefresh = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
        gsmGraphValueConversionDict = {'CS Call Setup Success Rate':'cssr', 'PS Call Setup Success Rate':'edgedlssr', 'CS Drop Call Rate':'dcr', 'PS Drop Call Rate':'edgedldcr', 'Assignment Success Rate':'assignmentsuccessrate', 'Location Update Success Rate':'luupdatesr'}
        umtsGraphValueConversionDict = {'CS Call Setup Success Rate':'csconnectionsuccessrate', 'PS Call Setup Success Rate':'psrtsuccessrate', 'CS Drop Call Rate':'csdropcallrate', 'PS Drop Call Rate':'psdropcallrate', 'Assignment Success Rate':'rrcconnectionsuccessrate', 'Location Update Success Rate':'pagingsuccessrate'}
        daysDelta = int(timeFrameDropdown)
        # starttime is the current date/time - daysdelta
        startTime = (datetime.now() - timedelta(days=daysDelta)).strftime("%Y/%m/%d %H:%M:%S")
        bscHighRefresh = ran_functions.bscHighRefreshQuery(pointer, startTime, bscHighRefresh, ranController.bscNameList, gsmGraphValueConversionDict, dataTypeDropdown)
        # Set Graph background colores & title font size
        bscHighRefresh.update_layout(
            plot_bgcolor=graphSyles.plot_bgcolor, 
            paper_bgcolor=graphSyles.paper_bgcolor, 
            font_color=graphSyles.font_color, 
            title_font_size=graphTitleFontSize,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation='h')
        )
        rncHighRefresh = ran_functions.rncHighRefreshQuery(pointer, startTime, rncHighRefresh, ranController.rncNameList, umtsGraphValueConversionDict, dataTypeDropdown)
        # Set Graph background colores & title font size
        rncHighRefresh.update_layout(
            plot_bgcolor=graphSyles.plot_bgcolor, 
            paper_bgcolor=graphSyles.paper_bgcolor, 
            font_color=graphSyles.font_color,  
            title_font_size=graphTitleFontSize,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation='h')
        )
        # TRX Utilization Graph
        tempDataFrame = {'neName':[], 'ipPoolId':[], 'trxQty':[]}
        # Loop through BSC Names
        for ne in ranController.bscNameList:
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
        # Close DB Connection
        pointer.close()
        connectr.close()
        return bscHighRefresh, rncHighRefresh, trxUsageGraph
    else:
        # Close DB Connection
        pointer.close()
        connectr.close()
        # Used in case there is no update needed on callback
        raise PreventUpdate

# Callback to update Top Worst Tab
@app.callback(
    [
        Output('topWorst4GeRabSrTable', 'columns'),
        Output('topWorst4GeRabSrTable', 'data'),
        Output('topWorst4GeRabSrRercordTable', 'columns'),
        Output('topWorst4GDcrTable', 'columns'),
        Output('topWorst4GDcrTable', 'data'),
        Output('topWorst4GDcrRercordTable', 'columns'),
        Output('topWorst3GPsCssrTable', 'columns'),
        Output('topWorst3GPsCssrTable', 'data'),
        Output('topWorst3GPsCssrRecordTable', 'columns'),
        Output('topWorst3GCsCssrTable', 'columns'),
        Output('topWorst3GCsCssrTable', 'data'),
        Output('topWorst3GCsCssrRecordTable', 'columns'),
        Output('topWorst3GPsDcrTable', 'columns'),
        Output('topWorst3GPsDcrTable', 'data'),
        Output('topWorst3GPsDcrRecordTable', 'columns'),
        Output('topWorst3GCsDcrTable', 'columns'),
        Output('topWorst3GCsDcrTable', 'data'),
        Output('topWorst3GCsDcrRecordTable', 'columns'),
        Output('topWorst2GSpeechCssrTable', 'columns'),
        Output('topWorst2GSpeechCssrTable', 'data'),
        Output('topWorst2GSpeechCssrRecordTable', 'columns'),
        Output('topWorst2GSpeechDcrTable', 'columns'),
        Output('topWorst2GSpeechDcrTable', 'data'),
        Output('topWorst2GSpeechDcrRecordTable', 'columns')
    ], 
    Input('tabsContainer', 'value')
)
def updateTopWorstTab(selectedTab):
    # Ensure to refresh top worst tables only if that tab is selected
    if selectedTab == 'Top Worst Report':
        # Top Worst Reports Variables
        current2GTopWorstDcrFile = ""
        current2GTopWorstCssrFile = ""
        current3GTopWorstFile = ""
        current4GTopWorstFile = ""
        topWorstCurrentDate = str(datetime.now().strftime('%Y%m%d'))
        # find the latest file on the directory
        for file in os.listdir(topWorstFilePath):
            if topWorstCurrentDate and "2G" and "CSSR" in file:
                current2GTopWorstCssrFile = file
            if topWorstCurrentDate and "2G" and "DCR" in file:
                current2GTopWorstDcrFile = file
            if topWorstCurrentDate and "3G" in file:
                current3GTopWorstFile = file
            if topWorstCurrentDate and "LTE" in file:
                current4GTopWorstFile = file
        # Open the latest files as dataframes
        current4GTopWorstDcrDataframe = pd.read_excel(topWorstFilePath + current4GTopWorstFile, sheet_name='TOP 50 Drop LTE', na_values='NIL')
        current4GTopWorsteRabSrDataframe = pd.read_excel(topWorstFilePath + current4GTopWorstFile, sheet_name='TOP 50 E-RAB Setup', na_values='NIL')
        current3GTopWorstDataframe = pd.read_excel(topWorstFilePath + current3GTopWorstFile, na_values=['NIL', '/0'])
        current2GTopWorstCssrDataframe = pd.read_excel(topWorstFilePath + current2GTopWorstCssrFile, na_values='NIL')
        current2GTopWorstDcrDataframe = pd.read_excel(topWorstFilePath + current2GTopWorstDcrFile, na_values='NIL')
        # Filter the selected columns
        topWorst4GeRabSrDataframe = current4GTopWorsteRabSrDataframe.filter(items = ['eNodeB Name', 'Cell FDD TDD Indication', 'Cell Name', 'E-RAB Setup Success Rate (ALL)[%](%)', 'Date'])
        # Fill N/A values as 0
        topWorst4GeRabSrDataframe = topWorst4GeRabSrDataframe.fillna(0)
        # Select top 10 results
        topWorst4GeRabSrDataframe = topWorst4GeRabSrDataframe.nsmallest(10, 'E-RAB Setup Success Rate (ALL)[%](%)')
        # Shape as a column list of dictionaries (Dash requirement)
        topWorst4GeRabSrColumns = [{'name': i, 'id': i} for i in topWorst4GeRabSrDataframe.columns]
        # Get the same column list, for the Records Tab
        topWorst4GeRabSrRecordColumns = topWorst4GeRabSrColumns.copy()
        topWorst4GeRabSrRecordColumns.append({'name': 'TTK', 'id':'TTK'})
        topWorst4GeRabSrRecordColumns.append({'name': 'Responsable', 'id':'Responsable'})

        topWorst4GDcrDataframe = current4GTopWorstDcrDataframe.filter(items = ['eNodeB Name', 'Cell FDD TDD Indication', 'Cell Name', 'Call Drop Rate (All)[%]', 'Date'])
        topWorst4GDcrDataframe = topWorst4GDcrDataframe.fillna(0)
        topWorst4GDcrDataframe = topWorst4GDcrDataframe.nlargest(10, 'Call Drop Rate (All)[%]')
        topWorst4GDcrColumns = [{'name': i, 'id': i} for i in topWorst4GDcrDataframe.columns]
        topWorst4GDcrRecordColumns = topWorst4GDcrColumns.copy()
        topWorst4GDcrRecordColumns.append({'name': 'TTK', 'id':'TTK'})
        topWorst4GDcrRecordColumns.append({'name': 'Responsable', 'id':'Responsable'})

        topWorst3GCsCssrDataframe = current3GTopWorstDataframe.filter(items = ['RNC Name', 'NodeB Name', 'Cell Name', 'HSDPA CSSR(%)', 'HSUPA CSSR(%)', 'Speech CSSR', 'Date'])
        topWorst3GCsCssrDataframe = topWorst3GCsCssrDataframe.fillna(0)
        topWorst3GCsCssrDataframe = topWorst3GCsCssrDataframe.nsmallest(10, 'Speech CSSR')
        topWorst3GCsCssrColumns = [{'name': i, 'id': i} for i in topWorst3GCsCssrDataframe.columns]
        topWorst3GCsCssrRecordColumns = topWorst3GCsCssrColumns.copy()
        topWorst3GCsCssrRecordColumns.append({'name': 'TTK', 'id':'TTK'})
        topWorst3GCsCssrRecordColumns.append({'name': 'Responsable', 'id':'Responsable'})
        
        topWorst3GPsCssrDataframe = current3GTopWorstDataframe.filter(items = ['RNC Name', 'NodeB Name', 'Cell Name', 'HSDPA CSSR(%)', 'HSUPA CSSR(%)', 'Total Fails', 'Date'])
        topWorst3GPsCssrDataframe = topWorst3GPsCssrDataframe.fillna(0)
        topWorst3GPsCssrDataframe = topWorst3GPsCssrDataframe.nlargest(10, 'Total Fails')
        topWorst3GPsCssrColumns = [{'name': i, 'id': i} for i in topWorst3GPsCssrDataframe.columns]
        topWorst3GPsCssrRecordColumns = topWorst3GPsCssrColumns.copy()
        topWorst3GPsCssrRecordColumns.append({'name': 'TTK', 'id':'TTK'})
        topWorst3GPsCssrRecordColumns.append({'name': 'Responsable', 'id':'Responsable'})
        
        topWorst3GCsDcrDataframe = current3GTopWorstDataframe.filter(items=['RNC Name', 'NodeB Name', 'Cell Name', 'Speech DCR(%)', 'HSDPA DCR(%)', 'HSUPA DCR(%)', 'Drops CS', 'Date'])
        topWorst3GCsDcrDataframe = topWorst3GCsDcrDataframe.fillna(0)
        topWorst3GCsDcrDataframe = topWorst3GCsDcrDataframe.nlargest(10, 'Drops CS')
        topWorst3GCsDcrColumns = [{'name': i, 'id': i} for i in topWorst3GCsDcrDataframe.columns]
        topWorst3GCsDcrRecordColumns = topWorst3GCsDcrColumns.copy()
        topWorst3GCsDcrRecordColumns.append({'name': 'TTK', 'id':'TTK'})
        topWorst3GCsDcrRecordColumns.append({'name': 'Responsable', 'id':'Responsable'})
        
        topWorst3GPsDcrDataframe = current3GTopWorstDataframe.filter(items=['RNC Name', 'NodeB Name', 'Cell Name', 'Speech DCR(%)', 'HSDPA DCR(%)', 'HSUPA DCR(%)', 'Drops PS', 'Date'])
        topWorst3GPsDcrDataframe = topWorst3GPsDcrDataframe.fillna(0)
        topWorst3GPsDcrDataframe = topWorst3GPsDcrDataframe.nlargest(10, 'Drops PS')
        topWorst3GPsDcrColumns = [{'name': i, 'id': i} for i in topWorst3GPsDcrDataframe.columns]
        topWorst3GPsDcrRecordColumns = topWorst3GPsDcrColumns.copy()
        topWorst3GPsDcrRecordColumns.append({'name': 'TTK', 'id':'TTK'})
        topWorst3GPsDcrRecordColumns.append({'name': 'Responsable', 'id':'Responsable'})
        
        topWorst2GSpeechCssrDataframe = current2GTopWorstCssrDataframe.filter(items = ['GBSC', 'Site Name', 'Cell Name', 'Call Setup Success Rate – Speech (%)', 'Date'])
        topWorst2GSpeechCssrDataframe = topWorst2GSpeechCssrDataframe.fillna(0)
        topWorst2GSpeechCssrDataframe = topWorst2GSpeechCssrDataframe.nsmallest(10, 'Call Setup Success Rate – Speech (%)')
        topWorst2GSpeechCssrColumns = [{'name': i, 'id': i} for i in topWorst2GSpeechCssrDataframe.columns]
        topWorst2GSpeechCssrRecordColumns = topWorst2GSpeechCssrColumns.copy()
        topWorst2GSpeechCssrRecordColumns.append({'name': 'TTK', 'id':'TTK'})
        topWorst2GSpeechCssrRecordColumns.append({'name': 'Responsable', 'id':'Responsable'})
        
        topWorst2GSpeechDcrDataframe = current2GTopWorstDcrDataframe.filter(items = ['GBSC', 'Site Name', 'Cell Name', 'Drop Call Rate – Speech (%)', 'Total Number of dropped Connections', 'Date'])
        topWorst2GSpeechDcrDataframe = topWorst2GSpeechDcrDataframe.fillna(0)
        topWorst2GSpeechDcrDataframe = topWorst2GSpeechDcrDataframe.nlargest(10, 'Total Number of dropped Connections')
        topWorst2GSpeechDcrColumns = [{'name': i, 'id': i} for i in topWorst2GSpeechDcrDataframe.columns]
        topWorst2GSpeechDcrRecordColumns = topWorst2GSpeechDcrColumns.copy()
        topWorst2GSpeechDcrRecordColumns.append({'name': 'TTK', 'id':'TTK'})
        topWorst2GSpeechDcrRecordColumns.append({'name': 'Responsable', 'id':'Responsable'})
        return topWorst4GeRabSrColumns, topWorst4GeRabSrDataframe.to_dict('records'), topWorst4GeRabSrRecordColumns, topWorst4GDcrColumns, topWorst4GDcrDataframe.to_dict('records'), topWorst4GDcrRecordColumns, topWorst3GPsCssrColumns, topWorst3GPsCssrDataframe.to_dict('records'), topWorst3GPsCssrRecordColumns, topWorst3GCsCssrColumns, topWorst3GCsCssrDataframe.to_dict('records'), topWorst3GCsCssrRecordColumns, topWorst3GPsDcrColumns, topWorst3GPsDcrDataframe.to_dict('records'), topWorst3GPsDcrRecordColumns, topWorst3GCsDcrColumns, topWorst3GCsDcrDataframe.to_dict('records'), topWorst3GCsDcrRecordColumns, topWorst2GSpeechCssrColumns, topWorst2GSpeechCssrDataframe.to_dict('records'), topWorst2GSpeechCssrRecordColumns, topWorst2GSpeechDcrColumns, topWorst2GSpeechDcrDataframe.to_dict('records'), topWorst2GSpeechDcrRecordColumns
    else:
        raise PreventUpdate

# Callback to add rows on Top Worst Records Tab. This tab's datatable data param must be updated on this callback to avoid callback output duplication.
@app.callback(
    [
        Output('topWorst4GeRabSrRercordTable', 'data'), 
        Output('topWorst4GDcrRercordTable', 'data')
    ],
    [
        Input('topWorst4GeRabSrRercordTableClicks', 'n_clicks'),
        Input('topWorst4GDcrRercordTableClicks', 'n_clicks'),
        Input('innerTopWorstTabContainer', 'value')
    ],
    State('topWorst4GeRabSrRercordTable', 'data_previous'),
    #State('topWorst4GeRabSrRercordTable', 'data'),
    State('topWorst4GeRabSrRercordTable', 'columns'),
    #State('topWorst4GDcrRercordTable', 'data'),
    State('topWorst4GDcrRercordTable', 'columns')
)
def addRow(topWorst4GeRabSrRercordTableClicks, topWorst4GDcrRercordTableClicks, selectedInnerTab, topWorst4GeRabSrRercordTableState, topWorst4GeRabSrRercordTableColumns, topWorst4GDcrRercordTableColumns):
    if selectedInnerTab == 'Records':
        # Instantiate the callback context, to find the button ID that triggered the callback
        callbackContext = dash.callback_context
        # Get button ID
        button_id = callbackContext.triggered[0]['prop_id'].split('.')[0]
        # Connect to DB
        connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.recordsDataTable)
        # Connection must be buffered when executing multiple querys on DB before closing connection.
        pointer = connectr.cursor(buffered=True)
        table = 'topworst4gerabsrrercord'
        # Fill datatable data with db table content
        topWorst4GeRabSrRercordTableData = ran_functions.queryTopRecords(pointer, topWorst4GeRabSrRercordTableColumns, table)
        table = 'topworst4gdcrrercord'
        topWorst4GDcrRercordTableData = ran_functions.queryTopRecords(pointer, topWorst4GDcrRercordTableColumns, table)
        if button_id == 'topWorst4GeRabSrRercordTableClicks':            
            topWorst4GeRabSrRercordTableData.append({column['id']: '' for column in topWorst4GeRabSrRercordTableColumns})
        if button_id == 'topWorst4GDcrRercordTableClicks':
            topWorst4GDcrRercordTableData.append({column['id']: '' for column in topWorst4GDcrRercordTableColumns})
        # Close DB Connection
        pointer.close()
        connectr.close()
        return topWorst4GeRabSrRercordTableData, topWorst4GDcrRercordTableData
    else:
        raise PreventUpdate

# Callback to update Network Check Tab
@app.callback(
    [
        Output('gsmCsCssrNetworkWideGraph', 'figure'),  
        Output('gsmPsCssrNetworkWideGraph', 'figure'), 
        Output('gsmCsDcrNetworkWideGraph', 'figure'),
        Output('umtsCssrNetworkWideGraph', 'figure'),
        Output('hsdpaCssrNetworkWideGraph', 'figure'),
        Output('hsupaCssrNetworkWideGraph', 'figure'),
        Output('umtsDcrNetworkWideGraph', 'figure'),
        Output('hsdpaDcrNetworkWideGraph', 'figure'),
        Output('hsupaDcrNetworkWideGraph', 'figure'),
        Output('lteVolteDcrNetworkWideGraph', 'figure'),
        Output('lteDataDcrNetworkWideGraph', 'figure'),
        Output('lteVolteCssrNetworkWideGraph', 'figure'),
        Output('lteDataCssrNetworkWideGraph', 'figure')
    ],
    [
        Input('tabsContainer', 'value'),
        Input('dataUpateInterval', 'n_intervals')
    ]
)
def updateNetworkCheckTab(selectedTab, currentInterval):
    if selectedTab == 'Network Check': 
        # starttime is the current date/time - daysdelta
        startTime = 7
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
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='LTE Data eRAB SSR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        lteVolteCssr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color,  
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='VoLTE eRAB SSR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        lteDataDcr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='LTE Data DCR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        lteVolteDcr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='VoLTE DCR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        umtsCssr, hsdpaCssr, hsupaCssr, umtsDcr, hsdpaDcr, hsupaDcr = ran_functions.populateUmtsGraphs(pointer, startTime, ranController.rncNameList, umtsCssr, hsdpaCssr, hsupaCssr, umtsDcr, hsdpaDcr, hsupaDcr)
        hsdpaCssr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='HSDPA CSSR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        hsupaCssr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='HSUPA CSSR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        umtsCssr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='UMTS CSSR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        hsdpaDcr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='HSDPA DCR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        hsupaDcr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='HSUPA DCR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        umtsDcr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='UMTS DCR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        gsmCsCssr, gsmPsCssr, gsmCsDcr = ran_functions.populateGsmGraphs(pointer, startTime, ranController.bscNameList, gsmCsCssr, gsmPsCssr, gsmCsDcr)
        gsmCsCssr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='GSM CS CSSR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        gsmPsCssr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='GSM PS CSSR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        gsmCsDcr.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='GSM CS DCR'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        # Close DB connection
        pointer.close()
        connectr.close()
        return gsmCsCssr, gsmPsCssr, gsmCsDcr, umtsCssr, hsdpaCssr, hsupaCssr, umtsDcr, hsdpaDcr, hsupaDcr, lteVolteDcr, lteDataDcr, lteVolteCssr, lteDataCssr
    else:
        raise PreventUpdate

#Callback to update Graph Insight Dropdown
@app.callback(
    Output('graphInsightGraphType', 'options'),
    Input('graphInsightRat', 'value')
)
def updateGraphInsightDropdown(selectedRAT):
    returnList = ['None']
    if selectedRAT == 'LTE':
        returnList = [{'label':'LTE Data DCR', 'value':'LTE Data DCR'}, {'label':'LTE Data CSSR', 'value':'LTE Data CSSR'}, {'label':'VoLTE DCR', 'value':'VoLTE DCR'}, {'label':'VoLTE CSSR', 'value':'VoLTE CSSR'}]
    elif selectedRAT == 'UMTS':
        returnList = [{'label':'UMTS DCR', 'value':'UMTS DCR'}, {'label':'UMTS CSSR', 'value':'UMTS CSSR'}, {'label':'HSDPA DCR', 'value':'HSDPA DCR'}, {'label':'HSDPA CSSR', 'value':'HSDPA CSSR'}, {'label':'HSUPA DCR', 'value':'HSUPA DCR'}, {'label':'HSUPA CSSR', 'value':'HSUPA CSSR'}]
    else:
        returnList = [{'label':'GSM CS CSSR', 'value':'GSM CS CSSR'}, {'label':'GSM PS CSSR', 'value':'GSM PS CSSR'}, {'label':'GSM CS DCR', 'value':'GSM CS DCR'}]
    return returnList

# Callback to update Graph Inisight Graph
@app.callback(
    Output('graphInsightGraph', 'figure'),
    Input('graphInsightGraphType', 'value')
)
def updateGraphInsightGraph(selectedKPI):
    startTime = 7
    # Connect to DB
    connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    currentGraph = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
    currentGraph = ran_functions.graphInsightQuery(currentGraph, startTime, selectedKPI, pointer)
    currentGraph.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        margin=dict(l=10, r=10, t=90, b=10),
        legend=dict(orientation='h'),
        title=dict(text=selectedKPI),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    return currentGraph

# Callback to update Network Check Tab
@app.callback(
    [
        Output('umtsNetworkPacketLossGraph', 'figure'),  
        Output('umtsNetworkDelayGraph', 'figure'), 
        Output('gsmNetworkPacketLossGraph', 'figure'), 
        Output('gsmNetworkDelayGraph', 'figure')
    ],
    [
        Input('tabsContainer', 'value'),
        Input('dataUpateInterval', 'n_intervals')
    ]
)
def updateTxCheckTab(selectedTab, currentInterval):
    if selectedTab == 'Tx Status': 
        # starttime is the current date/time - daysdelta
        startTime = 7
        # Connect to DB
        connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
        # Connection must be buffered when executing multiple querys on DB before closing connection.
        pointer = connectr.cursor(buffered=True)
        # Create plots
        umtsNetworkPacketLossGraph = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
        umtsNetworkDelayGraph = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
        gsmNetworkPacketLossGraph = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
        gsmNetworkDelayGraph = make_subplots(rows = 1, cols = 1, shared_xaxes = True, shared_yaxes = True)
        umtsNetworkPacketLossGraph, umtsNetworkDelayGraph, gsmNetworkPacketLossGraph, gsmNetworkDelayGraph = ran_functions.queryTxData(pointer, startTime, ranController.bscNameList, ranController.rncNameList, umtsNetworkPacketLossGraph, umtsNetworkDelayGraph, gsmNetworkPacketLossGraph, gsmNetworkDelayGraph)
        umtsNetworkPacketLossGraph.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='UMTS Network Packet Loss'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        umtsNetworkDelayGraph.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='UMTS Network Delay'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        gsmNetworkPacketLossGraph.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='GSM Network Packet Loss'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        gsmNetworkDelayGraph.update_layout(
            plot_bgcolor=graphColors.plot_bgcolor, 
            paper_bgcolor=graphColors.paper_bgcolor, 
            font_color=graphColors.font_color, 
            margin=dict(l=10, r=10, t=90, b=10),
            #legend=dict(orientation='h'),
            title=dict(text='GSM Network Delay'),
            title_font=dict(size=graphColors.graphTitleFontSize),
            legend_font_size=graphColors.legend_font_size
        )
        # Close DB connection
        pointer.close()
        connectr.close()
        return umtsNetworkPacketLossGraph, umtsNetworkDelayGraph, gsmNetworkPacketLossGraph, gsmNetworkDelayGraph
    else:
        raise PreventUpdate

# Callback to hide/display selected tab
@app.callback(
    [
        Output('graphGridContainer', 'style'),
        Output('outerTopWorstReportFlexContainer', 'style'),
        Output('networkCheckGridContainer', 'style'),
        Output('graphInsightFlexContainer', 'style'),
        Output('txCheckGridContainer', 'style')
    ], 
    Input('tabsContainer', 'value')
)
def showTabContent(currentTab):
    engDashboard = engDashboardStyles.graphGridContainerStyle
    topWorst = dataTableStyles.outerTopWorstReportFlexContainer
    networkCheck = networkCheckStyles.networkCheckGridContainer
    graphInsight = graphInsightStyles.graphInsightFlexContainer
    txCheck = txCheckStyles.txCheckGridContainer
    if currentTab == 'Engineering Dashboard':
        engDashboard['display'] = 'grid'
        topWorst['display'] = 'none'
        networkCheck['display'] = 'none'
        graphInsight['display'] = 'none'
        txCheck['display'] = 'none'
        return engDashboard, topWorst, networkCheck, graphInsight, txCheck
    elif currentTab == 'Top Worst Report':
        engDashboard['display'] = 'none'
        topWorst['display'] = 'flex'
        networkCheck['display'] = 'none'
        graphInsight['display'] = 'none'
        txCheck['display'] = 'none'
        return engDashboard, topWorst, networkCheck, graphInsight, txCheck
    elif currentTab == 'Network Check':
        engDashboard['display'] = 'none'
        topWorst['display'] = 'none'
        networkCheck['display'] = 'grid'
        graphInsight['display'] = 'none'
        txCheck['display'] = 'none'
        return engDashboard, topWorst, networkCheck, graphInsight, txCheck
    elif currentTab == 'Graph Insight':
        engDashboard['display'] = 'none'
        topWorst['display'] = 'none'
        networkCheck['display'] = 'none'
        graphInsight['display'] = 'flex'
        txCheck['display'] = 'none'
        return engDashboard, topWorst, networkCheck, graphInsight, txCheck
    else:
        engDashboard['display'] = 'none'
        topWorst['display'] = 'none'
        networkCheck['display'] = 'none'
        graphInsight['display'] = 'none'
        txCheck['display'] = 'grid'
        return engDashboard, topWorst, networkCheck, graphInsight, txCheck

# Callback to hide/display Top Worst inner tabs
@app.callback(
    [
        Output('datatableGridContainer', 'style'),
        Output('topReportRecordGridContainer', 'style')
    ], 
    Input('innerTopWorstTabContainer', 'value')
)
def showTopWorstInnerTabContent(currentTab):
    topWorstDaily = dataTableStyles.datatableGridContainer
    topWorstRecord = dataTableStyles.topWorstRecordGridContainer
    if currentTab == 'Daily Report':
        topWorstDaily['display'] = 'grid'
        topWorstRecord['display'] = 'none'
        return topWorstDaily, topWorstRecord
    else:
        topWorstDaily['display'] = 'none'
        topWorstRecord['display'] = 'grid'
        return topWorstDaily, topWorstRecord

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5016')

