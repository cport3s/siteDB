# ----------------------------------------------------------LIBRARIES----------------------------------------------------------#
import os
import csv
from datetime import datetime
import plotly.graph_objects as go
# ----------------------------------------------------------VARIABLES----------------------------------------------------------#
currentDate = datetime.now().strftime("%Y%m%d")
filePath = "D:\\ftproot\\configuration_files\\NBI_FM\\" + currentDate + "\\"
saveImgPath = "C:\\Apache24\\htdocs\\sitedb_live\\static\\html\\"
alarmInformationList = []
# Dictionary to count disconnection causes
disconnectionCauseCount = {'Port handshake': 0, 'Connection torn down': 0, 'ssl connections': 0, 'Power supply': 0, 'timed out': 0}
# ----------------------------------------------------------FUNCTIONS----------------------------------------------------------#

# -----------------------------------------------------------MAINCODE----------------------------------------------------------#
# Construct complete filepath with last file on the filePath var
currentAlarmFile = filePath + os.listdir(filePath)[-1]
with open(currentAlarmFile) as csvfile:
    lineList = csv.reader(csvfile)
    for alarmRow in lineList:
        # Alarm Name field is located on the column 8 of the csv file
        if alarmRow[8] == 'NE Is Disconnected':
            # Location information field is located on column 17 of the csv file
            alarmInformationList.append(alarmRow[17])
# Loop through alarm list
for alarmRow in alarmInformationList:
    # Loop through dictionary keys
    for key in disconnectionCauseCount:
        # If the key is found within the alarm list text
        if key in alarmRow:
            # Then increase the count value for the given key in the dictionary
            disconnectionCauseCount[key] += 1

fig = go.Figure([go.Bar(x=list(disconnectionCauseCount.keys()), y=list(disconnectionCauseCount.values()), width=0.3)])
fig.write_html(saveImgPath + 'neDisconnectedReport.html')