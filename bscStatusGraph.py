import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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

app.layout = html.Div(children=[
    html.H1(children='BSC KPIs'),
    html.Div(children='''Number of LU requests.'''),
    dcc.Dropdown(
        options=[{'label':'1 Day', 'value':'1'}, {'label':'3 Days', 'value':'3'}, {'label':'7 Days', 'value':'7'}, {'label':'30 Days', 'value':'30'}], 
        value='timeFrameDropdown'
    ),
    #dcc.Graph(id='example-graph', figure=fig)
    dcc.Graph(id='liveGraph'),
    dcc.Interval(id='upateInterval', interval=300000, n_intervals=0)
])

@app.callback(Output('liveGraph', 'figure'), [Input('upateInterval', 'n_intervals')])
def updateGraphData(n):
    # Connect to DB
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    pointer.execute('SELECT luupdaterequests, lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'BSC_01_RRA\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    df = pd.DataFrame({ 'LU Requests':queryPayload[:,0], 'Time':queryPayload[:,1] })
    fig = px.bar(df, x="Time", y="LU Requests")
    fig.update_layout()
    queryRaw.clear()
    # Close DB connection
    pointer.close()
    connectr.close()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5005')