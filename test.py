#from datetime import datetime
#from datetime import timedelta
#import mysql.connector
#import time
#
## DB Connection Parameters
#dbusername = 'sitedb'
#dbpassword = 'BSCAltice.123'
#hostip = '172.16.121.41'
#dbname = 'ran_pf_data'
#
#ne = 'BSC_01_RRA'
#data = []
#bscNameList = ['BSC_01_RRA', 'BSC_02_STGO', 'BSC_03_VM', 'BSC_04_VM', 'BSC_05_RRA', 'BSC_06_STGO']
#
## Connect to DB
#connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
## Connection must be buffered when executing multiple querys on DB before closing connection.
#pointer = connectr.cursor(buffered=True)
#tempDataFrame = {'neName':[], 'ipPoolId':[], 'trxQty':[]}
#
## Loop through BSC Names
#for ne in bscNameList:
#    # Loop through Ip Pool ID range (10 - 12)
#    for ippool in range(10,13):
#        print('{} in Pool {}'.format(ne, ippool))
#        tempDataFrame['neName'].append(ne)
#        tempDataFrame['ipPoolId'].append(ippool)
#        pointer.execute('SELECT trxqty FROM ran_pf_data.trx_usage_data where lastupdate >= \'' + datetime.now().strftime("%Y/%m/%d") + '\' and nename = \'' + ne + '\' and ippoolid = ' + str(ippool) + ' order by lastupdate desc;')
#        queryPayload = pointer.fetchone()
#        # Take the latest value on the DB
#        if queryPayload:
#            data = queryPayload[0]
#        else:
#            data = 0
#        #tempDataFrame['trxQty'].append(queryPayload[0])
#        #ipPoolReportDict[ne][ippool] = queryPayload[0]
#print(data)