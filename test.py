from ftplib import FTP
from io import BytesIO
import pandas as pd

class ranFtpCredentials():
    hostname = 'bscserver'
    username = 'sitedb'
    password = 'BSCAltice.123'

topWorstFilePath = '/BSC/'
fileName = 'testExcel.xlsx'

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
data = downloadFtpFile(ftpLogin, topWorstFilePath, fileName)
print(data)