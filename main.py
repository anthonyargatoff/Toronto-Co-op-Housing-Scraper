import schedule
import time
from compareVacancies import compareVacancies
from adminReport import adminReport
    
schedule.every(1).minutes.do(compareVacancies)
schedule.every().sunday.at("08:00").do(adminReport)

while True:
    schedule.run_pending()
    time.sleep(1)