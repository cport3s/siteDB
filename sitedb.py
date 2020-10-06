# ----------------------------------------------------------LIBRARIES----------------------------------------------------------#
from flask import Flask, render_template, request, redirect, url_for
from wtforms import StringField
import mysql.connector
import os
import csv
from datetime import datetime
import requests
import classes
# -----------------------------------------------------------OBJECTS-----------------------------------------------------------#

# ----------------------------------------------------------VARIABLES----------------------------------------------------------#
# HTML Files
mainhtml = 'Main_Child_Live_Site_Query.html'
errorhtml = 'Error.html'
searchhtml = 'Main_Base.html'
newpcihtml = 'NewInfo_Child_NewSectorInput.html'
newinfohtml = 'NewInfo_Base.html'
newsectorequeryhtml = 'Main_Child_NewSectorQuery.html'
dashboard_main_html = 'Main_Child_Dashboard.html'
wiki_html = 'Main_Child_Wiki.html'

# DB Connection Parameters
dbusername = 'sitedb'
dbpassword = 'BSCAltice.123'
hostip = '172.16.121.41'
dbname = 'alticedr_sitedb'

app = Flask(__name__, template_folder='templates', static_folder='static')
# ----------------------------------------------------------FUNCTIONS----------------------------------------------------------#
def siteconversion(networkElement):
    # Function recieves an instance of a class and must populate all of its vars.
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    pointer = connectr.cursor(buffered=True)
    # Check if siteid is a trans id and get the ran id
    if (len(str(networkElement.siteID)) == 3 or len(str(networkElement.siteID)) == 4) and (str(networkElement.siteID)[0] == '7' or str(networkElement.siteID)[0] == '8'):
        pointer.execute('SELECT * FROM siteinfo WHERE transid = ' + str(networkElement.siteID) + ';')
        querypayload = pointer.fetchone()
        networkElement.siteID = querypayload[0]
    pointer.execute('SELECT * FROM siteinfo WHERE id = ' + str(networkElement.siteID) + ';')
    querypayload = pointer.fetchone()
    # Check if query result is not empty
    if querypayload:
        networkElement.transID = querypayload[7]
        networkElement.tricomName = querypayload[8]
        networkElement.ptiCode = querypayload[2]
        networkElement.lat = querypayload[3]
        networkElement.lon = querypayload[4]
        networkElement.neName = querypayload[1]
        networkElement.neList.append(querypayload[1])
    else:
        networkElement.transID = 'N/A'
        networkElement.tricomName = 'N/A'
        networkElement.ptiCode = 'N/A'
        networkElement.lat = 'N/A'
        networkElement.lon = 'N/A'
        networkElement.neName = 'N/A'
    # Complete missing information and validate it exists on the database
    networkElement.eGbtsName = 'G' + networkElement.neName[1:]
    networkElement.nodebName = 'U' + networkElement.neName[1:]
    networkElement.eNodebName = 'L' + networkElement.neName[1:]
    # Check if all functions exists 
    pointer.execute('select * from alticedr_sitedb.gsmcellpara where egbtsname = \'' + networkElement.eGbtsName + '\';')
    if not(pointer.fetchone()):
        networkElement.eGbtsName = 'N/A'
    pointer.execute('select * from alticedr_sitedb.umtscellpara where unodebname = \'' + networkElement.nodebName + '\';')
    if not(pointer.fetchone()):
        networkElement.nodebName = 'N/A'
    pointer.execute('select * from alticedr_sitedb.ltecellpara where enbname = \'' + networkElement.eNodebName + '\';')
    if not(pointer.fetchone()):
        networkElement.eNodebName = 'N/A'
    # Search for external UMTS Only BBU
    pointer.execute('select * from ippara where functionname = \'' + networkElement.nodebName + '\';')
    querypayload = pointer.fetchone()
    if querypayload:
        if querypayload[0] == networkElement.nodebName:
            # If nename and nodebfunction name are the same, then....
            networkElement.neList.append(querypayload[0])
    # Search for L900 external enodeb
    pointer.execute('select * from ltecellpara where enbid = ' + str(80000 + int(networkElement.siteID)) + ';')
    querypayload = pointer.fetchall()
    if querypayload:
        networkElement.neList.append('UL' + networkElement.neName[1:])
    # Search for WTTx external enodeb
    pointer.execute('select * from ltecellpara where enbid = ' + str(100000 + int(networkElement.siteID)) + ';')
    querypayload = pointer.fetchall()
    if querypayload:
        networkElement.neList.append('LT' + networkElement.neName[1:])
    # Search for NR-NSA external enodeb
    pointer.execute('select * from ltecellpara where enbid = ' + str(110000 + int(networkElement.siteID)) + ';')
    querypayload = pointer.fetchall()
    if querypayload:
        networkElement.neList.append('NR' + networkElement.neName[1:])
    pointer.close()
    connectr.close()

