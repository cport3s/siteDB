# -----------------------------------------------------------OBJECTS-----------------------------------------------------------#
# NE Element Class
class neElement():
	siteID = ''
	neName = ''
	eGbtsName = ''
	nodebName = ''
	eNodebName = ''
	ptiCode = ''
	lat = ''
	lon = ''
	transID = ''
	tricomName = ''
	neList = []

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

#IP Parameter Class
class ipParaClass():
    neName = []
    functionName = []
    cpIP = []
    upIP = []
    gwIP = []
    vlanID = []
    ptpIP = []
    omIP = []
    peerIP = []

    def clrlst(self):
        self.neName.clear()
        self.functionName.clear()
        self.cpIP.clear()
        self.upIP.clear()
        self.gwIP.clear()
        self.vlanID.clear()
        self.ptpIP.clear()
        self.omIP.clear()
        self.peerIP.clear()

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

#Database credentiales
class dbCredentials():
    dbUsername = 'sitedb'
    dbPassword = 'BSCAltice.123'
    dbServerIp = '172.16.121.41'
    dataTable = 'alticedr_sitedb'
    performanceTable = 'ran_pf_data'
    recordsDataTable = 'datatable_data'

#Core Network Database credentiales
class coreDbCredentials():
    dbUsername = 'root'
    dbPassword = 'Changeme_123'
    dbServerIp = '172.17.102.75'
    schema = 'mme_logs'

# RAN FTP Server Credentials
class ranFtpCredentials():
    hostname = 'bscserver'
    username = 'sitedb'
    password = 'BSCAltice.123'

class ranControllers():
    bscNameList = ['BSC_01_RRA', 'BSC_02_STGO', 'BSC_03_VM', 'BSC_04_VM', 'BSC_05_RRA', 'BSC_06_STGO']
    rncNameList = ['RNC_01_RRA', 'RNC_02_STGO', 'RNC_03_VM', 'RNC_04_VM', 'RNC_05_RRA', 'RNC_06_STGO', 'RNC_07_VM']
    lteBandList = ['Network Band=2', 'Network Band=5', 'Network Band=4', 'Network Band=42', 'Network Band=8']