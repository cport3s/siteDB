# ----------------------------------------------------------LIBRARIES----------------------------------------------------------#
from flask import Flask, render_template, request, redirect, url_for
from wtforms import StringField
import mysql.connector
import os
import csv
from datetime import datetime
import requests

# -----------------------------------------------------------OBJECTS-----------------------------------------------------------#
# transDB class
class transDBInfo():
    ranSiteId = ''
    transSiteId = ''
    ptiSiteName = ''
    address = ''
    towerTopo = ''
    locationType = ''
    txType = ''
    manRouter = ''
    ibnRouter = ''

# RET class
class RetDevice():
    retdeviceno = []
    retdevicename = []
    retsubrack = []
    retmanufacturer = []
    retserial = []
    rettilt = []
    retantmodel = []
    retantmaxtilt = []
    retantmintilt = []

    def clrlst(self):
        self.retdeviceno.clear()
        self.retdevicename.clear()
        self.retsubrack.clear()
        self.retmanufacturer.clear()
        self.retserial.clear()
        self.rettilt.clear()
        self.retantmodel.clear()
        self.retantmaxtilt.clear()
        self.retantmintilt.clear()

# GSM Cell class
class GSMCell():
    btsidx = ''
    egbtsname = ''
    bscname = ''
    egbtsid = ''
    gcellidx = []
    gcellid = []
    gcellname = []
    gband = []
    glac = []
    ncc = []
    bcc = []
    hsn = []
    grac = []
    gbcch = []
    tch1 = []
    tch2 = []
    tch3 = []

    def clrlst(self):
        self.gcellidx.clear()
        self.gcellid.clear()
        self.gcellname.clear()
        self.gband.clear()
        self.glac.clear()
        self.ncc.clear()
        self.bcc.clear()
        self.hsn.clear()
        self.grac.clear()
        self.gbcch.clear()
        self.tch1.clear()
        self.tch2.clear()
        self.tch3.clear()

# UMTS Cell class
class UMTSCell():
    unodebname = ''
    urncname = ''
    unodebid = ''
    ucellid = []
    ucellname = []
    ulac = []
    urac = []
    dlarfcn = []
    ularfcn = []
    uband = []
    upsc = []

    def clrlst(self):
        self.ucellid.clear()
        self.ucellname.clear()
        self.ulac.clear()
        self.urac.clear()
        self.dlarfcn.clear()
        self.ularfcn.clear()
        self.uband.clear()
        self.upsc.clear()

#LTE Cell class
class LTECell():
    enbid = ''
    enbname = ''
    lcellname = []
    lcellid = []
    lband = []
    tac = []
    pci = []
    prach = []
    cellrad = []
    txmode = []
    earfcn = []

    def clrlst(self):
        self.lcellname.clear()
        self.lcellid.clear()
        self.pci.clear()
        self.prach.clear()
        self.earfcn.clear()
        self.lband.clear()
        self.txmode.clear()
        self.tac.clear()
        self.cellrad.clear()
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
def siteconversion(siteid):
    # Function recieves an INT and must return 6 strings and a list
    nelistf = []
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    pointer = connectr.cursor(buffered=True)
    # Check if siteid is a trans id and get the ran id
    if (len(str(siteid)) == 3 or len(str(siteid)) == 4) and (str(siteid)[0] == '7' or str(siteid)[0] == '8'):
        pointer.execute('SELECT * FROM siteinfo WHERE transid = ' + str(siteid) + ';')
        querypayload = pointer.fetchone()
        siteid = querypayload[0]
    pointer.execute('SELECT * FROM siteinfo WHERE id = ' + str(siteid) + ';')
    querypayload = pointer.fetchone()
    # Check if query result is not empty
    if querypayload:
        sitenamef = querypayload[1]
        enbnamef = 'L' + sitenamef[1:]
        nodebnamef = 'U' + sitenamef[1:]
        egbtsnamef = 'G' + sitenamef[1:]
        nodal_idf = querypayload[7]
        tricom_namef = querypayload[8]
        nelistf.append('M' + sitenamef[1:])
        # Search for external NodeB
        pointer.execute('select * from ippara where functionname = \'' + nodebnamef + '\';')
        querypayload = pointer.fetchone()
        if querypayload:
            if querypayload[0] == querypayload[1]:
                # If nename and nodebfunction name are the same, then....
                nelistf.append('U' + sitenamef[1:])
        # Search for L900 external enodeb
        pointer.execute('select * from ltecellpara where enbid = ' + str(80000 + int(siteid)) + ';')
        querypayload = pointer.fetchall()
        if querypayload:
            nelistf.append('UL' + sitenamef[1:])
        # Search for WTTx external enodeb
        pointer.execute('select * from ltecellpara where enbid = ' + str(100000 + int(siteid)) + ';')
        querypayload = pointer.fetchall()
        if querypayload:
            nelistf.append('LT' + sitenamef[1:])
        # Search for NR-NSA external enodeb
        pointer.execute('select * from ltecellpara where enbid = ' + str(110000 + int(siteid)) + ';')
        querypayload = pointer.fetchall()
        if querypayload:
            nelistf.append('NR' + sitenamef[1:])
    else:
        sitenamef = 'N/A'
        enbnamef = 'N/A'
        nodebnamef = 'N/A'
        egbtsnamef = 'N/A'
        nelistf = 'N/A'
        nodal_idf = 'N/A'
        tricom_namef = 'N/A'
    pointer.close()
    connectr.close()
    return siteid, sitenamef, egbtsnamef, nodebnamef, enbnamef, nelistf, nodal_idf, tricom_namef

