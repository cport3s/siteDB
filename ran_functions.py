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

neList = classes.ranControllers()

def populateLteGraphs(pointer, startTime, lteBandList, volteCssrNetworkWideGraph, cssrNetworkWideGraph, volteDcrNetworkWideGraph, dcrNetworkWideGraph):
    startTimeNetworkWide = (datetime.now()-timedelta(days=startTime)).strftime("%Y-%m-%d")
    for band in lteBandList:
        pointer.execute('SELECT time,erabssr,dcr FROM ran_pf_data.ran_report_4g_report_network_wide where ltecellgroup = \'' + band + '\' and time > \'' + str(startTimeNetworkWide) + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        lteDataDataframe = pd.DataFrame(queryPayload, columns=['time', 'erabssr', 'dcr'])
        # Add dataframe data to figure object
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

def graphInsightQuery(currentGraph, startTime, selectedKPI, pointer):
    startTimeNetworkWide = (datetime.now()-timedelta(days=startTime)).strftime("%Y-%m-%d")
    kpiDict = {'LTE Data CSSR':'erabssr', 'LTE Data DCR': 'dcr', 'VoLTE CSSR': 'volteerabssr', 'VoLTE DCR': 'voltedcr', 'GSM CS CSSR': 'cscssr', 'GSM PS CSSR': 'pscssr', 'GSM CS DCR': 'csdcr', 'UMTS CSSR': 'cscssr', 'UMTS DCR': 'csdcr', 'HSDPA CSSR': 'hsdpacssr', 'HSDPA DCR': 'hsdpadcr', 'HSUPA CSSR': 'hsupacssr', 'HSUPA DCR': 'hsupadcr'}
    kpiSpecificDict = {'LTE Data CSSR':'dataerabssr', 'LTE Data DCR': 'datadcr', 'VoLTE CSSR': 'volteerabssr', 'VoLTE DCR': 'voltedcr', 'GSM CS CSSR': 'cscssr', 'GSM PS CSSR': 'pscssr', 'GSM CS DCR': 'csdcr', 'UMTS CSSR': 'cscssr', 'UMTS DCR': 'csdcr', 'HSDPA CSSR': 'hsdpacssr', 'HSDPA DCR': 'hsdpadcr', 'HSUPA CSSR': 'hsupacssr', 'HSUPA DCR': 'hsupadcr'}
    networkWidetable = ''
    topTable = ''
    condition = ''
    order = ''
    currentList = ''
    if 'LTE' in selectedKPI or 'VoLTE' in selectedKPI:
        currentList = neList.lteBandList
        networkWidetable = 'ran_report_4g_report_network_wide'
        topTable = 'ran_report_4g_report_specific'
        condition = 'ltecellgroup = \''
    elif 'UMTS' in selectedKPI or 'HSDPA' in selectedKPI or 'HSUPA' in selectedKPI:
        currentList = neList.rncNameList
        networkWidetable = 'ran_report_3g_report_network_wide'
        topTable = 'ran_report_3g_report_specific'
        condition = 'rncname = \''
    elif 'GSM' in selectedKPI:
        currentList = neList.bscNameList
        networkWidetable = 'ran_report_2g_report_network_wide'
        topTable = 'ran_report_2g_report_specific'
        condition = 'gbsc = \''
    else:
        return currentGraph

    if 'DCR' in selectedKPI:
        order = 'desc'
    elif 'CSSR' in selectedKPI:
        order = 'asc'
    else:
        return currentGraph
    # Query TOP cell names from DB
    pointer.execute('select b.time,b.cellname,b.' + kpiSpecificDict[selectedKPI] + ' from (select a.time,a.cellname,a.' + kpiSpecificDict[selectedKPI] + ',row_number() over (partition by a.time order by a.' + kpiSpecificDict[selectedKPI] + ' ' + order + ') as rn from ran_pf_data.' + topTable + ' a where a.time >= \'' + str(startTimeNetworkWide) + '\') b where b.rn = 1')
    queryRaw = pointer.fetchall()
    queryPayload = np.array(queryRaw)
    topWorstPerHourDataFrame = pd.DataFrame(queryPayload, columns=['time', 'cellname', kpiSpecificDict[selectedKPI]])
    queryRaw.clear()
    for ne in currentList:
        query = 'select time,' + kpiDict[selectedKPI] + ' from ran_pf_data.' + networkWidetable + ' where ' + condition + ne + '\' and time > \'' + str(startTimeNetworkWide) + '\';'
        pointer.execute(query)
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        DataDataframe = pd.DataFrame(queryPayload, columns=['time', kpiDict[selectedKPI]])
        currentGraph.add_trace(go.Scatter(x=DataDataframe['time'], y=DataDataframe[kpiDict[selectedKPI]], name=ne, text=topWorstPerHourDataFrame['cellname']))
        queryRaw.clear()
    return currentGraph

def queryTxData(pointer, startTime, bscNameList, rncNameList, umtsNetworkPacketLossGraph, umtsNetworkDelayGraph, gsmNetworkPacketLossGraph, gsmNetworkDelayGraph):
    startTimeNetworkWide = (datetime.now()-timedelta(days=startTime)).strftime("%Y-%m-%d")
    for rnc in rncNameList:
        pointer.execute('SELECT date,delay,lost FROM ran_pf_data.rnc_packetloss_data where rncname = \'' + rnc + '\' and date > \'' + str(startTimeNetworkWide) + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        umtsDataDataframe = pd.DataFrame(queryPayload, columns=['date', 'delay', 'lost'])
        umtsNetworkPacketLossGraph.add_trace(go.Scatter(x=umtsDataDataframe['date'], y=umtsDataDataframe['lost'], name=rnc))
        umtsNetworkDelayGraph.add_trace(go.Scatter(x=umtsDataDataframe['date'], y=umtsDataDataframe['delay'], name=rnc))
        queryRaw.clear()
    for bsc in bscNameList:
        pointer.execute('SELECT date,delay,lost FROM ran_pf_data.bsc_packetloss_data where bscname = \'' + bsc + '\' and date > \'' + str(startTimeNetworkWide) + '\';')
        queryRaw = pointer.fetchall()
        queryPayload = np.array(queryRaw)
        # Transform the query payload into a dataframe
        gsmDataDataframe = pd.DataFrame(queryPayload, columns=['date', 'delay', 'lost'])
        gsmNetworkPacketLossGraph.add_trace(go.Scatter(x=gsmDataDataframe['date'], y=gsmDataDataframe['lost'], name=bsc))
        gsmNetworkDelayGraph.add_trace(go.Scatter(x=gsmDataDataframe['date'], y=gsmDataDataframe['delay'], name=bsc))
        queryRaw.clear()
    return umtsNetworkPacketLossGraph, umtsNetworkDelayGraph, gsmNetworkPacketLossGraph, gsmNetworkDelayGraph

def queryTopRecords(pointer, dataTableColumns, dbTable):
    dataTableData = []
    # Check if db table content
    pointer.execute('SELECT * FROM datatable_data.' + dbTable + ';')
    # If it's not empty, the append to the datatable content
    queryRaw = pointer.fetchall()
    if queryRaw:
        tempDict = {}
        # Loop the column headers list
        for i in range(len(queryRaw)):
            # Loop the db content list
            for y in range(len(dataTableColumns)):
                # Populate the entry's dictionary
                tempDict[dataTableColumns[y]['id']] = queryRaw[i][y]
            # Append that dictionary to the list
            dataTableData.append(tempDict)
            tempDict = {}
    # If the query content is empty, append an empty line to data
    else:
        dataTableData.append({'': ''})
    return dataTableData

def insertDataTable(pointer, connectr, dbTable, dataTableData):
    # First, we must query the column names from the table
    pointer.execute('SELECT * FROM datatable_data.' + dbTable + ';')
    # Description method of pointer return a tuple of tuples, containing the column name on positon 0 on each tuple
    columnNames = [column[0] for column in pointer.description]
    # Clean up the entire table
    pointer.execute('DELETE FROM datatable_data.' + dbTable + ';')
    # Now, we must construct the REPLACE query
    query = 'REPLACE INTO `datatable_data`.`' + dbTable + '` ('
    for i in range(len(columnNames)-1):
        query += '`' + str(columnNames[i]) + '`'
        # Add , to separate column names in query
        if i < len(columnNames)-2:
            query += ', '
    query += ') VALUES ('
    # Create temporary list with datatable data values
    tempList = []
    try:
        # We must always delete the key '' in case the datatable comes with an empty value
        dataTableData[0].pop('')
    except:
        pass
    #print(dataTableData[0])
    for i in range(len(dataTableData)):
        tempList.append([v for v in dataTableData[i].values()])
    for i in range(len(tempList)):
        for y in range(len(columnNames)-1):
            query += '\'' + str(tempList[i][y]) + '\''
            # Separate values by coma
            if y < len(columnNames)-2:
                query += ', '
        query += ")"
        # Separate groups of values by coma
        if i < len(dataTableData)-1:
            query += ', ('
    # Close query
    query += ";"
    pointer.execute(query)
    connectr.commit()