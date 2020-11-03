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

external_stylesheets = ['D:\\Code\\siteDB_testBed\\static\\css\\dash.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# DB Connection Parameters
dbusername = 'sitedb'
dbpassword = 'BSCAltice.123'
hostip = '172.16.121.41'
dbname = 'ran_pf_data'

app.layout = html.Div(children=[
    html.H1(
        children='BSC KPIs', 
        style={'text-align': 'center'}
        ),
    dcc.Dropdown(
        id='timeFrameDropdown',
        options=[{'label':'1 Day', 'value':'1'}, {'label':'3 Days', 'value':'3'}, {'label':'7 Days', 'value':'7'}, {'label':'30 Days', 'value':'30'}],
        # value var is the default value for the drop down.
        value='7'
    ),
    dcc.Dropdown(
        id='dataTypeDropdown',
        options=[
            {'label':'Call Setup Success Rate', 'value':'cssr'}, 
            {'label':'Drop Call Rate', 'value':'dcr'}, 
            {'label':'Assignment Success Rate', 'value':'assignmentsuccessrate'}, 
            {'label':'Location Update Success Rate', 'value':'luupdatesr'}
            ],
        value='cssr'
    ),
    html.Div(children='BSC_01_RRA'),
    dcc.Graph(
        id='bsc01Graph'
    ),
    html.Div(children='BSC_02_STGO'),
    dcc.Graph(
        id='bsc02Graph'
    ),
    html.Div(children='BSC_03_VM'),
    dcc.Graph(
        id='bsc03Graph'
    ),
    html.Div(children='BSC_04_VM'),
    dcc.Graph(
        id='bsc04Graph'
    ),
    html.Div(children='BSC_05_RRA'),
    dcc.Graph(
        id='bsc05Graph'
    ),
    html.Div(children='BSC_06_STGO'),
    dcc.Graph(
        id='bsc06Graph'
    ),
    dcc.Interval(
        id='upateInterval', 
        interval=300000, 
        n_intervals=0
    )
])

# We pass value from the time frame dropdown because it gets updated everytime you change the seleccion on the drop down.
@app.callback([Output('bsc01Graph', 'figure'), Output('bsc02Graph', 'figure'), Output('bsc03Graph', 'figure'), Output('bsc04Graph', 'figure'), Output('bsc05Graph', 'figure'), Output('bsc06Graph', 'figure')], [Input('upateInterval', 'n_intervals'), Input('timeFrameDropdown', 'value'), Input('dataTypeDropdown', 'value')])
def updateGraphData_bsc_01(currentInterval, timeFrameDropdown, dataTypeDropdown):
    daysDelta = int(timeFrameDropdown)
    # starttime is the current date/time - daysdelta
    startTime = (datetime.now() - timedelta(days=daysDelta)).strftime("%Y/%m/%d %H:%M:%S")
    # Connect to DB
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    pointer.execute('SELECT ' + dataTypeDropdown + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_01_RRA\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig1 = px.bar(df, x="Time", y='Value')
    fig1.update_layout()
    queryRaw.clear()
    pointer.execute('SELECT ' + dataTypeDropdown + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_02_STGO\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig2 = px.bar(df, x="Time", y='Value')
    fig2.update_layout()
    queryRaw.clear()
    pointer.execute('SELECT ' + dataTypeDropdown + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_03_VM\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig3 = px.bar(df, x="Time", y='Value')
    fig3.update_layout()
    queryRaw.clear()
    pointer.execute('SELECT ' + dataTypeDropdown + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_04_VM\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig4 = px.bar(df, x="Time", y='Value')
    fig4.update_layout()
    queryRaw.clear()
    pointer.execute('SELECT ' + dataTypeDropdown + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_05_RRA\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig5 = px.bar(df, x="Time", y='Value')
    fig5.update_layout()
    queryRaw.clear()
    pointer.execute('SELECT ' + dataTypeDropdown + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_06_STGO\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig6 = px.bar(df, x="Time", y='Value')
    fig6.update_layout()
    # Close DB connection
    pointer.close()
    connectr.close()
    return fig1, fig2, fig3, fig4, fig5, fig6

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5005')