# -----------------------------------------------------------MAINCODE----------------------------------------------------------#
@app.route('/')
# Home Page
def searchsite():
    return render_template(searchhtml)

# Live Site Search result page
@app.route('/siteQuery', methods = ['POST'])
def site_db_consult():
    # Instantiate new ne element
    networkElement = classes.neElement()
    networkElement.neList.clear()
    #networkElement.clrlst()
    networkElement.siteID = int(request.form['siteidh'])
    # Pass instance to function
    siteconversion(networkElement)
    # If site doesn't exists, return error site
    if networkElement.neName == 'N/A' and networkElement.eGbtsName == 'N/A' and networkElement.nodebName == 'N/A' and networkElement.eNodebName:
        return render_template(errorhtml)
    # Connect to DB
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    # Pull IP Data  from DB
    # Instantiate ipParaClass and clear all lists to ensure they are empty.
    ipPara = classes.ipParaClass()
    ipPara.clrlst()
    # Search all siteid's ne names
    for ne in networkElement.neList:
        pointer.execute('select * from alticedr_sitedb.ippara where sitename = \'' + str(ne) + '\';')
        querypayload = pointer.fetchall()
        # If the query payload is not empty, then....
        if querypayload:
            # Append all information to class instance
            for i in range(len(querypayload)):
                ipPara.neName.append(querypayload[i][0])
                ipPara.functionName.append(querypayload[i][1])
                ipPara.cpIP.append(querypayload[i][2])
                ipPara.upIP.append(querypayload[i][3])
                ipPara.gwIP.append(querypayload[i][4])
                ipPara.vlanID.append(querypayload[i][5])
                ipPara.ptpIP.append(querypayload[i][6])
                ipPara.omIP.append(querypayload[i][7])
                ipPara.peerIP.append(querypayload[i][8])
    # Get RET Device Data from DB
    pointer.execute('SELECT * FROM alticedr_sitedb.retpara WHERE sitename = \'' + str(networkElement.neName) + '\';')
    # We use fetchall because the return is a 2D list.
    querypayload = pointer.fetchall()
    # Check if the return is not empty
    # Instantiate new RET Class object to store DB information
    retdevice = classes.RetDevice()
    retdevice.clrlst()
    if querypayload:
        # querypayload contains a matrix array
        # Loop through data that has multiple values
        for i in range(len(querypayload)):
            retdevice.retdeviceno.append(querypayload[i][1])
            retdevice.retdevicename.append(querypayload[i][2])
            retdevice.retsubrack.append(querypayload[i][3])
            retdevice.retmanufacturer.append(querypayload[i][4])
            retdevice.retserial.append(querypayload[i][5])
            retdevice.rettilt.append(querypayload[i][6])
            retdevice.retantmodel.append(querypayload[i][7])
            retdevice.retantmaxtilt.append(querypayload[i][8])
            retdevice.retantmintilt.append(querypayload[i][9])
    # If the return is empty, fill the vars with 'N/A'
    else:
        retdevice.retdeviceno.append('N/A')
        retdevice.retdevicename.append('N/A')
        retdevice.retsubrack.append('N/A')
        retdevice.retmanufacturer.append('N/A')
        retdevice.retserial.append('N/A')
        retdevice.rettilt.append('N/A')
        retdevice.retantmodel.append('N/A')
        retdevice.retantmaxtilt.append('N/A')
        retdevice.retantmintilt.append('N/A')
    # Get GSM Data from DB
    pointer.execute('SELECT * FROM gsmcellpara WHERE egbtsname = \'' + str(networkElement.eGbtsName) + '\';')
    # We use fetchall because the return is a 2D list.
    querypayload = pointer.fetchall()
    # Check if the return is not empty
    # Instantiate new GSM Cell Class object to store DB information
    gsmcell = classes.GSMCell()
    gsmcell.clrlst()
    if querypayload:
        # querypayload contains a matrix array
        gsmcell.btsidx = querypayload[0][0]
        gsmcell.egbtsname = querypayload[0][1]
        gsmcell.bscname = querypayload[0][2]
        gsmcell.egbtsid = querypayload[0][12]
        # Loop through data that has multiple values
        for i in range(len(querypayload)):
            gsmcell.gcellidx.append(querypayload[i][3])
            gsmcell.gcellid.append(querypayload[i][4])
            gsmcell.gcellname.append(querypayload[i][5])
            gsmcell.gband.append(querypayload[i][6])
            gsmcell.glac.append(querypayload[i][7])
            gsmcell.ncc.append(querypayload[i][8])
            gsmcell.bcc.append(querypayload[i][9])
            gsmcell.hsn.append(querypayload[i][10])
            gsmcell.grac.append(querypayload[i][11])
    # If the return is empty, fill the vars with 'N/A'
    else:
        gsmcell.btsidx = 'N/A'
        gsmcell.egbtsname = 'N/A'
        gsmcell.bscname = 'N/A'
        gsmcell.egbtsid = 'N/A'
        gsmcell.gcellidx.append('N/A')
        gsmcell.gcellid.append('N/A')
        gsmcell.gcellname.append('N/A')
        gsmcell.gband.append('N/A')
        gsmcell.glac.append('N/A')
        gsmcell.ncc.append('N/A')
        gsmcell.bcc.append('N/A')
        gsmcell.hsn.append('N/A')
        gsmcell.grac.append('N/A')
    querypayload.clear()
    # Get UMTS Data from DB
    pointer.execute('SELECT * FROM alticedr_sitedb.umtscellpara WHERE unodebname = \'' + str(networkElement.nodebName) + '\';')
    querypayload = pointer.fetchall()
    # Check if the return is not empty
    # Instantiate new UMTS Cell Class object to store DB information
    umtscell = classes.UMTSCell()
    umtscell.clrlst()
    if querypayload:
        umtscell.unodebname = querypayload[0][2]
        umtscell.urncname = querypayload[0][3]
        umtscell.unodebid = 'N/A'
        for i in range(len(querypayload)):
            umtscell.ucellid.append(querypayload[i][0])
            umtscell.ucellname.append(querypayload[i][1])
            umtscell.ulac.append(querypayload[i][4])
            umtscell.urac.append(querypayload[i][5])
            umtscell.dlarfcn.append(querypayload[i][6])
            umtscell.ularfcn.append(querypayload[i][7])
            umtscell.uband.append(querypayload[i][8])
            umtscell.upsc.append(querypayload[i][9])
    # If the return is empty, fill the vars with 'N/A'
    else:
        umtscell.unodebname = 'N/A'
        umtscell.urncname = 'N/A'
        umtscell.unodebid = 'N/A'
        umtscell.ucellid.append('N/A')
        umtscell.ucellname.append('N/A')
        umtscell.ulac.append('N/A')
        umtscell.urac.append('N/A')
        umtscell.dlarfcn.append('N/A')
        umtscell.ularfcn.append('N/A')
        umtscell.uband.append('N/A')
        umtscell.upsc.append('N/A')
    querypayload.clear()
    # Get LTE Data from DB
    pointer.execute('SELECT * FROM alticedr_sitedb.ltecellpara WHERE enbid = ' + str(networkElement.siteID) + ' order by band asc;')
    querypayload = pointer.fetchall()
    # Check if the return is not empty
    # Instantiate new LTE Cell Class object to store DB information
    ltecell = classes.LTECell()
    ltecell.clrlst()
    if querypayload:
        ltecell.enbid = querypayload[0][0]
        ltecell.enbname = querypayload[0][8]
        for i in range(len(querypayload)):
            ltecell.lcellname.append(querypayload[i][9])
            ltecell.lcellid.append(querypayload[i][1])
            ltecell.pci.append(querypayload[i][2])
            ltecell.prach.append(querypayload[i][3])
            ltecell.earfcn.append(querypayload[i][4])
            ltecell.lband.append(querypayload[i][5])
            ltecell.txmode.append(querypayload[i][6])
            ltecell.tac.append(querypayload[i][7])
            ltecell.cellrad.append(querypayload[i][10])
    # If the return is empty, fill the vars with 'N/A'
    else:
        ltecell.enbid = 'N/A'
        ltecell.enbname = 'N/A'
        ltecell.lcellname.append('N/A')
        ltecell.lcellid.append('N/A')
        ltecell.pci.append('N/A')
        ltecell.prach.append('N/A')
        ltecell.earfcn.append('N/A')
        ltecell.lband.append('N/A')
        ltecell.txmode.append('N/A')
        ltecell.tac.append('N/A')
        ltecell.cellrad.append('N/A')
    # Get UL eNodeB Data from DB
    pointer.execute('SELECT * FROM alticedr_sitedb.ltecellpara WHERE enbid = ' + str(80000 + int(networkElement.siteID)) + ';')
    querypayload = pointer.fetchall()
    # Check if the return is not empty
    if querypayload:
        for i in range(len(querypayload)):
            ltecell.lcellname.append(querypayload[i][9])
            ltecell.lcellid.append(querypayload[i][1])
            ltecell.pci.append(querypayload[i][2])
            ltecell.prach.append(querypayload[i][3])
            ltecell.earfcn.append(querypayload[i][4])
            ltecell.lband.append(querypayload[i][5])
            ltecell.txmode.append(querypayload[i][6])
            ltecell.tac.append(querypayload[i][7])
    # If the return is empty, fill the vars with 'N/A'
    else:
        pass
    # Get LT eNodeB Data from DB
    pointer.execute('SELECT * FROM alticedr_sitedb.ltecellpara WHERE enbid = ' + str(100000 + int(networkElement.siteID)) + ';')
    querypayload = pointer.fetchall()
    # Check if the return is not empty
    if querypayload:
        for i in range(len(querypayload)):
            ltecell.lcellname.append(querypayload[i][9])
            ltecell.lcellid.append(querypayload[i][1])
            ltecell.pci.append(querypayload[i][2])
            ltecell.prach.append(querypayload[i][3])
            ltecell.earfcn.append(querypayload[i][4])
            ltecell.lband.append(querypayload[i][5])
            ltecell.txmode.append(querypayload[i][6])
            ltecell.tac.append(querypayload[i][7])
    # If the return is empty, fill the vars with 'N/A'
    else:
        pass
    # Close DB connection
    pointer.close()
    connectr.close()
    # Get transDB site info
    transDbData = classes.transDBInfo()
    response = requests.get('http://transdb/cgi-bin/querysite.py?site_name={}'.format(str(networkElement.siteID)))
    # Check response status code to see if the information was found on server
    if int(response.status_code) == 200:
        # Parse json key 'line' to an array
        dataList = response.json()['line']
        # Cycle through the array and search for the especific site id
        for data in dataList:
            if data['ran_site_name'] == str(networkElement.siteID):
                transDbData.ranSiteId = data['ran_site_name']
                transDbData.transSiteId = data['trans_site_name']
                transDbData.ptiSiteName = data['pti_site_name']
                transDbData.address = data['direccion']
                transDbData.towerTopo = data['Tipo_Torre']
                transDbData.locationType = data['PTI_estructura']
                transDbData.txType = data['Transmision']
                transDbData.manRouter = data['man']
                transDbData.ibnRouter = data['ibn']
                break
            else:
                transDbData.ranSiteId = 'N/A'
                transDbData.transSiteId = 'N/A'
                transDbData.ptiSiteName = 'N/A'
                transDbData.address = 'N/A'
                transDbData.towerTopo = 'N/A'
                transDbData.locationType = 'N/A'
                transDbData.txType = 'N/A'
                transDbData.manRouter = 'N/A'
                transDbData.ibnRouter = 'N/A'
    # 'cellnameh' is a variable in the HTML code on Main.html
    return render_template(mainhtml, networkElement = networkElement, transDbDatah = transDbData, ipPara = ipPara, retDeviceh = retdevice, gsmCellh = gsmcell, umtsCellh = umtscell, lteCellh = ltecell)

