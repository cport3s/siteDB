import plotly.express as px
import mysql.connector
import pandas as pd
import numpy as np
import classes

# DB Connection Parameters
dbPara = classes.dbCredentials()

# Connect to DB
mysqlConnector = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
# Connection must be buffered when executing multiple querys on DB before closing connection.
mysqlPointer = mysqlConnector.cursor(buffered=True)

px.set_mapbox_access_token(open('pk.eyJ1IjoiY2Fwb3J0ZXMiLCJhIjoiY2t1NzJpbjZjMTZ0dzJ4bzY1d2VpMjRobiJ9.8e-KlPtJoXHFFElAcu68uA').read())
mysqlPointer.execute('SELECT nodo,lat,lon FROM alticedr_sitedb.raningdata;')
queryRaw = mysqlPointer.fetchall()
queryPayload = np.array(queryRaw)
siteDataframe = pd.DataFrame(queryPayload, columns=['nodo', 'lat', 'lon'])
map = px.scatter_mapbox(siteDataframe, lat='lat', lon='lon')
map.show()

# Close DB connection
mysqlPointer.close()
mysqlConnector.close()