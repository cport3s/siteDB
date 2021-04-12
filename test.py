from ftplib import FTP
from io import StringIO, BytesIO
import pandas as pd
from datetime import datetime

class ranFtpCredentials():
    hostname = 'bscserver'
    username = 'sitedb'
    password = 'BSCAltice.123'

topWorstFilePath = '/BSC/'
fileName = 'testExcel.xlsx'
currentDate = str(datetime.now().strftime('%Y%m%d'))

def getFtpLatestFileName(ftpLogin, currentDate, filePath):
    fileName = ""
    # Instantiate FTP connection
    ftp = FTP(host=ftpLogin.hostname)
    ftp.login(user=ftpLogin.username, passwd=ftpLogin.password)
    # Move to desired path
    ftp.cwd(filePath)
    s = StringIO()
    # Return file as binary with retrbinary functon. Must send according RETR command as part of FTP protocol
    ftp.retrlines('LIST', s.write)
    fileName = str(s.getvalue())
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
fileName = getFtpLatestFileName(ftpLogin, currentDate, topWorstFilePath)
fileName = fileName.replace('              ', ' ')
fileName = fileName.replace('  ', ' ')
#fileName = fileName.split('              ')
#for line in fileName:
#    print(line)
print(fileName)