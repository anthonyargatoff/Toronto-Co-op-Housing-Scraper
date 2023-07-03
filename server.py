import time
from scraping import *
from send_email import *

starttime = time.time()
recipients = ["anthonyargatoff@gmail.com", "mrkoolpants@gmail.com", "emily.denison3@gmail.com"]
time_interval = int(input("Enter search frequency in minutes:"))
print("Server is running with frequency of {} minutes. Press 'q' to quit.".format(time_interval))

while True:
    time.sleep((time_interval * 60 ) - ((time.time() - starttime) % (60 *time_interval)))
    coop_bool, coop_string = get_vacancies()
    if (coop_bool):
        body = "One or more coops are available. View below:\n{}View the website here: https://co-ophousingtoronto.coop/resources/find-a-coop/".format(
            coop_string)
        send_email("Coop Available!", body, recipients)
        print("Co-op vacancy found. Sending email to {}.\nNext Update in 12 hours\n".format(recipients))
        time.sleep(43200)
    else:
        print("No co-op vacancies found. Next search in {} minutes.".format(time_interval))
    
