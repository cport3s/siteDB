import pandas as pd
import mysql.connector
import numpy as np
import classes
from datetime import datetime
from datetime import timedelta

dbPara = classes.dbCredentials()
# Connect to DB
connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
# Connection must be buffered when executing multiple querys on DB before closing connection.
pointer = connectr.cursor(buffered=True)

startTimeNetworkWide = (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")

pointer.execute('SELECT time,cellname,pstraffic FROM ran_pf_data.ran_report_4g_report_specific where time > ' + str(startTimeNetworkWide) + ';')
queryRaw = pointer.fetchall()
queryPayload = np.array(queryRaw)

# Close DB connection
pointer.close()
connectr.close()

topWorst4GDcrPerHourDataFrame = pd.DataFrame(queryPayload, columns=['time', 'cellname', 'pstraffic'])
topWorst4GDcrPerHourDataFrame = topWorst4GDcrPerHourDataFrame.groupby(['time', 'cellname']).max()

print(topWorst4GDcrPerHourDataFrame)