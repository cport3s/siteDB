import plotly.express as px
import mysql.connector
import pandas as pd
import numpy as np
import classes

# Public Token = pk.eyJ1IjoiY2Fwb3J0ZXMiLCJhIjoiY2t1NzJpbjZjMTZ0dzJ4bzY1d2VpMjRobiJ9.8e-KlPtJoXHFFElAcu68uA
# Secret Toekn = sk.eyJ1IjoiY2Fwb3J0ZXMiLCJhIjoiY2t1NzQzc3hlNWdmczJwcDM2Z2Uwbzc5eiJ9.9NuNuihu7bi2Ox4vYWJqag

# DB Connection Parameters
dbPara = classes.dbCredentials()

# Connect to DB
mysqlConnector = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
# Connection must be buffered when executing multiple querys on DB before closing connection.
mysqlPointer = mysqlConnector.cursor(buffered=True)

mysqlPointer.execute('SELECT site,lat,lon,bsc,rnc,provincia FROM alticedr_sitedb.raningdata;')
queryRaw = mysqlPointer.fetchall()
queryPayload = np.array(queryRaw)
siteDataframe = pd.DataFrame(queryPayload, columns=['site', 'lat', 'lon', 'bsc', 'rnc', 'provincia'])
# Cast columns to float type
siteDataframe['lat'] = siteDataframe['lat'].astype(float)
siteDataframe['lon'] = siteDataframe['lon'].astype(float)
map = px.scatter_mapbox(siteDataframe, lat='lat', lon='lon', hover_name='site', hover_data=['bsc', 'rnc'])
map.update_layout(mapbox_style='open-street-map')
map.show()

# Close DB connection
mysqlPointer.close()
mysqlConnector.close()