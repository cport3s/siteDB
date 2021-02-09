import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import mysql.connector
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
import os
import csv
import classes

# Function to query APN list
def getApnDropdownList(pointer, startTime):
    # Get APN Dropdown List
    pointer.execute('select APN_Used from mme_logs.session_event where Times >= \'' + str(startTime) + '\';')
    queryRaw = list(set(pointer.fetchall()))
    apnList = []
    for apn in queryRaw:
        current = str(apn)[2:-3]
        if len(current) < 1:
            apnList.append('NULL')
        else:
            apnList.append(str(apn)[2:-3])
    # Parse into an Options Dictionary Format for the drop down
    apnDict = [{'label':i, 'value':i} for i in apnList]
    # Add the "All" apn option to the dictionary
    apnDict.append({'label':'All', 'value':'All'})
    return apnDict

# This function generates the pie chart and the APN dropdown list.
def logEventDistributionQuery(pointer, graphTitleFontSize, dataTypeDropdown, startTime):
    apnQuery = ""
    # If the drop down is not "All", then there's an APN selected
    if dataTypeDropdown != 'All':
        apnQuery = 'APN_Used = \'' + str(dataTypeDropdown) + '\' and'
    # Fetch Details from db
    pointer.execute('select Times,Details from mme_logs.session_event where ' + apnQuery + ' Times > \'' + str(startTime) + '\';')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    mmeSessionEventsDataframe = pd.DataFrame(queryPayload, columns = ['Times', 'Details'])
    mmeSessionEventsDataframe = mmeSessionEventsDataframe.groupby('Details', as_index=False)['Details'].agg({'id_count':'count'})
    mmeSessionEventsPie = px.pie(mmeSessionEventsDataframe, names = 'Details', values = 'id_count')
    mmeSessionEventsPie.update_layout(
        plot_bgcolor='#000000', 
        paper_bgcolor='#000000', 
        font_color='#FFFFFF',
        title_font_size=graphTitleFontSize,
        font_size=graphTitleFontSize, 
        title='MME Event Logs',
        height=1000,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    mmeSessionEventsPie.update_traces(textinfo='value')
    return mmeSessionEventsPie

def topEventsQuery(pointer, dataTypeDropdown, startTime):
    # First, get the whole Details list inside the time frame
    pointer.execute('select Details from mme_logs.session_event where Times > \'' + startTime + '\';')
    # Then, create a dropdown with the list of details
    queryRaw = list(set(pointer.fetchall()))
    eventList = []
    for event in queryRaw:
        current = str(event)[2:-3]
        if len(current) < 1:
            eventList.append('NULL')
        else:
            eventList.append(str(event)[2:-3])
    # Now, get top 10 APNs from every detail
    eventDict = {}
    # loop through the list containing all the different events on the timeframe
    for event in eventList:
        pointer.execute('select APN_Used,count(*) from mme_logs.session_event where Details = \'' + event + '\' and Times > \'' + startTime + '\' group by APN_Used order by count(*) desc limit 10;')
        queryRaw = pointer.fetchall()
        for i in range(len(queryRaw[0])):
            eventDict[event].append({queryRaw[0][i]:queryRaw[1][i]})
    return eventDict