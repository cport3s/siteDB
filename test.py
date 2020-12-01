#import os
#import csv
#from datetime import datetime
#import pandas as pd
#
#ranReportFilepath = "D:\\ftproot\\BSC\\ran_report\\"
#latestRanReport = ranReportFilepath + os.listdir(ranReportFilepath)[0]
#ranReportLteTable = pd.read_excel(latestRanReport, sheet_name='4G Table')
#ranReportUmtsTable = pd.read_excel(latestRanReport, sheet_name='3G Table')
#ranReportGsmTable = pd.read_excel(latestRanReport, sheet_name='2G Table')
#print(ranReportLteTable['KPI\Object'])