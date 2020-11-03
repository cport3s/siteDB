from datetime import datetime
from datetime import timedelta

daysDelta = 2

# starttime is the current date/time - daysdelta
startTime = (datetime.now() - timedelta(days=daysDelta)).strftime("%Y/%m/%d %H:%M:%S")

print(startTime)