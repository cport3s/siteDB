#import pandas as pd
#import mysql.connector
#import numpy as np
#import classes
#from datetime import datetime
#from datetime import timedelta
#import coreNetwork_functions
#
#dbPara = classes.coreDbCredentials()
## Connect to DB
#connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.schema)
## Connection must be buffered when executing multiple querys on DB before closing connection.
#pointer = connectr.cursor(buffered=True)
#startTime = (datetime.now() - timedelta(hours=1)).strftime("%Y/%m/%d %H:%M:%S")
#dataTypeDropdown = 'Gateway Selection error'
#dropDownDict, eventList = coreNetwork_functions.getEventDropdownList(pointer, startTime)
#eventDict = coreNetwork_functions.topEventsQuery(pointer, dataTypeDropdown, startTime, eventList)
#
#print(eventDict)
#
## Close DB connection
#pointer.close()
#connectr.close()
