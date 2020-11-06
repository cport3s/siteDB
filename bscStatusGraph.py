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

graphTitleFontSize = 54

app.layout = html.Div(children=[
    html.H1(
        className='titleHeader',
        children='RAN Ops KPIs', 
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
                style={'width': '50%'}
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
                style={'width': '50%'}
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
        id='upateInterval', 
        interval=300000, 
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
        Output('bsc06Graph', 'figure')
    ], 
    [
        # We use the update interval function and both dropdown menus as inputs for the callback
        Input('upateInterval', 'n_intervals'), 
        Input('timeFrameDropdown', 'value'), 
        Input('dataTypeDropdown', 'value')]
    )
def updateGraphData_bsc(currentInterval, timeFrameDropdown, dataTypeDropdown):
    bscNameList = ['BSC_01_RRA', 'BSC_02_STGO', 'BSC_03_VM', 'BSC_04_VM', 'BSC_05_RRA', 'BSC_06_STGO']
    rncNameList = ['RNC_01_RRA', 'RNC_02_STGO', 'RNC_03_VM', 'RNC_04_VM', 'RNC_05_RRA', 'RNC_06_STGO', 'RNC_07_VM']
    gsmGraphValueConversionDict = {'Call Setup Success Rate':'cssr', 'Drop Call Rate':'dcr', 'Assignment Rate':'assignmentsuccessrate', 'Location Update Success Rate':'luupdatesr'}
    umtsGraphValueconversionDict = {'Call Setup Success Rate':'csconnectionsuccessrate', 'Drop Call Rate':'csdropcallrate', 'Assignment Rate':'rrcconnectionsuccessrate', 'Location Update Success Rate':'pagingsuccessrate'}
    bscGraphList = []
    daysDelta = int(timeFrameDropdown)
    # starttime is the current date/time - daysdelta
    startTime = (datetime.now() - timedelta(days=daysDelta)).strftime("%Y/%m/%d %H:%M:%S")
    # Connect to DB
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    for ne in bscNameList:
        pointer.execute('SELECT ' + gsmGraphValueConversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'' + ne + '\' and lastupdate >= \'' + startTime + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        df = pd.DataFrame({ dataTypeDropdown:queryPayload[:,0], 'Time':queryPayload[:,1] })
        fig = px.bar(df, x="Time", y=dataTypeDropdown, title=ne)
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
    # Close DB connection
    pointer.close()
    connectr.close()
    return bscGraphList[0], bscGraphList[1], bscGraphList[2], bscGraphList[3], bscGraphList[4], bscGraphList[5]

# We pass value from the time frame dropdown because it gets updated everytime you change the seleccion on the drop down.
@app.callback([Output('rnc01Graph', 'figure'), Output('rnc02Graph', 'figure'), Output('rnc03Graph', 'figure'), Output('rnc04Graph', 'figure'), Output('rnc05Graph', 'figure'), Output('rnc06Graph', 'figure'), Output('rnc07Graph', 'figure')], [Input('upateInterval', 'n_intervals'), Input('timeFrameDropdown', 'value'), Input('dataTypeDropdown', 'value')])
def updateGraphData_rnc(currentInterval, timeFrameDropdown, dataTypeDropdown):
    conversionDict = {'Call Setup Success Rate':'csconnectionsuccessrate', 'Drop Call Rate':'csdropcallrate', 'Assignment Rate':'rrcconnectionsuccessrate', 'Location Update Success Rate':'pagingsuccessrate'}
    daysDelta = int(timeFrameDropdown)
    # starttime is the current date/time - daysdelta
    startTime = (datetime.now() - timedelta(days=daysDelta)).strftime("%Y/%m/%d %H:%M:%S")
    # Connect to DB
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    pointer.execute('SELECT ' + conversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.rnc_performance_data where nename = \'RNC_01_RRA\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig1 = px.bar(df, x="Time", y='Value', title='RNC_01_RRA')
    # Set Graph background colores & title font size
    fig1.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=graphTitleFontSize
    )
    # Color the graph
    fig1.update_traces(marker_color='#17FF00')
    queryRaw.clear()
    pointer.execute('SELECT ' + conversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.rnc_performance_data where nename = \'RNC_02_STGO\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig2 = px.bar(df, x="Time", y='Value', title='RNC_02_STGO')
    # Set Graph background colores & title font size
    fig2.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=graphTitleFontSize
    )
    # Color the graph
    fig2.update_traces(marker_color='#17FF00')
    queryRaw.clear()
    pointer.execute('SELECT ' + conversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.rnc_performance_data where nename = \'RNC_03_VM\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig3 = px.bar(df, x="Time", y='Value', title='RNC_03_VM')
    # Set Graph background colores & title font size
    fig3.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=graphTitleFontSize
    )
    # Color the graph
    fig3.update_traces(marker_color='#17FF00')
    queryRaw.clear()
    pointer.execute('SELECT ' + conversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.rnc_performance_data where nename = \'RNC_04_VM\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig4 = px.bar(df, x="Time", y='Value', title='RNC_04_VM')
    # Set Graph background colores & title font size
    fig4.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=graphTitleFontSize
    )
    # Color the graph
    fig4.update_traces(marker_color='#17FF00')
    queryRaw.clear()
    pointer.execute('SELECT ' + conversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.rnc_performance_data where nename = \'RNC_05_RRA\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig5 = px.bar(df, x="Time", y='Value', title='RNC_05_RRA')
    # Set Graph background colores & title font size
    fig5.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=graphTitleFontSize
    )
    # Color the graph
    fig5.update_traces(marker_color='#17FF00')
    queryRaw.clear()
    pointer.execute('SELECT ' + conversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.rnc_performance_data where nename = \'RNC_06_STGO\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig6 = px.bar(df, x="Time", y='Value', title='RNC_06_STGO')
    # Set Graph background colores & title font size
    fig6.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=graphTitleFontSize
    )
    # Color the graph
    fig6.update_traces(marker_color='#17FF00')
    queryRaw.clear()
    pointer.execute('SELECT ' + conversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.rnc_performance_data where nename = \'RNC_07_VM\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig7 = px.bar(df, x="Time", y='Value', title='RNC_07_VM')
    # Set Graph background colores & title font size
    fig7.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=graphTitleFontSize
    )
    # Color the graph
    fig7.update_traces(marker_color='#17FF00')
    # Close DB connection
    pointer.close()
    connectr.close()
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7

@app.callback([Output('bsc01Graph', 'style'), Output('bsc02Graph', 'style'), Output('bsc03Graph', 'style'), Output('bsc04Graph', 'style'), Output('bsc05Graph', 'style'), Output('bsc06Graph', 'style'), Output('rnc01Graph', 'style'), Output('rnc02Graph', 'style'), Output('rnc03Graph', 'style'), Output('rnc04Graph', 'style'), Output('rnc05Graph', 'style'), Output('rnc06Graph', 'style'), Output('rnc07Graph', 'style')], [Input('upateInterval', 'n_intervals')])
def hideGraph(currentInterval):
    if currentInterval%2 == 0:
        return {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}
    else:
        return {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5005')