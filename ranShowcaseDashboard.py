import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
from plotly.subplots import make_subplots
import pandas as pd
# Round to 2 decimal places in dataframe
pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.precision', 2)
import mysql.connector
from datetime import datetime, timedelta
from dash.exceptions import PreventUpdate
# Custom libraries
import classes
import ranShowcaseDashboardStyles as styles
import ran_functions

app = dash.Dash(__name__, title='RAN-Ops Dashboard')
server = app.server

dataTableObjectColumnWidth = '400px'
dataTableRatColumnWidth = '50px'
dataTableThresholdColumnWidth = '130px'
dataTableLatestHourColumnWidth = '180px'

# DB Connection Parameters
dbPara = classes.dbCredentials()
# FTP Connection Parameters
ftpLogin = classes.ranFtpCredentials()
ranController = classes.ranControllers()
graphColors = styles.NetworkWideGraphColors()
# Instantiate styles class
gridContainerStyles = styles.gridContainer()
gridelementStyles = styles.gridElement()
dataTableStyles = styles.datatableHeaderStyle()
# RAN Report Variables
currentKPIGridFilePath = "/BSC/current_kpi_per_hour/"
weeklyKPIGridFilePath = "/BSC/current_kpi_per_week/"

ranReportLteColumns = [{'name':'RAT', 'id':'RAT'}, {'name':'KPI\\Object', 'id':'KPI\\Object'}, {'name':'Threshold', 'id':'Threshold'}, {'name':'Latest Hour', 'id':'Latest Hour'}]
ranReportLteTable = pd.DataFrame(data={'RAT':[], 'KPI\\Object':[], 'Threshold':[], 'Latest Hour':[]})
ranReportUmtsColumns = [{'name':'RAT', 'id':'RAT'}, {'name':'KPI\\Object', 'id':'KPI\\Object'}, {'name':'Threshold', 'id':'Threshold'}, {'name':'Latest Hour', 'id':'Latest Hour'}]
ranReportUmtsTable = pd.DataFrame(data={'RAT':[], 'KPI\\Object':[], 'Threshold':[], 'Latest Hour':[]})
ranReportGsmColumns = [{'name':'RAT', 'id':'RAT'}, {'name':'KPI\\Object', 'id':'KPI\\Object'}, {'name':'Threshold', 'id':'Threshold'}, {'name':'Latest Hour', 'id':'Latest Hour'}]
ranReportGsmTable = pd.DataFrame(data={'RAT':[], 'KPI\\Object':[], 'Threshold':[], 'Latest Hour':[]})

