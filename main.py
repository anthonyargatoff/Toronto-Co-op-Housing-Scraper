import schedule
import time
from compareVacancies import compareVacancies
from adminReport import adminReport
    
print("Scheduler starting")
schedule.every(10).minutes.do(compareVacancies)
schedule.every().sunday.at("08:00").do(adminReport)

while True:
    schedule.run_pending()
    time.sleep(1)