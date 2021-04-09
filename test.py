from ftplib import FTP
class ftpCredentials():
    hostname = 'bscserver'
    username = 'sitedb'
    password = 'BSCAltice.123'
    topWorstFilePath = '/BSC/top_worst_report/'

ftpLogin = ftpCredentials()
# Instantiate FTP connection
ftp = FTP(host=ftpLogin.hostname)
ftp.login(user=ftpLogin.username, passwd=ftpLogin.password)
# Move to desired path
ftp.cwd(ftpLogin.topWorstFilePath)
print(ftp.pwd())
ftp.quit()