# -----------------------------------------------------------MAINCODE----------------------------------------------------------#
@app.route('/')
# Home Page
def searchsite():
    return render_template(searchhtml)

# Live Site Search result page
@app.route('/siteQuery', methods = ['POST'])
def site_db_consult():
    siteid = int(request.form['siteidh'])
    siteid, sitename, egbtsname, unodebname, enbname, nelist, nodal_id, tricom_name = siteconversion(siteid)
    # If site doesn't exists, return error site
    if sitename == 'N/A':
        return render_template(errorhtml)
    # Connect to DB
    connectr = mysql.connector.connect(user = dbusername, password = dbpassword, host = hostip, database = dbname)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    # Execute Query on DB
    # Get Site Information from DB
    pointer.execute('SELECT * FROM alticedr_sitedb.siteinfo WHERE id = ' + str(siteid) + ';')
    # Convery query result into a list. We use fetchone because the return is a single list.
    querypayload = pointer.fetchone()
    # Site info data
    lat = querypayload[3]
    lon = querypayload[4]
    pticode = querypayload[2]
    # Get RET Device Data from DB
    pointer.execute('SELECT * FROM retpara WHERE sitename = \'' + str(sitename) + '\';')
    # We use fetchall because the return is a 2D list.
    querypayload = pointer.fetchall()
    # Check if the return is not empty
    # Instantiate new RET Class object to store DB information
    retdevice = RetDevice()
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
    pointer.execute('SELECT * FROM gsmcellpara WHERE egbtsname = \'' + str(egbtsname) + '\';')
    # We use fetchall because the return is a 2D list.
    querypayload = pointer.fetchall()
    # Check if the return is not empty
    # Instantiate new GSM Cell Class object to store DB information
    gsmcell = GSMCell()
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
    pointer.execute('SELECT * FROM alticedr_sitedb.umtscellpara WHERE unodebname = \'' + str(unodebname) + '\';')
    querypayload = pointer.fetchall()
    # Check if the return is not empty
    # Instantiate new UMTS Cell Class object to store DB information
    umtscell = UMTSCell()
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
    pointer.execute('SELECT * FROM alticedr_sitedb.ltecellpara WHERE enbid = ' + str(siteid) + ' order by band asc;')
    querypayload = pointer.fetchall()
    # Check if the return is not empty
    # Instantiate new LTE Cell Class object to store DB information
    ltecell = LTECell()
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
    pointer.execute('SELECT * FROM alticedr_sitedb.ltecellpara WHERE enbid = ' + str(80000 + int(siteid)) + ';')
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
    pointer.execute('SELECT * FROM alticedr_sitedb.ltecellpara WHERE enbid = ' + str(100000 + int(siteid)) + ';')
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
    transDbData = transDBInfo()
    response = requests.get('http://transdb/cgi-bin/querysite.py?site_name={}'.format(str(siteid)))
    # Check response status code to see if the information was found on server
    if int(response.status_code) == 200:
        # Parse json key 'line' to an array
        dataList = response.json()['line']
        # Cycle through the array and search for the especific site id
        for data in dataList:
            if data['ran_site_name'] == str(siteid):
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
    return render_template(mainhtml, pticodeh = pticode, lath = lat, longh = lon, nodalidh = nodal_id, tricomnameh = tricom_name, nelisth = nelist, transDbDatah = transDbData, retDeviceh = retdevice, gsmCellh = gsmcell, umtsCellh = umtscell, lteCellh = ltecell)

# New Sector Query Result
@app.route('/newsectorquery', methods = ['POST'])
def newsectorquery():
    # Declare objects to be used in this route
    gsmcell = GSMCell()
    gsmcell.clrlst()
    ltecell = LTECell()
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