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
pointer.execute('select Times,Details from mme_logs.session_event where Times > \'' + str(startTime) + '\';')
queryRaw = pointer.fetchall()
queryPayload = np.array(queryRaw)


# Close DB connection
pointer.close()
connectr.close()

mmeSessionEventsDataframe = pd.DataFrame(queryPayload, columns = ['Times','Details'])
mmeSessionEventsDataframe = mmeSessionEventsDataframe.groupby('Details').count()
#mmeSessionEventsDataframe = mmeSessionEventsDataframe.groupby('Details').count().transform('count')

print(mmeSessionEventsDataframe)
