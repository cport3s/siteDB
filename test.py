#import pandas as pd
#import mysql.connector
#import numpy as np
#import classes
#from datetime import datetime
#from datetime import timedelta
#
#def topEventsQuery(pointer, dataTypeDropdown, startTime):
#    # First, get the whole Details list inside the time frame
#    pointer.execute('select Details from mme_logs.session_event where Times > \'' + startTime + '\';')
#    # Then, create a dropdown with the list of details
#    queryRaw = list(set(pointer.fetchall()))
#    eventList = []
#    for event in queryRaw:
#        current = str(event)[2:-3]
#        if len(current) < 1:
#            eventList.append('NULL')
#        else:
#            eventList.append(str(event)[2:-3])
#    # Now, get top 10 APNs from every detail
#    eventDict = {}
#    # loop through the list containing all the different events on the timeframe
#    for event in eventList:
#        pointer.execute('select APN_Used,count(*) from mme_logs.session_event where Details = \'' + event + ' and Times > \'' + startTime + '\' group by APN_Used order by count(*) desc limit 10;')
#        queryRaw = pointer.fetchall()
#        for i in range(len(queryRaw[0])):
#            eventDict[event] = []
#            eventDict[event].append({queryRaw[0][i]:queryRaw[1][i]})
#    return eventDict
#
#dbPara = classes.coreDbCredentials()
## Connect to DB
#connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.schema)
## Connection must be buffered when executing multiple querys on DB before closing connection.
#pointer = connectr.cursor(buffered=True)
#startTime = (datetime.now() - timedelta(hours=1)).strftime("%Y/%m/%d %H:%M:%S")
#
#eventDict = coreNetwork_functions.topEventsQuery(pointer, dataTypeDropdown, startTime)
#
## Close DB connection
#pointer.close()
#connectr.close()
#
#print(apnDict)
