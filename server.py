import time
from scraping import *
from send_email import *
import keyboard

starttime = time.time()
recipients = ["anthonyargatoff@gmail.com", "mrkoolpants@gmail.com", "emily.denison3@gmail.com"]
print("Server is running. Press 'q' to quit.")
time_interval = 60 # time is in seconds

while True:
    time.sleep(time_interval - ((time.time() - starttime) % time_interval))
    coop_bool, coop_string = get_vacancies()
    if (coop_bool):
        body = "One or more coops are available. View below:\n{}View the website here: https://co-ophousingtoronto.coop/resources/find-a-coop/".format(
            coop_string)
        send_email("Coop Available!", body, recipients)
    else:
        print("No co-op vacancies found. Time next search in {} seconds.".format(time_interval))
    
