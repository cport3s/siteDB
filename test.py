#import mysql.connector
#import ran_functions
#import classes
#
## DB Connection Parameters
#dbPara = classes.dbCredentials()
#
#dataTableColumns = [{'name': 'eNodeB Name', 'id':'eNodeB Name'}, {'name': 'TTK', 'id':'TTK'}, {'name': 'Responsable', 'id':'Responsable'}]
#
## Connect to DB
#connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.recordsDataTable)
## Connection must be buffered when executing multiple querys on DB before closing connection.
#pointer = connectr.cursor(buffered=True)
## Fill datatable data with db table content
#dbTable = 'topworst4gerabsrrercord'
#dataTableData = []
## Check if db table content
#pointer.execute('SELECT * FROM datatable_data.' + dbTable + ';')
## If it's not empty, the append to the datatable content
#queryRaw = pointer.fetchall()
## Description method of pointer return a tuple of tuples, containing the column name on positon 0 on each tuple
#columnNames = [field[0] for field in pointer.description]
#print(columnNames)
#
##if queryRaw:
##    tempDict = {}
##    # Loop the column headers list
##    for i in range(len(queryRaw)):
##        # Loop the db content list
##        for y in range(len(dataTableColumns)):
##            # Populate the entry's dictionary
##            tempDict[dataTableColumns[y]['id']] = queryRaw[i][y]
##        # Append that dictionary to the list
##        dataTableData.append(tempDict)
##        tempDict = {}
##        print(dataTableData)
### If the query content is empty, append an empty line to data
##else:
##    dataTableData.append({'': ''})
##print(dataTableData)
## Close DB Connection
#pointer.close()
#connectr.close()