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
    # Loop through the query result and remove the excess chars (first 2 (',) and last 3 (,',))
    for apn in queryRaw:
        current = str(apn)[2:-3]
        # If there's an empty position on the results, fill it with 'NULL'
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

# This function receives sql pointer, timeframe and returns list with events and dictionary for the event list dropdown
def getEventDropdownList(pointer, startTime):
    # First, get the whole Details list inside the time frame
    pointer.execute('select Details from mme_logs.session_event where Times > \'' + startTime + '\';')
    # Then, create a dropdown with the list of details
    queryRaw = list(set(pointer.fetchall()))
    eventList = []
    # Loop through the query result and remove the excess chars (first 2 (',) and last 3 (,',))
    for event in queryRaw:
        current = str(event)[2:-3]
        # If there's an empty position on the results, fill it with 'NULL'
        if len(current) < 1:
            eventList.append('NULL')
        else:
            current = current.replace("'", "\\\'")
            eventList.append(current)
    # Parse into an Options Dictionary Format for the drop down
    eventDict = [{'label':i, 'value':i} for i in eventList]
    # Add the "All" apn option to the dictionary
    eventDict.append({'label':'All', 'value':'All'})
    return eventDict, eventList

# This function receives mysql pointer, timeframe, event list and returns the event dictionary to generate the datatable.
def topEventsQuery(pointer, dataTypeDropdown, startTime, eventList):
    # Now, get top 10 APNs from every detail
    eventDict = {"":[]}
    if dataTypeDropdown == 'All':
        dataTypeDropdown = 'Gateway Selection error'
    # loop through the list containing all the different events on the timeframe
    for event in eventList:
        # Initialize dictionary with key and an empty list
        eventDict[event] = []
        data = 'select APN_Used,count(*) from mme_logs.session_event where Details = \'' + event + '\' and Times > \'' + startTime + '\' group by APN_Used order by count(*) desc limit 10;'
        pointer.execute(data)
        queryRaw = pointer.fetchall()
        for query in queryRaw:
            eventDict[event].append({str(query[0]):str(query[1])})
    return eventDict[dataTypeDropdown]
