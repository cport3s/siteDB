import os
import csv
from datetime import datetime
import pandas as pd

topWorstFilePath = "D:\\ftproot\\BSC\\top_worst_report\\"
current2GTopWorstDcrFile = ""
current2GTopWorstCssrFile = ""
current3GTopWorstFile = ""
current4GTopWorstFile = ""
topWorstCurrentDate = datetime.now().strftime("%Y%m%d")

for file in os.listdir(topWorstFilePath):
    if topWorstCurrentDate and "2G" and "CSSR" in file:
        current2GTopWorstCssrFile = file
    if topWorstCurrentDate and "2G" and "DCR" in file:
        current2GTopWorstDcrFile = file
    if topWorstCurrentDate and "3G" in file:
        current3GTopWorstFile = file
    if topWorstCurrentDate and "LTE" in file:
        current4GTopWorstFile = file
current3GTopWorstDataframe = pd.read_excel(topWorstFilePath + current3GTopWorstFile, index_col='Cell Name')
print(current3GTopWorstDataframe['HSDPA CSSR(%)'].nsmallest(10))