app.layout = html.Div(
    children=[
        html.H1(
        className='showCasetitleHeader',
        children='RAN Ops Dashboard', 
        style={
            'text-align': 'center',
            'color':'white'
            }
        ),
        # Current KPI View
        html.Div(
            id='currentKPIGridContainer',
            style = gridContainerStyles.currentKPIGridContainer,
            children = [
                html.Div(
                    id = 'lteGeneralKPITable',
                    style=gridelementStyles.lteGeneralKPITableStyle,
                    children = [
                        dash_table.DataTable(
                            id = 'ranReportLteTable',
                            style_header = dataTableStyles.style_header,
                            style_cell = dataTableStyles.style_cell,
                            #style_cell_conditional = [
                            #    {
                            #        'if':{'column_id':'KPI\\Object'},
                            #        'textAlign':'left',
                            #        'minWidth': dataTableObjectColumnWidth,
                            #        'width': dataTableObjectColumnWidth,
                            #        'maxWidth': dataTableObjectColumnWidth
                            #    },
                            #    {
                            #        'if':{'column_id':'RAT'},
                            #        'textAlign':'center',
                            #        'minWidth': dataTableRatColumnWidth,
                            #        'width': dataTableRatColumnWidth,
                            #        'maxWidth': dataTableRatColumnWidth
                            #    },
                            #    {
                            #        'if':{'column_id':'Threshold'},
                            #        'textAlign':'center',
                            #        'minWidth': dataTableThresholdColumnWidth,
                            #        'width': dataTableThresholdColumnWidth,
                            #        'maxWidth': dataTableThresholdColumnWidth
                            #    }
                            #    ],
                            style_data_conditional = [
                                {
                                    # LTE DCR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':2, 'filter_query':'{Latest Hour} >= 0.13'},
                                    'backgroundColor':'red'
                                },
                                {
                                    # LTE RRC SSR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':3, 'filter_query':'{Latest Hour} < 99'},
                                    'backgroundColor':'red'
                                },
                                {
                                    # LTE eRAB SSR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':4, 'filter_query':'{Latest Hour} < 99'},
                                    'backgroundColor':'red'
                                },
                                {
                                    # VoLTE DCR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':10, 'filter_query':'{Latest Hour} >= 0.13'},
                                    'backgroundColor':'red'
                                },
                                {
                                    # VoLTE eRAB SSR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':12, 'filter_query':'{Latest Hour} < 99'},
                                    'backgroundColor':'red'
                                }
                            ]
                        )
                    ]
                ),
                html.Div(
                    id = 'umtsGeneralKPITable',
                    style=gridelementStyles.umtsGeneralKPITableStyle,
                    children = [
                        dash_table.DataTable(
                            id = 'ranReportUmtsTable',
                            style_header = dataTableStyles.style_header,
                            style_cell = dataTableStyles.style_cell,
                            style_cell_conditional = [
                                {
                                    'if':{'column_id':'KPI\\Object'},
                                    'textAlign':'left',
                                    'minWidth': dataTableObjectColumnWidth,
                                    'width': dataTableObjectColumnWidth,
                                    'maxWidth': dataTableObjectColumnWidth
                                },
                                {
                                    'if':{'column_id':'RAT'},
                                    'textAlign':'center',
                                    'minWidth': dataTableRatColumnWidth,
                                    'width': dataTableRatColumnWidth,
                                    'maxWidth': dataTableRatColumnWidth
                                },
                                {
                                    'if':{'column_id':'Threshold'},
                                    'textAlign':'center',
                                    'minWidth': dataTableThresholdColumnWidth,
                                    'width': dataTableThresholdColumnWidth,
                                    'maxWidth': dataTableThresholdColumnWidth
                                }
                                ],
                            style_data_conditional = [
                                {
                                    # HSDPA DCR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':2, 'filter_query':'{Latest Hour} >= 0.17'},
                                    'backgroundColor':'red'
                                },
                                {
                                    # HSUPA DCR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':3, 'filter_query':'{Latest Hour} >= 0.17'},
                                    'backgroundColor':'red'
                                },
                                {
                                    # UMTS DCR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':4, 'filter_query':'{Latest Hour} >= 0.17'},
                                    'backgroundColor':'red'
                                },
                                {
                                    # HSDPA CSSR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':5, 'filter_query':'{Latest Hour} < 99.87'},
                                    'backgroundColor':'red'
                                },
                                {
                                    # HSUPA CSSR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':6, 'filter_query':'{Latest Hour} < 99.87'},
                                    'backgroundColor':'red'
                                },
                                {
                                    # UMTS CSSR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':7, 'filter_query':'{Latest Hour} < 99.87'},
                                    'backgroundColor':'red'
                                }
                            ]
                        )
                    ]
                ), 
                html.Div(
                    id = 'gsmGeneralKPITable',
                    style=gridelementStyles.gsmGeneralKPITableStyle,
                    children = [
                        dash_table.DataTable(
                            id = 'ranReportGsmTable',
                            style_header = dataTableStyles.style_header,
                            style_cell = dataTableStyles.style_cell,
                            style_cell_conditional = [
                                {
                                    'if':{'column_id':'KPI\\Object'},
                                    'textAlign':'left',
                                    'minWidth': dataTableObjectColumnWidth,
                                    'width': dataTableObjectColumnWidth,
                                    'maxWidth': dataTableObjectColumnWidth
                                },
                                {
                                    'if':{'column_id':'RAT'},
                                    'textAlign':'center',
                                    'minWidth': dataTableRatColumnWidth,
                                    'width': dataTableRatColumnWidth,
                                    'maxWidth': dataTableRatColumnWidth
                                },
                                {
                                    'if':{'column_id':'Threshold'},
                                    'textAlign':'center',
                                    'minWidth': dataTableThresholdColumnWidth,
                                    'width': dataTableThresholdColumnWidth,
                                    'maxWidth': dataTableThresholdColumnWidth
                                }
                                ],
                            style_data_conditional = [
                                {
                                    # GSM CS DCR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':1, 'filter_query':'{Latest Hour} < 99.87'},
                                    'backgroundColor':'red'
                                },
                                {
                                    # GSM CS CSSR style rule
                                    'if':{'column_id':'Latest Hour', 'row_index':2, 'filter_query':'{Latest Hour} >= 0.3'},
                                    'backgroundColor':'red'
                                }
                            ]
                        )
                    ]
                )
            ]
        ),
        # GSM Graph View
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
        # UMTS Graph View
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
        ),
        # LTE Graph View
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
            interval=1800*1000, 
            n_intervals=0
        ),
        dcc.Interval(
            id='viewUpateInterval',
            # interval is expressed in milliseconds (evey 1min)
            #interval=20*1000,
            interval=20*1000,
            n_intervals=0
        ),
        dcc.Interval(
            id='currentKPIWeeklyInterval',
            # interval is expressed in milliseconds (evey 1min)
            interval=42*1000,
            #interval=10*1000,
            n_intervals=0
        )
    ]
)

