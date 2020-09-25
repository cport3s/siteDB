# ----------------------------------------------------------LIBRARIES----------------------------------------------------------#
import os
import csv
import matplotlib.pyplot as pyplot
from datetime import datetime
from datetime import timedelta
import numpy
import mysql.connector
# -----------------------------------------------------------OBJECTS-----------------------------------------------------------#

# ----------------------------------------------------------VARIABLES----------------------------------------------------------#
gb_int_rootpath = "D:\\ftproot\\BSC\\Gb_Interface\\"
path_bscFeGe = "D:\\ftproot\\BSC\\BSC_FEGE\\"
static_image_path = "C:\\Apache24\\htdocs\\sitedb_live\\static\\images\\"
path_trxReport = "D:\\ftproot\\BSC\\trx_report\\"
xaxis = []
yaxis = []
neNameList = []
bscNeList = ['BSC_01_RRA', 'BSC_02_STGO', 'BSC_03_VM', 'BSC_04_VM', 'BSC_05_RRA', 'BSC_06_STGO']
# Time range for the interface graphs
daysdelta = 2
# TRX Usage Graph Vars
dbusername = 'sitedb'
dbpassword = 'BSCAltice.123'
hostip = 'localhost'
dbname = 'alticedr_sitedb'
bscName = []
ipPoolId = []
trxQty = []
neNameDict = {'BSC_01_RRA':{'10':0, '11':0, '12':0}, 'BSC_02_STGO':{'10':0, '11':0, '12':0}, 'BSC_03_VM':{'10':0, '11':0, '12':0}, 'BSC_04_VM':{'10':0, '11':0, '12':0}, 'BSC_05_RRA':{'10':0, '11':0, '12':0}, 'BSC_06_STGO':{'10':0, '11':0, '12':0}}
ippool = {10:[], 11:[], 12:[]}
# the width of the bars
width = 0.2
# ----------------------------------------------------------FUNCTIONS----------------------------------------------------------#
def timeparser(timef, sttimef, edtimef):
    # Function to check if timef is between sttimef and edtimef. Must return True or False
    returnvar = False
    # First, format time strings into datetime vars
    start_date = datetime.strptime(sttimef, "%m/%d/%Y %H:%M")
    end_date = datetime.strptime(edtimef, "%m/%d/%Y %H:%M")
    timef = datetime.strptime(timef, "%m/%d/%Y %H:%M")
    # Check if the current date is between the range
    if timef >= start_date and timef <= end_date:
        returnvar = True
    return returnvar

def csv_to_graph(csvdirectorypathf, nef, xaxisf, yaxisf, starttimef, endtimef, data_columnf):
    # Function to open and store X & Y values from CSV to plot in a graph
    # Open CSV file as read-only
    with open(csvdirectorypathf, 'r') as csvfile:
        csvreader = list(csv.reader(csvfile, delimiter=','))
        # Must start in line 7 and end before the line, they contain the raw data.
        for row in csvreader[7:-1]:
            # Only filter the desired NE inside the timeframe
            current_time = timeparser(row[0], starttimef, endtimef)
            if row[1] == nef and current_time:
                xaxisf.append(row[0])
                # We convert from byte to Mbyte before appending to list
                yaxisf.append(float(row[data_columnf]) / (1024 * 1024))
        return xaxisf, yaxisf

def plotLineGraphFunction(ne_statsf, xaxisf, yaxisf, graph_titlef, static_image_pathf):
    # Set plot aspect ratio
    pyplot.rcParams['figure.figsize'] = [16,9]
    # Plot paramteres
    pyplot.plot(xaxisf, yaxisf)
    # Add labels to the graph
    pyplot.title(ne_statsf + ' ' + graph_titlef)
    pyplot.xlabel('Time')
    pyplot.ylabel('MBytes')
    pyplot.savefig('{}{}_{}.png'.format(static_image_path, ne_statsf, graph_titlef), dpi=150)

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
# -----------------------------------------------------------MAINCODE----------------------------------------------------------#
# Cycle through the NE List
for ne_stats in bscNeList:
    # endtime is the current date/time
    endtime = datetime.now().strftime("%m/%d/%Y %H:%M")
    # starttime is the current date/time - daysdelta
    starttime = (datetime.now() - timedelta(days=daysdelta)).strftime("%m/%d/%Y %H:%M")

    # FEGE Statistics Graph
    # First we have to construct the filepath with the latest file on the directory
    # Get the filename list and store it on a list. os.walk return a list of lists, the last position contains a list of filesnames.
    file_list = list(os.walk(path_bscFeGe))[-1][-1]
    # The last position on the list contains the newest file on the directory
    newest_filename = file_list[-1]
    csvdirectorypath = path_bscFeGe + newest_filename
    # Get both axis' information filled
    xaxis, yaxis = csv_to_graph(csvdirectorypath, ne_stats, xaxis, yaxis, starttime, endtime, 6)
    plotLineGraphFunction(ne_stats, xaxis, yaxis, 'FE-GE_Interface', static_image_path)
    # Clear the lists to avoid graph data corruption
    xaxis.clear()
    yaxis.clear()

# TRX Usage Graph
# Connect to DB
connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
# Connection must be buffered when executing multiple querys on DB before closing connection.
pointer = connectr.cursor(buffered=True)
pointer.execute('SELECT * FROM alticedr_sitedb.trx_usage_report;')
# Fetch query payload
queryPayload = pointer.fetchall()
for i in range(len(queryPayload)):
    nename = str(queryPayload[i][0])
    ippoolTemp = str(queryPayload[i][1])
    trx = int(queryPayload[i][2])
    neNameDict[nename][ippoolTemp] = trx
# Move all trxQty stored in neNameDict to ippool, to generate 1 list per pool ID.
for k in neNameDict:
    for p in range(10, 13):
        ippool[p].append(neNameDict[k][str(p)])
# the label locations
x = numpy.arange(len(neNameDict))
# Set plot aspect ratio
pyplot.rcParams['figure.figsize'] = [16,9]
# Create multiple subplots (multiple bars, in this case)
fig, ax = pyplot.subplots()
# Each ax.bar instantiates a bar and gives them properties
pool10 = ax.bar(x - width, ippool[10], width, label='IP Pool 10')
pool11 = ax.bar(x, ippool[11], width, label='IP Pool 11')
pool12 = ax.bar(x + width, ippool[12], width, label='IP Pool 12')
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xticks(x)
ax.set_xticklabels(neNameDict)
ax.legend()
# Label the columns
autolabel(pool10)
autolabel(pool11)
autolabel(pool12)
fig.tight_layout()
pyplot.setp(ax.set_xticklabels(neNameDict), rotation=10, horizontalalignment='center')
pyplot.savefig('{}trx_usage.png'.format(static_image_path), dpi=150)