# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import mysql.connector
import numpy as np
import time

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# DB Connection Parameters
dbusername = 'sitedb'
dbpassword = 'BSCAltice.123'
hostip = '172.16.121.41'
dbname = 'ran_pf_data'

# Connect to DB
connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
# Connection must be buffered when executing multiple querys on DB before closing connection.
pointer = connectr.cursor(buffered=True)

pointer.execute('SELECT luupdaterequests, lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_01_RRA\';')
queryRaw = pointer.fetchall()
queryPayload = np.array(queryRaw)
df = pd.DataFrame({ 'LU Requests':queryPayload[:,0], 'Time':queryPayload[:,1] })
fig = px.bar(df, x="Time", y="LU Requests")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''Dash: A web application framework for Python.'''),
    #dcc.Graph(id='example-graph', figure=fig)
    dcc.Graph(id='live-graph', figure=fig, animate=True),
    dcc.Interval(id='graph-update', interval=1000, n_intervals=0)
])

@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])

queryRaw.clear()
# Close DB connection
pointer.close()
connectr.close()

if __name__ == '__main__':
    app.run_server(debug=True)