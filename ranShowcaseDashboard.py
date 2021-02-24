import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import mysql.connector
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
import os
import csv
# Custom libraries
import classes
import styles
import ran_functions

app = dash.Dash(__name__, title='RAN-Ops Dashboard')
server = app.server

# DB Connection Parameters
dbPara = classes.dbCredentials()
ranController = classes.ranControllers()
graphColors = styles.NetworkWideGraphColors()
# Instantiate styles class
gridContainerStyles = styles.gridContainer()
gridelementStyles = styles.gridElement()
dataTableStyles = styles.datatableHeaderStyle()
# RAN Report Variables
ranReportFilepath = "D:\\ftproot\\BSC\\ran_report\\"
ranReportLteColumns = [{'name':'KPI\\Object', 'id':'KPI\\Object'}, {'name':'Whole Network', 'id':'Whole Network'}, {'name':'Threshold', 'id':'Threshold'}]
ranReportLteTable = pd.DataFrame(data={'KPI\\Oject':[], 'Whole Network':[], 'Threshold':[]})
ranReportUmtsColumns = [{'name':'KPI\\Object', 'id':'KPI\\Object'}, {'name':'Whole Network', 'id':'Whole Network'}, {'name':'Threshold', 'id':'Threshold'}]
ranReportUmtsTable = pd.DataFrame(data={'KPI\\Oject':[], 'Whole Network':[], 'Threshold':[]})
ranReportGsmColumns = [{'name':'KPI\\Object', 'id':'KPI\\Object'}, {'name':'Whole Network', 'id':'Whole Network'}, {'name':'Threshold', 'id':'Threshold'}]
ranReportGsmTable = pd.DataFrame(data={'KPI\\Oject':[], 'Whole Network':[], 'Threshold':[]})

app.layout = html.Div(children=[
    html.H1(
        className='showCasetitleHeader',
        children='RAN Ops Dashboard', 
        style={
            'text-align': 'center',
            'color':'white'
            }
    ),
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
            ),
            html.Div(
                id = 'lteGeneralKPITable',
                style=gridelementStyles.lteGeneralKPITableStyle,
                children = [
                    html.H3('LTE General Network KPI'),
                    dash_table.DataTable(
                        id = 'ranReportLteTable',
                        columns = ranReportLteColumns,
                        data = ranReportLteTable.to_dict('records'),
                        style_header = dataTableStyles.style_header,
                        style_cell = dataTableStyles.style_cell,
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
                id = 'umtsGeneralKPITable',
                style=gridelementStyles.umtsGeneralKPITableStyle,
                children = [
                    html.H3('UMTS General Network KPI'), 
                    dash_table.DataTable(
                        id = 'ranReportUmtsTable',
                        columns = ranReportUmtsColumns,
                        data = ranReportUmtsTable.to_dict('records'),
                        style_header = dataTableStyles.style_header,
                        style_cell = dataTableStyles.style_cell,
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
                id = 'gsmGeneralKPITable',
                style=gridelementStyles.gsmGeneralKPITableStyle,
                children = [
                    html.H3('GSM General Network KPI'),
                    dash_table.DataTable(
                        id = 'ranReportGsmTable',
                        columns = ranReportGsmColumns,
                        data = ranReportGsmTable.to_dict('records'),
                        style_header = dataTableStyles.style_header,
                        style_cell = dataTableStyles.style_cell,
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
            )
        ]
    ),
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
    )
    ,
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
        interval=1800000, 
        n_intervals=0
    ),
    dcc.Interval(
        id='viewUpateInterval',
        # interval is expressed in milliseconds (evey 1min)
        interval=20000, 
        n_intervals=0
    )
])

# Callback to update the graph data
@app.callback([
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
    Input('graphUpateInterval', 'n_intervals'))
def updateGraph(currentInterval):
    # starttime is the current date/time - daysdelta
    startTime = 3
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

# Callback to update the Network Check Datatable
@app.callback([
        Output('ranReportLteTable', 'columns'),
        Output('ranReportLteTable', 'data'),
        Output('ranReportUmtsTable', 'columns'),
        Output('ranReportUmtsTable', 'data'),
        Output('ranReportGsmTable', 'columns'),
        Output('ranReportGsmTable', 'data')
    ],  
    Input('graphUpateInterval', 'n_intervals'))
def updateDatatable(currentInterval):
    currentDateTime = str(datetime.now().strftime('%Y%m%d%H%M'))
    # If current time minutes is less than 30 minutes, set currentDateTime to the last hour. Reports are generated every 30 minutes past the hour
    if int(currentDateTime[-2:]) < 30:
        currentDateTime = str(int(currentDateTime[:-2]) - 1)
    else:
        currentDateTime = currentDateTime[:-2]
    for file in os.listdir(ranReportFilepath):
        if currentDateTime in file:
            latestRanReport = ranReportFilepath + file
    
    ranReportLteTable = pd.read_excel(latestRanReport, sheet_name='4G Table')
    ranReportLteTable['Threshold'] = ['< 0.13%', '>= 99.00%', '>= 99%', '', '>= 6500.0000', '', '', '', '', '', '']
    ranReportUmtsTable = pd.read_excel(latestRanReport, sheet_name='3G Table')
    ranReportUmtsTable['Threshold'] = ['< 0.17%', '>= 99.87%', '', '', '', '', '<= 0.30%', '<= 0.30%', '>= 99%', '>= 99%', '', '', '']
    ranReportGsmTable = pd.read_excel(latestRanReport, sheet_name='2G Table')
    ranReportGsmTable['Threshold'] = ['>= 99.87%', '>= 99.87%', '', '', '', '']
    ranReportLteColumns = [{'name': i, 'id': i} for i in ranReportLteTable.columns]
    ranReportUmtsColumns = [{'name': i, 'id': i} for i in ranReportUmtsTable.columns]
    ranReportGsmColumns = [{'name': i, 'id': i} for i in ranReportGsmTable.columns]
    return ranReportLteColumns, ranReportLteTable.to_dict('records'), ranReportUmtsColumns, ranReportUmtsTable.to_dict('records'), ranReportGsmColumns, ranReportGsmTable.to_dict('records')

# Callback to update the view
@app.callback([
        Output('gsmGraphGridContainer', 'style'),  
        Output('umtsGraphGridContainer', 'style'), 
        Output('lteGraphGridContainer', 'style'),
    ],  
    Input('viewUpateInterval', 'n_intervals'))
def updateView(currentInterval):
    if currentInterval%3 == 0:
        return {'display':'grid'}, {'display':'none'}, {'display':'none'}
    elif currentInterval%3 == 1:
        return {'display':'none'}, {'display':'grid'}, {'display':'none'}
    elif currentInterval%3 == 2:
        return {'display':'none'}, {'display':'none'}, {'display':'grid'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5015')