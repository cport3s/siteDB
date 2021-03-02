import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
ranControllers = classes.ranControllers()
topWorstFilePath = "D:\\ftproot\\BSC\\top_worst_report\\"
# Styles
tabStyles = styles.headerStyles()
engDashboardStyles = styles.engDashboardTab()
graphSyles = styles.graphStyles()
dataTableStyles = styles.dataTableStyles()

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
        id = 'datatableGridContainer', 
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
                    html.H3('Top Worst HSDPA CSSR'),
                    dash_table.DataTable(
                        id = 'topWorst3GHsdpaCssrTable',
                        style_header = dataTableStyles.style_header,
                        style_cell = dataTableStyles.style_cell
                    )
                ]
            ),
            html.Div(
                className = 'datatableGridElement',
                children = [
                    html.H3('Top Worst HSUPA CSSR'),
                    dash_table.DataTable(
                        id='topWorst3GHsupaCssrTable',
                        style_header = dataTableStyles.style_header,
                        style_cell = dataTableStyles.style_cell
                    )
                ]
            ),
            html.Div(
                className = 'datatableGridElement',
                children = [
                    html.H3('Top Worst UMTS CSSR'),
                    dash_table.DataTable(
                        id='topWorst3GUmtsCssrTable',
                        style_header = dataTableStyles.style_header,
                        style_cell = dataTableStyles.style_cell
                    )
                ]
            ),
            html.Div(
                className = 'datatableGridElement',
                children = [
                    html.H3('Top Worst HSDPA DCR'),
                    dash_table.DataTable(
                        id='topWorst3GHsdpaDcrTable',
                        style_header = dataTableStyles.style_header,
                        style_cell = dataTableStyles.style_cell
                    )
                ]
            ),
            html.Div(
                className = 'datatableGridElement',
                children = [
                    html.H3('Top Worst HSUPA DCR'),
                    dash_table.DataTable(
                        id='topWorst3GHsupaDcrTable',
                        style_header = dataTableStyles.style_header,
                        style_cell = dataTableStyles.style_cell
                    )
                ]
            ),
            html.Div(
                className = 'datatableGridElement',
                children = [
                    html.H3('Top Worst UMTS DCR'),
                    dash_table.DataTable(
                        id='topWorst3GUmtsDcrTable',
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
    # Network Check Tab
    html.Div(
        id = 'networkCheckGridContainer',
        children = [ 
            html.Div(
                className = 'networkCheckGridElement',
                id = 'lteGeneralKPITable',
                children = [
                    html.H3('LTE General Network KPI'),
                    dash_table.DataTable(
                        id = 'ranReportLteTable',
                        style_header = {
                            'backgroundColor':'black',
                            'color':'white'
                            },
                        style_cell = {
                            'backgroundColor':'black',
                            'color':'white'
                        },
                        style_cell_conditional = [
                            {
                                'if':{'column_id':'KPI\\Object'},
                                'textAlign':'left'
                            }
                            ],
                        style_data_conditional = [
                            {
                                # LTE DCR style rule
                                'if':{'column_id':'Whole Network', 'row_index':0, 'filter_query':'{Whole Network} >= 0.13'},
                                'backgroundColor':'red'
                            },
                            {
                                # LTE RRC SSR style rule
                                'if':{'column_id':'Whole Network', 'row_index':1, 'filter_query':'{Whole Network} < 99'},
                                'backgroundColor':'red'
                            },
                            {
                                # LTE eRAB SSR style rule
                                'if':{'column_id':'Whole Network', 'row_index':2, 'filter_query':'{Whole Network} < 99'},
                                'backgroundColor':'red'
                            }
                        ]
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'umtsGeneralKPITable',
                children = [
                    html.H3('UMTS General Network KPI'), 
                    dash_table.DataTable(
                        id = 'ranReportUmtsTable',
                        style_header = {
                            'backgroundColor':'black',
                            'color':'white'
                            },
                        style_cell = {
                            'backgroundColor':'black',
                            'color':'white'
                        },
                        style_cell_conditional = [
                            {
                                'if':{'column_id':'KPI\\Object'},
                                'textAlign':'left'
                            }
                            ],
                        style_data_conditional = [
                            {
                                # UMTS DCR style rule
                                'if':{'column_id':'Whole Network', 'row_index':0, 'filter_query':'{Whole Network} >= 0.17'},
                                'backgroundColor':'red'
                            },
                            {
                                # UMTS CSSR style rule
                                'if':{'column_id':'Whole Network', 'row_index':1, 'filter_query':'{Whole Network} < 99.87'},
                                'backgroundColor':'red'
                            },
                            {
                                # HSDPA DCR style rule
                                'if':{'column_id':'Whole Network', 'row_index':6, 'filter_query':'{Whole Network} > 0.30'},
                                'backgroundColor':'red'
                            },
                            {
                                # HSUPA DCR style rule
                                'if':{'column_id':'Whole Network', 'row_index':7, 'filter_query':'{Whole Network} > 0.30'},
                                'backgroundColor':'red'
                            },
                            {
                                # HSDPA CSSR style rule
                                'if':{'column_id':'Whole Network', 'row_index':8, 'filter_query':'{Whole Network} < 99'},
                                'backgroundColor':'red'
                            },
                            {
                                # HSUPA CSSR style rule
                                'if':{'column_id':'Whole Network', 'row_index':9, 'filter_query':'{Whole Network} < 99'},
                                'backgroundColor':'red'
                            },
                        ]
                    )
                ]
            ), 
            html.Div(
                className = 'networkCheckGridElement',
                id = 'gsmGeneralKPITable',
                children = [
                    html.H3('GSM General Network KPI'),
                    dash_table.DataTable(
                        id = 'ranReportGsmTable',
                        style_header = {
                            'backgroundColor':'black',
                            'color':'white'
                            },
                        style_cell = {
                            'backgroundColor':'black',
                            'color':'white'
                        },
                        style_cell_conditional = [
                            {
                                'if':{'column_id':'KPI\\Object'},
                                'textAlign':'left'
                            }
                            ],
                        style_data_conditional = [
                            {
                                # GSM CS DCR style rule
                                'if':{'column_id':'Whole Network', 'row_index':0, 'filter_query':'{Whole Network} >= 0.3'},
                                'backgroundColor':'red'
                            },
                            {
                                # GSM CS CSSR style rule
                                'if':{'column_id':'Whole Network', 'row_index':1, 'filter_query':'{Whole Network} < 99.87'},
                                'backgroundColor':'red'
                            }
                        ]
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'cssrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'cssrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'volteCssrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'volteCssrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'dcrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'dcrNetworkWideGraph'
                    )
                ]
            ),
            html.Div(
                className = 'networkCheckGridElement',
                id = 'volteDcrNetworkWideGraphGridElement',
                children = [
                    dcc.Graph(
                        id = 'volteDcrNetworkWideGraph'
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
    # Graph Insight Tab (WIP)
    html.Div(
        id = 'graphInsightContainer',
        children = [
            html.Div(
                id = 'graphInsightDropdownContainer',
                style = {'display': 'flex', 'width':'100%'},
                children = [
                    dcc.Dropdown(
                        id = 'graphInsightRat',
                        style = {'width': '100%'},
                        options = [
                            {'label':'BSC', 'value':'BSC'},
                            {'label':'RNC', 'value':'RNC'}
                        ],
                        value = 'BSC'
                    ),
                    dcc.Dropdown(
                        id = 'graphInsightDataType',
                        style = {'width': '100%'},
                        options = [
                            {'label':'CS DCR', 'value':'CS DCR'},
                            {'label':'PS DCR', 'value':'PS DCR'},
                            {'label':'CS CSSR', 'value':'CS CSSR'},
                            {'label':'PS CSSR', 'value':'PS CSSR'}
                        ],
                        value = 'CS DCR'
                    )
                ]
            ),
            html.Div(
                id = 'graphInsightGraphContainer',
                children = [
                    dcc.Graph(
                        id = 'graphInsightgraph'
                    )
                ]
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
        bscHighRefresh = ran_functions.bscHighRefreshQuery(pointer, startTime, bscHighRefresh, ranControllers.bscNameList, gsmGraphValueConversionDict, dataTypeDropdown)
        # Set Graph background colores & title font size
        bscHighRefresh.update_layout(
            plot_bgcolor=graphSyles.plot_bgcolor, 
            paper_bgcolor=graphSyles.paper_bgcolor, 
            font_color=graphSyles.font_color, 
            title_font_size=graphTitleFontSize,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation='h')
        )
        rncHighRefresh = ran_functions.rncHighRefreshQuery(pointer, startTime, rncHighRefresh, ranControllers.rncNameList, umtsGraphValueConversionDict, dataTypeDropdown)
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
        for ne in ranControllers.bscNameList:
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
        return bscHighRefresh, rncHighRefresh, trxUsageGraph
    else:
        # Used in case there is no update needed on callback
        raise PreventUpdate

# Callback to update Top Worst Tab
@app.callback(
    [
        Output('topWorst4GeRabSrTable', 'columns'),
        Output('topWorst4GeRabSrTable', 'data'),
        Output('topWorst4GDcrTable', 'columns'),
        Output('topWorst4GDcrTable', 'data'),
        Output('topWorst3GHsdpaCssrTable', 'columns'),
        Output('topWorst3GHsdpaCssrTable', 'data'),
        Output('topWorst3GHsupaCssrTable', 'columns'),
        Output('topWorst3GHsupaCssrTable', 'data'),
        Output('topWorst3GUmtsCssrTable', 'columns'),
        Output('topWorst3GUmtsCssrTable', 'data'),
        Output('topWorst3GHsdpaDcrTable', 'columns'),
        Output('topWorst3GHsdpaDcrTable', 'data'),
        Output('topWorst3GHsupaDcrTable', 'columns'),
        Output('topWorst3GHsupaDcrTable', 'data'),
        Output('topWorst3GUmtsDcrTable', 'columns'),
        Output('topWorst3GUmtsDcrTable', 'data'),
        Output('topWorst2GSpeechCssrTable', 'columns'),
        Output('topWorst2GSpeechCssrTable', 'data'),
        Output('topWorst2GSpeechDcrTable', 'columns'),
        Output('topWorst2GSpeechDcrTable', 'data')
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
        for file in os.listdir(topWorstFilePath):
            if topWorstCurrentDate and "2G" and "CSSR" in file:
                current2GTopWorstCssrFile = file
            if topWorstCurrentDate and "2G" and "DCR" in file:
                current2GTopWorstDcrFile = file
            if topWorstCurrentDate and "3G" in file:
                current3GTopWorstFile = file
            if topWorstCurrentDate and "LTE" in file:
                current4GTopWorstFile = file

        current4GTopWorstDcrDataframe = pd.read_excel(topWorstFilePath + current4GTopWorstFile, sheet_name='TOP 50 Drop LTE', na_values='NIL')
        current4GTopWorsteRabSrDataframe = pd.read_excel(topWorstFilePath + current4GTopWorstFile, sheet_name='TOP 50 E-RAB Setup', na_values='NIL')
        current3GTopWorstDataframe = pd.read_excel(topWorstFilePath + current3GTopWorstFile, na_values=['NIL', '/0'])
        current2GTopWorstCssrDataframe = pd.read_excel(topWorstFilePath + current2GTopWorstCssrFile, na_values='NIL')
        current2GTopWorstDcrDataframe = pd.read_excel(topWorstFilePath + current2GTopWorstDcrFile, na_values='NIL')

        topWorst4GeRabSrDataframe = current4GTopWorsteRabSrDataframe.filter(items = ['eNodeB Name', 'Cell FDD TDD Indication', 'Cell Name', 'E-RAB Setup Success Rate (ALL)[%](%)', 'Date'])
        topWorst4GeRabSrDataframe = topWorst4GeRabSrDataframe.fillna(0)
        topWorst4GeRabSrDataframe = topWorst4GeRabSrDataframe.nsmallest(10, 'E-RAB Setup Success Rate (ALL)[%](%)')
        topWorst4GeRabSrColumns = [{'name': i, 'id': i} for i in topWorst4GeRabSrDataframe.columns]

        topWorst4GDcrDataframe = current4GTopWorstDcrDataframe.filter(items = ['eNodeB Name', 'Cell FDD TDD Indication', 'Cell Name', 'Call Drop Rate (All)[%]', 'Date'])
        topWorst4GDcrDataframe = topWorst4GDcrDataframe.fillna(0)
        topWorst4GDcrDataframe = topWorst4GDcrDataframe.nlargest(10, 'Call Drop Rate (All)[%]')
        topWorst4GDcrColumns = [{'name': i, 'id': i} for i in topWorst4GDcrDataframe.columns]

        topWorst3GHsdpaCssrDataframe = current3GTopWorstDataframe.filter(items = ['RNC Name', 'NodeB Name', 'Cell Name', 'HSDPA CSSR(%)', 'Date'])
        topWorst3GHsdpaCssrDataframe = topWorst3GHsdpaCssrDataframe.fillna(0)
        topWorst3GHsdpaCssrDataframe = topWorst3GHsdpaCssrDataframe.nsmallest(10, 'HSDPA CSSR(%)')
        topWorst3GHsdpaCssrColumns = [{'name': i, 'id': i} for i in topWorst3GHsdpaCssrDataframe.columns]

        topWorst3GHsupaCssrDataframe = current3GTopWorstDataframe.filter(items = ['RNC Name', 'NodeB Name', 'Cell Name', 'HSUPA CSSR(%)', 'Date'])
        topWorst3GHsupaCssrDataframe = topWorst3GHsupaCssrDataframe.fillna(0)
        topWorst3GHsupaCssrDataframe = topWorst3GHsupaCssrDataframe.nsmallest(10, 'HSUPA CSSR(%)')
        topWorst3GHsupaCssrColumns = [{'name': i, 'id': i} for i in topWorst3GHsupaCssrDataframe.columns]

        topWorst3GUmtsCssrDataframe = current3GTopWorstDataframe.filter(items = ['RNC Name', 'NodeB Name', 'Cell Name', 'Speech CSSR', 'Date'])
        topWorst3GUmtsCssrDataframe = topWorst3GUmtsCssrDataframe.fillna(0)
        topWorst3GUmtsCssrDataframe = topWorst3GUmtsCssrDataframe.nsmallest(10, 'Speech CSSR')
        topWorst3GUmtsCssrColumns = [{'name': i, 'id': i} for i in topWorst3GUmtsCssrDataframe.columns]

        topWorst3GHsdpaDcrDataframe = current3GTopWorstDataframe.filter(items = ['RNC Name', 'NodeB Name', 'Cell Name', 'HSDPA DCR(%)', 'Date'])
        topWorst3GHsdpaDcrDataframe = topWorst3GHsdpaDcrDataframe.fillna(0)
        topWorst3GHsdpaDcrDataframe = topWorst3GHsdpaDcrDataframe.nlargest(10, 'HSDPA DCR(%)')
        topWorst3GHsdpaDcrColumns = [{'name': i, 'id': i} for i in topWorst3GHsdpaDcrDataframe.columns]

        topWorst3GHsupaDcrDataframe = current3GTopWorstDataframe.filter(items = ['RNC Name', 'NodeB Name', 'Cell Name', 'HSUPA DCR(%)', 'Date'])
        topWorst3GHsupaDcrDataframe = topWorst3GHsupaDcrDataframe.fillna(0)
        topWorst3GHsupaDcrDataframe = topWorst3GHsupaDcrDataframe.nlargest(10, 'HSUPA DCR(%)')
        topWorst3GHsupaDcrColumns = [{'name': i, 'id': i} for i in topWorst3GHsupaDcrDataframe.columns]

        topWorst3GUmtsDcrDataframe = current3GTopWorstDataframe.filter(items=['RNC Name', 'NodeB Name', 'Cell Name', 'Speech DCR(%)', 'Date'])
        topWorst3GUmtsDcrDataframe = topWorst3GUmtsDcrDataframe.fillna(0)
        topWorst3GUmtsDcrDataframe = topWorst3GUmtsDcrDataframe.nlargest(10, 'Speech DCR(%)')
        topWorst3GUmtsDcrColumns = [{'name': i, 'id': i} for i in topWorst3GUmtsDcrDataframe.columns]

        topWorst2GSpeechCssrDataframe = current2GTopWorstCssrDataframe.filter(items = ['GBSC', 'Site Name', 'Cell Name', 'Call Setup Success Rate – Speech (%)', 'Date'])
        topWorst2GSpeechCssrDataframe = topWorst2GSpeechCssrDataframe.fillna(0)
        topWorst2GSpeechCssrDataframe = topWorst2GSpeechCssrDataframe.nsmallest(10, 'Call Setup Success Rate – Speech (%)')
        topWorst2GSpeechCssrColumns = [{'name': i, 'id': i} for i in topWorst2GSpeechCssrDataframe.columns]

        topWorst2GSpeechDcrDataframe = current2GTopWorstDcrDataframe.filter(items = ['GBSC', 'Site Name', 'Cell Name', 'Drop Call Rate – Speech (%)', 'Date'])
        topWorst2GSpeechDcrDataframe = topWorst2GSpeechDcrDataframe.fillna(0)
        topWorst2GSpeechDcrDataframe = topWorst2GSpeechDcrDataframe.nlargest(10, 'Drop Call Rate – Speech (%)')
        topWorst2GSpeechDcrColumns = [{'name': i, 'id': i} for i in topWorst2GSpeechDcrDataframe.columns]
        return topWorst4GeRabSrColumns, topWorst4GeRabSrDataframe.to_dict('records'), topWorst4GDcrColumns, topWorst4GDcrDataframe.to_dict('records'), topWorst3GHsdpaCssrColumns, topWorst3GHsdpaCssrDataframe.to_dict('records'), topWorst3GHsupaCssrColumns, topWorst3GHsupaCssrDataframe.to_dict('records'), topWorst3GUmtsCssrColumns, topWorst3GUmtsCssrDataframe.to_dict('records'), topWorst3GHsdpaDcrColumns, topWorst3GHsdpaDcrDataframe.to_dict('records'), topWorst3GHsupaDcrColumns, topWorst3GHsupaDcrDataframe.to_dict('records'), topWorst3GUmtsDcrColumns, topWorst3GUmtsDcrDataframe.to_dict('records'), topWorst2GSpeechCssrColumns, topWorst2GSpeechCssrDataframe.to_dict('records'), topWorst2GSpeechDcrColumns, topWorst2GSpeechDcrDataframe.to_dict('records')
    else:
        raise PreventUpdate

# Callback to hide/display selected tab
@app.callback(
    [
        Output('graphGridContainer', 'style'),
        Output('datatableGridContainer', 'style'), 
        Output('networkCheckGridContainer', 'style'),
        Output('graphInsightContainer', 'style')
    ], 
    Input('tabsContainer', 'value')
)
def showTabContent(currentTab):
    if currentTab == 'Engineering Dashboard':
        return {'display':'grid'}, {'display':'none'}, {'display':'none'}, {'display':'none'}
    elif currentTab == 'Top Worst Report':
        return {'display':'none'}, {'display':'grid'}, {'display':'none'}, {'display':'none'}
    elif currentTab == 'Network Check':
        return {'display':'none'}, {'display':'none'}, {'display':'grid'}, {'display':'none'}
    else:
        return {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'inline'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5016')