# New Sector Query Result
@app.route('/newsectorquery', methods = ['POST'])
def newsectorquery():
    # Declare objects to be used in this route
    gsmcell = classes.GSMCell()
    gsmcell.clrlst()
    ltecell = classes.LTECell()
    ltecell.clrlst()
    siteid = request.form['siteidh']
    sitename, gsmcell.egbtsname, unodebname, ltecell.enbname = siteconversion(siteid)
    # Connect to DB
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    # Execute Query on DB
    # Query LAC from the live site table on DB
    pointer.execute('SELECT lac FROM gsmcellpara WHERE egbtsname = \'' + str(gsmcell.egbtsname) + '\';')
    querypayload = pointer.fetchone()
    gsmcell.glac = querypayload[0]
    # Query new sector information from DB
    pointer.execute('SELECT * FROM gsmnewcell WHERE egbtsname = \'' + str(gsmcell.egbtsname) + '\';')
    querypayload = pointer.fetchall()
    if querypayload:
        for i in range(len(querypayload)):
            gsmcell.gcellid.append(querypayload[i][1])
            gsmcell.ncc.append(querypayload[i][2])
            gsmcell.bcc.append(querypayload[i][3])
            gsmcell.gbcch.append(querypayload[i][4])
            gsmcell.tch1.append(querypayload[i][5])
            gsmcell.tch2.append(querypayload[i][6])
            gsmcell.tch3.append(querypayload[i][7])
    # If the return is empty, fill the vars with 'N/A'
    else:
        gsmcell.egbtsname = 'N/A'
        gsmcell.gcellid.append('N/A')
        gsmcell.ncc.append('N/A')
        gsmcell.bcc.append('N/A')
        gsmcell.gbcch.append('N/A')
        gsmcell.tch1.append('N/A')
        gsmcell.tch2.append('N/A')
        gsmcell.tch3.append('N/A')
    # Query the TAC from the Live Site Table on DB
    pointer.execute('SELECT tac FROM alticedr_sitedb.ltecellpara WHERE enbid = ' + str(siteid) + ';')
    # Query will return a simple list, no need to fetchall.
    querypayload = pointer.fetchone()
    ltecell.tac = querypayload[0]
    # Query new sector information from DB
    pointer.execute('SELECT * FROM alticedr_sitedb.ltenewcell WHERE enbid = ' + str(siteid) + ';')
    # We use fetchall because the return could be a 2D list.
    querypayload = pointer.fetchall()
    # Check if the return is not empty
    if querypayload:
        ltecell.enbid = querypayload[0][0]
        for i in range(len(querypayload)):
            ltecell.lcellid.append(querypayload[i][1])
            ltecell.pci.append(querypayload[i][2])
            ltecell.prach.append(querypayload[i][3])
            ltecell.cellrad.append(querypayload[i][4])
    # If the return is empty, fill the vars with 'N/A'
    else:
        ltecell.enbid = 'N/A'
        ltecell.tac = 'N/A'
        ltecell.lcellid.append('N/A')
        ltecell.pci.append('N/A')
        ltecell.prach.append('N/A')
        ltecell.cellrad.append('N/A')
    # Close DB connection
    pointer.close()
    connectr.close()
    return render_template(newsectorequeryhtml, egbtsnameh = gsmcell.egbtsname, gcellidh = gsmcell.gcellid, ncch = gsmcell.ncc, bcch = gsmcell.bcc, bcchh = gsmcell.gbcch, tch1h = gsmcell.tch1, tch2h = gsmcell.tch2, tch3h = gsmcell.tch3, lach = gsmcell.glac, enbnameh = ltecell.enbname, enbidh = ltecell.enbid, lcellidh = ltecell.lcellid, pcih = ltecell.pci, prachh = ltecell.prach, cellradh = ltecell.cellrad, tach = ltecell.tac)