# Callback to update the graph data
@app.callback(
    [
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
    Input('graphUpateInterval', 'n_intervals')
)
def updateGraph(currentInterval):
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
        height=graphColors.height,
        legend=dict(orientation='h'),
        title=dict(text='LTE Data eRAB SSR'),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    lteVolteCssr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color,  
        margin=dict(l=10, r=10, t=90, b=10),
        height=graphColors.height,
        legend=dict(orientation='h'),
        title=dict(text='VoLTE eRAB SSR'),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    lteDataDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        margin=dict(l=10, r=10, t=90, b=10),
        height=graphColors.height,
        legend=dict(orientation='h'),
        title=dict(text='LTE Data DCR'),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    lteVolteDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        margin=dict(l=10, r=10, t=90, b=10),
        height=graphColors.height,
        legend=dict(orientation='h'),
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
        height=graphColors.height,
        legend=dict(orientation='h'),
        title=dict(text='HSDPA CSSR'),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    hsupaCssr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        margin=dict(l=10, r=10, t=90, b=10),
        height=graphColors.height,
        legend=dict(orientation='h'),
        title=dict(text='HSUPA CSSR'),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    umtsCssr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        margin=dict(l=10, r=10, t=90, b=10),
        height=graphColors.height,
        legend=dict(orientation='h'),
        title=dict(text='UMTS CSSR'),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    hsdpaDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        margin=dict(l=10, r=10, t=90, b=10),
        height=graphColors.height,
        legend=dict(orientation='h'),
        title=dict(text='HSDPA DCR'),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    hsupaDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        margin=dict(l=10, r=10, t=90, b=10),
        height=graphColors.height,
        legend=dict(orientation='h'),
        title=dict(text='HSUPA DCR'),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    umtsDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        margin=dict(l=10, r=10, t=90, b=10),
        height=graphColors.height,
        legend=dict(orientation='h'),
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
        height=graphColors.height,
        legend=dict(orientation='h'),
        title=dict(text='GSM CS CSSR'),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    gsmPsCssr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        margin=dict(l=10, r=10, t=90, b=10),
        height=graphColors.height,
        legend=dict(orientation='h'),
        title=dict(text='GSM PS CSSR'),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    gsmCsDcr.update_layout(
        plot_bgcolor=graphColors.plot_bgcolor, 
        paper_bgcolor=graphColors.paper_bgcolor, 
        font_color=graphColors.font_color, 
        margin=dict(l=10, r=10, t=90, b=10),
        height=graphColors.height,
        legend=dict(orientation='h'),
        title=dict(text='GSM CS DCR'),
        title_font=dict(size=graphColors.graphTitleFontSize),
        legend_font_size=graphColors.legend_font_size
    )
    # Close DB connection
    pointer.close()
    connectr.close()
    return gsmCsCssr, gsmPsCssr, gsmCsDcr, umtsCssr, hsdpaCssr, hsupaCssr, umtsDcr, hsdpaDcr, hsupaDcr, lteVolteDcr, lteDataDcr, lteVolteCssr, lteDataCssr

# Callback to update the General KPI Datatable
@app.callback(
    [
        Output('ranReportLteTable', 'columns'),
        Output('ranReportLteTable', 'data'),
        Output('ranReportLteTable', 'style_cell_conditional'),
        Output('ranReportUmtsTable', 'columns'),
        Output('ranReportUmtsTable', 'data'),
        Output('ranReportGsmTable', 'columns'),
        Output('ranReportGsmTable', 'data')
    ],  
    [
        # Triggered by the view interval
        Input('viewUpateInterval', 'n_intervals'),
        # Triggered by the weekly update interval
        Input('currentKPIWeeklyInterval', 'n_intervals')
    ],
    [
        State('ranReportLteTable', 'data'),
        State('ranReportUmtsTable', 'data'),
        State('ranReportGsmTable', 'data')
    ]
)
def updateDatatable(currentInterval, weeklyInterval, ranReportLteTableStateData, ranReportUmtsTableStateData, ranReportGsmTableStateData):
    currentDateTime = str(datetime.now().strftime('%Y%m%d%H%M'))
    # Instantiate the callback context, to find the button ID that triggered the callback
    callbackContext = dash.callback_context
    # Get button ID
    timer_id = callbackContext.triggered[0]['prop_id'].split('.')[0]
    # If current time minutes is less than 15 minutes, set currentDateTime to the last hour. Reports are generated every 15 minutes past the hour
    if int(currentDateTime[-2:]) < 15:
        currentDateTime = str(int(currentDateTime[:-2]) - 1)
    else:
        currentDateTime = currentDateTime[:-2]
    currentKPIDirList = ran_functions.getFtpPathFileList(ftpLogin, currentKPIGridFilePath)
    for file in currentKPIDirList:
        if currentDateTime in file:
            latestRanReport = currentKPIGridFilePath + file
    ranReportLteTableTmp = pd.read_excel(ran_functions.downloadFtpFile(ftpLogin, currentKPIGridFilePath, latestRanReport), sheet_name='4G Whole Network')
    # Drop columns
    ranReportLteTableTmp = ranReportLteTableTmp.drop('Integrity', axis=1)
    # Copy dataframe columns as rows on the KPI\Object column
    ranReportLteTable['KPI\\Object'] = ranReportLteTableTmp.columns
    ranReportLteTable['RAT'] = '4G'
    # Copy data on first row
    ranReportLteTable['Latest Hour'] = list(ranReportLteTableTmp.iloc[0])
    ranReportLteTable['Latest Hour'][2] = '{:.2f}'.format(float(ranReportLteTable['Latest Hour'][2]))
    ranReportLteTable['Latest Hour'][3] = '{:.2f}'.format(float(ranReportLteTable['Latest Hour'][3]))
    ranReportLteTable['Latest Hour'][4] = '{:.2f}'.format(float(ranReportLteTable['Latest Hour'][4]))
    ranReportLteTable['Latest Hour'][5] = '{:.2f}'.format(float(ranReportLteTable['Latest Hour'][5]))
    ranReportLteTable['Latest Hour'][6] = '{:.2f}'.format(float(ranReportLteTable['Latest Hour'][6]))
    ranReportLteTable['Latest Hour'][7] = '{:.2f}'.format(float(ranReportLteTable['Latest Hour'][7]))
    ranReportLteTable['Latest Hour'][8] = '{:.2f}'.format(float(ranReportLteTable['Latest Hour'][8]))
    ranReportLteTable['Latest Hour'][9] = '{:.2f}'.format(float(ranReportLteTable['Latest Hour'][9]))
    ranReportLteTable['Latest Hour'][10] = '{:.2f}'.format(float(ranReportLteTable['Latest Hour'][10]))
    ranReportLteTable['Latest Hour'][11] = '{:.2f}'.format(float(ranReportLteTable['Latest Hour'][11]))
    ranReportLteTable['Latest Hour'][12] = '{:.2f}'.format(float(ranReportLteTable['Latest Hour'][12]))
    ranReportLteTable['Threshold'] = ['', '', '< 0.13%', '>= 99%', '>= 99%', '', '', '', '', '', '< 0.13%', '', '>= 99%']
    ranReportUmtsTableTmp = pd.read_excel(ran_functions.downloadFtpFile(ftpLogin, currentKPIGridFilePath, latestRanReport), sheet_name='3G Whole Network')
    # Copy dataframe columns as rows on the KPI\Object column
    ranReportUmtsTable['KPI\\Object'] = ranReportUmtsTableTmp.columns[3:]
    ranReportUmtsTable['RAT'] = '3G'
    # Adjust data
    ranReportUmtsTable['Latest Hour'][0] = '{:.2f}'.format(float(ranReportUmtsTableTmp['PS Traffic'].sum()))
    ranReportUmtsTable['Latest Hour'][1] = '{:.2f}'.format(float(ranReportUmtsTableTmp['CS Traffic(Erl)'].sum()))
    ranReportUmtsTable['Latest Hour'][2] = '{:.2f}'.format(float(ranReportUmtsTableTmp['HSDPA DCR(%)'].mean()))
    ranReportUmtsTable['Latest Hour'][3] = '{:.2f}'.format(float(ranReportUmtsTableTmp['HSUPA DCR(%)'].mean()))
    ranReportUmtsTable['Latest Hour'][4] = '{:.2f}'.format(float(ranReportUmtsTableTmp['CS DCR(%)'].mean()))
    ranReportUmtsTable['Latest Hour'][5] = '{:.2f}'.format(float(ranReportUmtsTableTmp['HSDPA CSSR(%)'].mean()))
    ranReportUmtsTable['Latest Hour'][6] = '{:.2f}'.format(float(ranReportUmtsTableTmp['HSUPA CSSR(%)'].mean()))
    ranReportUmtsTable['Latest Hour'][7] = '{:.2f}'.format(float(ranReportUmtsTableTmp['CS CSSR'].mean()))
    ranReportUmtsTable['Latest Hour'][8] = '{:.2f}'.format(float(ranReportUmtsTableTmp['HSDPA Users'].sum()))
    ranReportUmtsTable['Latest Hour'][9] = '{:.2f}'.format(float(ranReportUmtsTableTmp['DL Throughput(kbit/s)'].mean()))
    ranReportUmtsTable['Latest Hour'][10] = '{:.2f}'.format(float(ranReportUmtsTableTmp['CSSR CSFB(%)'].mean()))
    ranReportUmtsTable['Latest Hour'][11] = '{:.2f}'.format(float(ranReportUmtsTableTmp['MOC CSFB SR(%)'].mean()))
    ranReportUmtsTable['Latest Hour'][12] = '{:.2f}'.format(float(ranReportUmtsTableTmp['MTC CSFB SR(%)'].mean()))
    ranReportUmtsTable['Threshold'] = ['', '', '< 0.17%', '< 0.17%', '< 0.17%', '>= 99.87%', '>= 99.87%', '>= 99.87%', '', '', '>= 99%', '>= 99%', '>= 99%']
    ranReportGsmTableTmp = pd.read_excel(ran_functions.downloadFtpFile(ftpLogin, currentKPIGridFilePath, latestRanReport), sheet_name='2G Whole Network')
    # Copy dataframe columns as rows on the KPI\Object column
    ranReportGsmTable['KPI\\Object'] = ranReportGsmTableTmp.columns[3:]
    ranReportGsmTable['RAT'] = '2G'
    # Adjust data
    ranReportGsmTable['Latest Hour'][0] = '{:.2f}'.format(float(ranReportGsmTableTmp['CS Traffic(Erl)'].sum()))
    ranReportGsmTable['Latest Hour'][1] = '{:.2f}'.format(float(ranReportGsmTableTmp['CS CSSR'].mean()))
    ranReportGsmTable['Latest Hour'][2] = '{:.2f}'.format(float(ranReportGsmTableTmp['CS DCR'].mean()))
    ranReportGsmTable['Latest Hour'][3] = '{:.2f}'.format(float(ranReportGsmTableTmp['TCH Client Perceived Congestion'].mean()))
    ranReportGsmTable['Latest Hour'][4] = '{:.2f}'.format(float(ranReportGsmTableTmp['RA333A:BSS Call Establishment Success Rate(%)'].mean()))
    ranReportGsmTable['Latest Hour'][5] = '{:.2f}'.format(float(ranReportGsmTableTmp['PS Traffic'].sum()))
    ranReportGsmTable['Latest Hour'][6] = '{:.2f}'.format(float(ranReportGsmTableTmp['PS CSSR'].mean()))
    ranReportGsmTable['Threshold'] = ['', '>= 99.87%', '<= 0.30%', '', '', '', '']
    lte_style_cell_conditional = [
        {
            'if':{'column_id':'KPI\\Object'},
            'textAlign':'left',
            'minWidth': dataTableObjectColumnWidth,
            'width': dataTableObjectColumnWidth,
            'maxWidth': dataTableObjectColumnWidth
        },
        {
            'if':{'column_id':'RAT'},
            'textAlign':'center',
            'minWidth': dataTableRatColumnWidth,
            'width': dataTableRatColumnWidth,
            'maxWidth': dataTableRatColumnWidth
        },
        {
            'if':{'column_id':'Threshold'},
            'textAlign':'center',
            'minWidth': dataTableThresholdColumnWidth,
            'width': dataTableThresholdColumnWidth,
            'maxWidth': dataTableThresholdColumnWidth
        },
        {
            'if':{'column_id':'Latest Hour'},
            'textAlign':'right',
            'minWidth': dataTableLatestHourColumnWidth,
            'width': dataTableLatestHourColumnWidth,
            'maxWidth': dataTableLatestHourColumnWidth
        }
    ]

    # If the trigger is the weekly interval, update accordingly
    if timer_id == 'currentKPIWeeklyInterval':
        currentKPIDirList = ran_functions.getFtpPathFileList(ftpLogin, weeklyKPIGridFilePath)
        for file in currentKPIDirList:
            # Filename date is stored between these indexes
            currentFileDate = datetime.strptime(file[53:61], '%Y%m%d')
            # If the file date is within the last 7 days, then get the complete filepath
            if currentFileDate > (datetime.now() - timedelta(days=7)):
                latestWeeklyRanReport = weeklyKPIGridFilePath + file
        currentWeekNum = 'Week-' + str(currentFileDate.isocalendar()[1])
        lte_style_cell_conditional.append(
            {
                'if':{'column_id':currentWeekNum},
                'textAlign':'right',
                'minWidth': dataTableLatestHourColumnWidth,
                'width': dataTableLatestHourColumnWidth,
                'maxWidth': dataTableLatestHourColumnWidth
            }
        )
        ranReportLteTableTmp = pd.read_excel(ran_functions.downloadFtpFile(ftpLogin, weeklyKPIGridFilePath, latestWeeklyRanReport), sheet_name='4G Whole Network')
        # Drop columns
        ranReportLteTableTmp = ranReportLteTableTmp.drop('Integrity', axis=1)
        # Assign new list to currentWeekNum column on df
        ranReportLteTable[currentWeekNum] = list(ranReportLteTableTmp.iloc[0])
        ranReportLteTable[currentWeekNum][2] = '{:.2f}'.format(float(ranReportLteTable[currentWeekNum][2]))
        ranReportLteTable[currentWeekNum][3] = '{:.2f}'.format(float(ranReportLteTable[currentWeekNum][3]))
        ranReportLteTable[currentWeekNum][4] = '{:.2f}'.format(float(ranReportLteTable[currentWeekNum][4]))
        ranReportLteTable[currentWeekNum][5] = '{:.2f}'.format(float(ranReportLteTable[currentWeekNum][5]))
        ranReportLteTable[currentWeekNum][6] = '{:.2f}'.format(float(ranReportLteTable[currentWeekNum][6]))
        ranReportLteTable[currentWeekNum][7] = '{:.2f}'.format(float(ranReportLteTable[currentWeekNum][7]))
        ranReportLteTable[currentWeekNum][8] = '{:.2f}'.format(float(ranReportLteTable[currentWeekNum][8]))
        ranReportLteTable[currentWeekNum][9] = '{:.2f}'.format(float(ranReportLteTable[currentWeekNum][9]))
        ranReportLteTable[currentWeekNum][10] = '{:.2f}'.format(float(ranReportLteTable[currentWeekNum][10]))
        ranReportLteTable[currentWeekNum][11] = '{:.2f}'.format(float(ranReportLteTable[currentWeekNum][11]))
        ranReportLteTable[currentWeekNum][12] = '{:.2f}'.format(float(ranReportLteTable[currentWeekNum][12]))
        # Read UMTS Data
        ranReportUmtsTableTmp = pd.read_excel(ran_functions.downloadFtpFile(ftpLogin, weeklyKPIGridFilePath, latestWeeklyRanReport), sheet_name='3G Whole Network')
        # Adjust data
        tmpList = []
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['PS Traffic'].sum())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['CS Traffic(Erl)'].sum())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['HSDPA DCR(%)'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['HSUPA DCR(%)'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['CS DCR(%)'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['HSDPA CSSR(%)'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['HSUPA CSSR(%)'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['CS CSSR'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['HSDPA Users'].sum())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['DL Throughput(kbit/s)'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['CSSR CSFB(%)'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['MOC CSFB SR(%)'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportUmtsTableTmp['MTC CSFB SR(%)'].mean())))
        ranReportUmtsTable[currentWeekNum] = tmpList
        # Read GSM Data
        ranReportGsmTableTmp = pd.read_excel(ran_functions.downloadFtpFile(ftpLogin, weeklyKPIGridFilePath, latestWeeklyRanReport), sheet_name='2G Whole Network')
        # Adjust data
        tmpList = []
        tmpList.append('{:.2f}'.format(float(ranReportGsmTableTmp['CS Traffic(Erl)'].sum())))
        tmpList.append('{:.2f}'.format(float(ranReportGsmTableTmp['CS CSSR'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportGsmTableTmp['CS DCR'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportGsmTableTmp['TCH Client Perceived Congestion'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportGsmTableTmp['RA333A:BSS Call Establishment Success Rate(%)'].mean())))
        tmpList.append('{:.2f}'.format(float(ranReportGsmTableTmp['PS Traffic'].sum())))
        tmpList.append('{:.2f}'.format(float(ranReportGsmTableTmp['PS CSSR'].mean())))
        ranReportGsmTable[currentWeekNum] = tmpList
    # Format columns data
    ranReportLteColumns = [{'name': i, 'id': i} for i in ranReportLteTable.columns]
    ranReportUmtsColumns = [{'name': i, 'id': i} for i in ranReportUmtsTable.columns]
    ranReportGsmColumns = [{'name': i, 'id': i} for i in ranReportGsmTable.columns]
    return ranReportLteColumns, ranReportLteTable.to_dict('records'), lte_style_cell_conditional, ranReportUmtsColumns, ranReportUmtsTable.to_dict('records'), ranReportGsmColumns, ranReportGsmTable.to_dict('records')

# Callback to update the view
@app.callback(
    [
        Output('currentKPIGridContainer', 'style'), 
        Output('gsmGraphGridContainer', 'style'), 
        Output('umtsGraphGridContainer', 'style'), 
        Output('lteGraphGridContainer', 'style')
    ],  
    Input('viewUpateInterval', 'n_intervals')
)
def updateView(currentInterval):
    currentKPIGridContainer = gridContainerStyles.currentKPIGridContainer
    gsmGraphGridContainer = gridContainerStyles.gsmGraphGridContainerStyle
    umtsGraphGridContainer = gridContainerStyles.umtsGraphGridContainerStyle
    lteGraphGridContainer = gridContainerStyles.lteGraphGridContainerStyle
    # We use % to count the cycle
    if currentInterval % 4 == 0:
        currentKPIGridContainer['display'] = 'grid'
        gsmGraphGridContainer['display'] = 'none'
        umtsGraphGridContainer['display'] = 'none'
        lteGraphGridContainer['display'] = 'none'
    elif currentInterval % 4 == 1:
        currentKPIGridContainer['display'] = 'none'
        gsmGraphGridContainer['display'] = 'grid'
        umtsGraphGridContainer['display'] = 'none'
        lteGraphGridContainer['display'] = 'none'
    elif currentInterval % 4 == 2:
        currentKPIGridContainer['display'] = 'none'
        gsmGraphGridContainer['display'] = 'none'
        umtsGraphGridContainer['display'] = 'grid'
        lteGraphGridContainer['display'] = 'none'
    elif currentInterval % 4 == 3:
        currentKPIGridContainer['display'] = 'none'
        gsmGraphGridContainer['display'] = 'none'
        umtsGraphGridContainer['display'] = 'none'
        lteGraphGridContainer['display'] = 'grid'
    return currentKPIGridContainer, gsmGraphGridContainer, umtsGraphGridContainer, lteGraphGridContainer

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5005', dev_tools_silence_routes_logging=False)