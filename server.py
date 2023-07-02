import time
from scraping import *
from send_email import *

starttime = time.time()
recipients = ["anthonyargatoff@gmail.com", "mrkoolpants@gmail.com", "emily.denison3@gmail.com"]
print("Server is running.")

while True:
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    coop_bool, coop_string = get_vacancies()

    if (coop_bool):
        body = "One or more coops are available. View below:\n{}View the website here: https://co-ophousingtoronto.coop/resources/find-a-coop/".format(
            coop_string)
        send_email("Coop Available!", body, recipients)
