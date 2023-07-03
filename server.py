import time
from scraping import *
from send_email import *

def get_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

starttime = time.time()
recipients = ["anthonyargatoff@gmail.com", "mrkoolpants@gmail.com", "emily.denison3@gmail.com"]
time_interval = float(input("Enter search frequency in minutes:"))
print("Server is running with frequency of {:.0f} minutes.".format(time_interval))


while True:
    coop_bool, coop_string = get_vacancies()
    if (coop_bool):
        body = "One or more coops are available. View below:\n{}View the website here: https://co-ophousingtoronto.coop/resources/find-a-coop/".format(
            coop_string)
        send_email("Coop Available!", body, recipients)
        print("System Time: {}. Co-op vacancy found. Sending email to {}. Next Update in 12 hours\n".format(get_time(), recipients))
        time.sleep(43200)
    else:
        print("System Time: {}. No co-op vacancies found. Next search in {:.0f} minutes.".format(get_time(), time_interval))
    time.sleep((time_interval * 60 ) - ((time.time() - starttime) % (60 *time_interval)))
    
