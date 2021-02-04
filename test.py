import pandas as pd
import mysql.connector
import numpy as np
import classes
from datetime import datetime
from datetime import timedelta

dbPara = classes.coreDbCredentials()
# Connect to DB
connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.schema)
# Connection must be buffered when executing multiple querys on DB before closing connection.
pointer = connectr.cursor(buffered=True)

startTime = (datetime.now() - timedelta(hours=1)).strftime("%Y/%m/%d %H:%M:%S")
#print('test')
pointer.execute('select APN_Used from mme_logs.session_event where Times > \'' + str(startTime) + '\';')
queryRaw = list(set(pointer.fetchall()))
apnList = []
apnDict = {}
for apn in queryRaw:
    current = str(apn)[2:-3]
    print(current + " " + str(len(current)))
    if len(current) < 1:
        apnList.append('NULL')
    else:
        apnList.append(str(apn)[2:-3])

# Close DB connection
pointer.close()
connectr.close()

print(apnList)
