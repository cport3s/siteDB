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
                    {'label':'Call Setup Success Rate', 'value':'cssr'}, 
                    {'label':'Drop Call Rate', 'value':'dcr'}, 
                    {'label':'Assignment Success Rate', 'value':'assignmentsuccessrate'}, 
                    {'label':'Location Update Success Rate', 'value':'luupdatesr'}
                    ],
                value='luupdatesr',
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
@app.callback([Output('bsc01Graph', 'figure'), Output('bsc02Graph', 'figure'), Output('bsc03Graph', 'figure'), Output('bsc04Graph', 'figure'), Output('bsc05Graph', 'figure'), Output('bsc06Graph', 'figure')], [Input('upateInterval', 'n_intervals'), Input('timeFrameDropdown', 'value'), Input('dataTypeDropdown', 'value')])
def updateGraphData_bsc(currentInterval, timeFrameDropdown, dataTypeDropdown):
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
    fig1 = px.bar(df, x="Time", y='Value', title='BSC_01_RRA')
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
    pointer.execute('SELECT ' + dataTypeDropdown + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_02_STGO\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig2 = px.bar(df, x="Time", y='Value', title='BSC_02_STGO')
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
    pointer.execute('SELECT ' + dataTypeDropdown + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_03_VM\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig3 = px.bar(df, x="Time", y='Value', title='BSC_03_VM')
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
    pointer.execute('SELECT ' + dataTypeDropdown + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_04_VM\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig4 = px.bar(df, x="Time", y='Value', title='BSC_04_VM')
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
    pointer.execute('SELECT ' + dataTypeDropdown + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_05_RRA\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig5 = px.bar(df, x="Time", y='Value', title='BSC_05_RRA')
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
    pointer.execute('SELECT ' + dataTypeDropdown + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_06_STGO\' and lastupdate >= \'' + startTime + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'Value':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig6 = px.bar(df, x="Time", y='Value', title='BSC_06_STGO')
    # Set Graph background colores & title font size
    fig6.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF', 
        title_font_size=graphTitleFontSize
    )
    # Color the graph
    fig6.update_traces(marker_color='#17FF00')
    # Close DB connection
    pointer.close()
    connectr.close()
    return fig1, fig2, fig3, fig4, fig5, fig6



@app.callback([Output('bsc01Graph', 'style'), Output('bsc02Graph', 'style'), Output('bsc03Graph', 'style'), Output('bsc04Graph', 'style'), Output('bsc05Graph', 'style'), Output('bsc06Graph', 'style')], [Input('upateInterval', 'n_intervals')])
def hideGraph(currentInterval):
    if currentInterval%2 == 0:
        return {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}, {'display':'inline'}
    else:
        return {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5005')