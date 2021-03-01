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

def populateLteGraphs(pointer, startTime, lteBandList, volteCssrNetworkWideGraph, cssrNetworkWideGraph, volteDcrNetworkWideGraph, dcrNetworkWideGraph):
    startTimeNetworkWide = (datetime.now()-timedelta(days=startTime)).strftime("%Y-%m-%d")
    for band in lteBandList:
        pointer.execute('SELECT time,erabssr,dcr FROM ran_pf_data.ran_report_4g_report_network_wide where ltecellgroup = \'' + band + '\' and time > \'' + str(startTimeNetworkWide) + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        lteDataDataframe = pd.DataFrame(queryPayload, columns=['time', 'erabssr', 'dcr'])
        #cssrNetworkWideGraph.add_trace(go.Scatter(x=lteDataDataframe['time'], y=lteDataDataframe['erabssr'], name=band, text=topWorst4GeRabSrPerHourDataFrame['cellname']))
        #dcrNetworkWideGraph.add_trace(go.Scatter(x=lteDataDataframe['time'], y=lteDataDataframe['dcr'], name=band, text=topWorst4GDcrPerHourDataFrame['cellname']))
        cssrNetworkWideGraph.add_trace(go.Scatter(x=lteDataDataframe['time'], y=lteDataDataframe['erabssr'], name=band))
        dcrNetworkWideGraph.add_trace(go.Scatter(x=lteDataDataframe['time'], y=lteDataDataframe['dcr'], name=band))
        queryRaw.clear()
        # Since there's no VoLTE on B42, we must skip it from the VolTE graphs
        if band != 'Network Band=42':
            pointer.execute('SELECT time,volteerabssr,voltedcr FROM ran_pf_data.ran_report_4g_report_network_wide where ltecellgroup = \'' + band + '\' and time > \'' + str(startTimeNetworkWide) + '\';')
            queryRaw = pointer.fetchall()
            queryPayload = np.array(queryRaw)
            # Transform the query payload into a dataframe
            wttxDataDataframe = pd.DataFrame(queryPayload, columns=['time', 'volteerabssr', 'voltedcr'])
            #volteCssrNetworkWideGraph.add_trace(go.Scatter(x=wttxDataDataframe['time'], y=wttxDataDataframe['volteerabssr'], name=band, text=topWorst4GVolteDcrPerHourDataFrame['cellname']))
            #volteDcrNetworkWideGraph.add_trace(go.Scatter(x=wttxDataDataframe['time'], y=wttxDataDataframe['voltedcr'], name=band, text=topWorst4GvolteeRabSrPerHourDataFrame['cellname']))
            volteCssrNetworkWideGraph.add_trace(go.Scatter(x=wttxDataDataframe['time'], y=wttxDataDataframe['volteerabssr'], name=band))
            volteDcrNetworkWideGraph.add_trace(go.Scatter(x=wttxDataDataframe['time'], y=wttxDataDataframe['voltedcr'], name=band))
            queryRaw.clear()
        queryRaw.clear()
    return volteCssrNetworkWideGraph, cssrNetworkWideGraph, volteDcrNetworkWideGraph, dcrNetworkWideGraph

def populateUmtsGraphs(pointer, startTime, rncNameList, umtsCssrNetworkWideGraph, hsdpaCssrNetworkWideGraph, hsupaCssrNetworkWideGraph, umtsDcrNetworkWideGraph, hsdpaDcrNetworkWideGraph, hsupaDcrNetworkWideGraph):
    startTimeNetworkWide = (datetime.now()-timedelta(days=startTime)).strftime("%Y-%m-%d")
    for rnc in rncNameList:
        pointer.execute('SELECT time,hsdpadcr,hsupadcr,csdcr,hsdpacssr,hsupacssr,cscssr FROM ran_pf_data.ran_report_3g_report_network_wide where rncname = \'' + rnc + '\' and time > \'' + str(startTimeNetworkWide) + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        umtsDataDataframe = pd.DataFrame(queryPayload, columns=['time', 'hsdpadcr', 'hsupadcr', 'csdcr', 'hsdpacssr', 'hsupacssr', 'cscssr'])
        hsdpaCssrNetworkWideGraph.add_trace(go.Scatter(x=umtsDataDataframe['time'], y=umtsDataDataframe['hsdpacssr'], name=rnc))
        hsupaCssrNetworkWideGraph.add_trace(go.Scatter(x=umtsDataDataframe['time'], y=umtsDataDataframe['hsupacssr'], name=rnc))
        umtsCssrNetworkWideGraph.add_trace(go.Scatter(x=umtsDataDataframe['time'], y=umtsDataDataframe['cscssr'], name=rnc))
        hsdpaDcrNetworkWideGraph.add_trace(go.Scatter(x=umtsDataDataframe['time'], y=umtsDataDataframe['hsdpadcr'], name=rnc))
        hsupaDcrNetworkWideGraph.add_trace(go.Scatter(x=umtsDataDataframe['time'], y=umtsDataDataframe['hsupadcr'], name=rnc))
        umtsDcrNetworkWideGraph.add_trace(go.Scatter(x=umtsDataDataframe['time'], y=umtsDataDataframe['csdcr'], name=rnc))
        queryRaw.clear()
    return umtsCssrNetworkWideGraph, hsdpaCssrNetworkWideGraph, hsupaCssrNetworkWideGraph, umtsDcrNetworkWideGraph, hsdpaDcrNetworkWideGraph, hsupaDcrNetworkWideGraph

def populateGsmGraphs(pointer, startTime, bscNameList, gsmCsCssrNetworkWideGraph, gsmPsCssrNetworkWideGraph, gsmCsDcrNetworkWideGraph):
    startTimeNetworkWide = (datetime.now()-timedelta(days=startTime)).strftime("%Y-%m-%d")
    for bsc in bscNameList:
        pointer.execute('SELECT time,cscssr,csdcr,pscssr FROM ran_pf_data.ran_report_2g_report_network_wide where gbsc = \'' + bsc + '\' and time > \'' + str(startTimeNetworkWide) + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        gsmDataDataframe = pd.DataFrame(queryPayload, columns=['time', 'cscssr', 'csdcr', 'pscssr'])
        gsmCsCssrNetworkWideGraph.add_trace(go.Scatter(x=gsmDataDataframe['time'], y=gsmDataDataframe['cscssr'], name=bsc))
        gsmPsCssrNetworkWideGraph.add_trace(go.Scatter(x=gsmDataDataframe['time'], y=gsmDataDataframe['pscssr'], name=bsc))
        gsmCsDcrNetworkWideGraph.add_trace(go.Scatter(x=gsmDataDataframe['time'], y=gsmDataDataframe['csdcr'], name=bsc))
        queryRaw.clear()
    return gsmCsCssrNetworkWideGraph, gsmPsCssrNetworkWideGraph, gsmCsDcrNetworkWideGraph

def bscHighRefreshQuery(pointer, startTime, bscHighRefresh, bscNameList, gsmGraphValueConversionDict, dataTypeDropdown):
    for bsc in bscNameList:
        pointer.execute('SELECT ' + gsmGraphValueConversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.bsc_performance_data where nename = \'' + bsc + '\' and lastupdate >= \'' + startTime + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        df = pd.DataFrame({dataTypeDropdown:queryPayload[:,0], 'Time':queryPayload[:,1]})
        # Add trace to the plot
        bscHighRefresh.add_trace(go.Scatter(x=df["Time"], y=df[dataTypeDropdown], name=bsc))
        queryRaw.clear()
    return bscHighRefresh

def rncHighRefreshQuery(pointer, startTime, rncHighRefresh, rncNameList, umtsGraphValueConversionDict, dataTypeDropdown):
    for rnc in rncNameList:
        pointer.execute('SELECT ' + umtsGraphValueConversionDict[dataTypeDropdown] + ', lastupdate FROM ran_pf_data.rnc_performance_data where nename = \'' + rnc + '\' and lastupdate >= \'' + startTime + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        df = pd.DataFrame({ dataTypeDropdown:queryPayload[:,0], 'Time':queryPayload[:,1] })
        rncHighRefresh.add_trace(go.Scatter(x=df["Time"], y=df[dataTypeDropdown], name=rnc))
        queryRaw.clear()
    return rncHighRefresh