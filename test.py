#import os
#from datetime import datetime
#
#ranReportFilepath = "D:\\ftproot\\BSC\\ran_report\\"
#for file in os.listdir(ranReportFilepath):
#    print(file)
#    currentDateTime = str(datetime.now().strftime('%Y%m%d%H%M'))
#    if int(currentDateTime[-2:]) < 30:
#        currentDateTime = str(int(currentDateTime[:-2]) - 1)
#    else:
#        currentDateTime = currentDateTime[:-2]
#    if currentDateTime in file:
#        latestRanReport = ranReportFilepath + file
#        print(latestRanReport)