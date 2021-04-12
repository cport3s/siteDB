from ftplib import FTP
from io import BytesIO
import pandas as pd
from datetime import datetime

class ranFtpCredentials():
    hostname = 'bscserver'
    username = 'sitedb'
    password = 'BSCAltice.123'

topWorstFilePath = '/BSC/top_worst_report/'
currentDate = str(datetime.now().strftime('%Y%m%d'))
current2GTopWorstCssrFile = ""
current2GTopWorstDcrFile = ""
current3GTopWorstFile = ""
current4GTopWorstFile = ""

def getFtpPathFileList(ftpLogin, filePath):
    fileName = ""
    # Instantiate FTP connection
    ftp = FTP(host=ftpLogin.hostname)
    ftp.login(user=ftpLogin.username, passwd=ftpLogin.password)
    # Move to desired path
    ftp.cwd(filePath)
    fileName = ftp.nlst()
    return fileName

def downloadFtpFile(ftpLogin, filePath, fileName):
    # Instantiate FTP connection
    ftp = FTP(host=ftpLogin.hostname)
    ftp.login(user=ftpLogin.username, passwd=ftpLogin.password)
    # Move to desired path
    ftp.cwd(filePath)
    # Instantiate a BytesIO object to temp store the xlsx file from the FTP server
    b = BytesIO()
    # Return file as binary with retrbinary functon. Must send according RETR command as part of FTP protocol
    ftp.retrbinary('RETR ' + fileName, b.write)
    # Open as Dataframe
    dataframe = pd.read_excel(b)
    ftp.quit()
    return dataframe
    
ftpLogin = ranFtpCredentials()
dirList = getFtpPathFileList(ftpLogin, topWorstFilePath)
for file in dirList:
    if currentDate and "2G" and "CSSR" in file:
        current2GTopWorstCssrFile = file
    if currentDate and "2G" and "DCR" in file:
        current2GTopWorstDcrFile = file
    if currentDate and "3G" in file:
        current3GTopWorstFile = file
    if currentDate and "LTE" in file:
        current4GTopWorstFile = file

data = downloadFtpFile(ftpLogin, topWorstFilePath, current2GTopWorstCssrFile)
print(data)