@app.route('/login', methods=['GET', 'POST'])
# Route for handling the login logic
def login():
    error = None
    if request.method == 'POST':
        # Connect to DB to search for user credentials
        connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
        pointer = connectr.cursor()
        # Search for the input username on the DB and get PW
        pointer.execute('SELECT * FROM usercredentials WHERE username = \'' + request.form['usernameh'] + '\';')
        querypayload = pointer.fetchone()
        if querypayload:
            username = querypayload[0]
            password = querypayload[1]
        else:
            username = "NULL"
            password = "NULL"
        # Close DB connection before comparison to ensure it is closed.
        pointer.close()
        connectr.close()
        if request.form['usernameh'] != username or request.form['passwordh'] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            # If the credentials are correct, we're going to redirect to the /newinfo route
            return redirect(url_for('newinfo'))
    return render_template(searchhtml, errorh=error)

@app.route('/newinfo')
# Login return (New site Info Landing Page)
def newinfo():
    return render_template(newinfohtml)

@app.route('/newsector', methods =['POST'])
# New Sector Input Form
def newsector():
    return render_template(newpcihtml)

@app.route('/newsectorprovisioning', methods =['POST'])
# New PCI Privsioning Function
def newpciprovisioning():
    # Store data in input forms on VARS
    egbtsname = request.form['egbtsnameh']
    gcellid = request.form['gcellidh']
    gncc = request.form['ncch']
    gbcc = request.form['bcch']
    gbcch = request.form['bcchh']
    gtch1 = request.form['tch1h']
    gtch2 = request.form['tch2h']
    gtch3 = request.form['tch3h']
    enbname = request.form['enbnameh']
    lcellid = request.form['cellidh']
    lpci = request.form['pcih']
    lprach = request.form['prachh']
    lcellrad = request.form['cellradh']
    # Now, let's insert values in DB
    # Connect to DB
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    # Check if GSM data is null
    if egbtsname != "":
        # Insert GSM data into DB Table
        query = 'REPLACE INTO gsmnewcell (`egbtsname`, `gcellid`, `ncc`, `bcc`, `bcch`, `tch1`, `tch2`, `tch3`) VALUES (\'' + egbtsname + '\', ' + gcellid + ', ' + gncc + ', ' + gbcc + ', ' + gbcch + ', ' + gtch1 + ', ' + gtch2 + ', ' + gtch3 + ');'
        pointer.execute(query)
        # You have to commit when writing data to DB
        connectr.commit()
    # Check if LTE data is null
    if enbname != "":
        # Insert LTE data into DB Table
        query = 'REPLACE INTO ltenewcell (`enbid`, `cellid`, `pci`, `prach`, `cellrad`) VALUES (' + str(enbname[1:-1]) + ', ' + lcellid + ', ' + lpci + ', ' + lprach + ', ' + lcellrad + ');'
        pointer.execute(query)
        # You have to commit when writing data to DB
        connectr.commit()
    # Close DB connection before comparison to ensure it is closed.
    pointer.close()
    connectr.close()
    return render_template(newpcihtml)

@app.route('/dashboard')
# Dashboard Home Page
def dashboard_main():
    return render_template(dashboard_main_html)

@app.route('/wiki')
# Wiki Home Page
def wiki_main():
    return render_template(wiki_html)