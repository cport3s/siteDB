#import pandas as pd
#import mysql.connector
#import numpy as np
#import classes
#from datetime import datetime
#from datetime import timedelta
#
#dbPara = classes.dbCredentials()
## Connect to DB
#connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
## Connection must be buffered when executing multiple querys on DB before closing connection.
#pointer = connectr.cursor(buffered=True)
#
#startTimeNetworkWide = (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
##print('test')
#pointer.execute('SELECT time,cellname,pstraffic FROM ran_pf_data.ran_report_4g_report_specific where time > \'' + str(startTimeNetworkWide) + '\';')
#queryRaw = pointer.fetchall()
#queryPayload = np.array(queryRaw)
#
#
## Close DB connection
#pointer.close()
#connectr.close()
#
#topWorst4GDcrPerHourDataFrame = pd.DataFrame(queryPayload, columns=['time', 'cellname', 'pstraffic'])
##print(topWorst4GDcrPerHourDataFrame.index())
#topWorst4GDcrPerHourDataFrameTemp = topWorst4GDcrPerHourDataFrame.groupby(['time']).max()
#for i,j in topWorst4GDcrPerHourDataFrameTemp['time', 'pstraffic']:
#    print(topWorst4GDcrPerHourDataFrame.loc[topWorst4GDcrPerHourDataFrame['time']==i, topWorst4GDcrPerHourDataFrame['pstraffic']==j, 'cellname'])
#print(topWorst4GDcrPerHourDataFrameTemp)




#tempTimeList = set(topWorst4GDcrPerHourDataFrame['time'])
#tempTopList = []
#for time in tempTimeList:
#    if topWorst4GDcrPerHourDataFrame['time'] == time:
#        pass
#
#print(topWorst4GDcrPerHourDataFrame)
