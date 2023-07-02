import time
from scraping import *
from send_email import *

starttime = time.time()
recipients = ["anthonyargatoff@gmail.com", "mrkoolpants@gmail.com"]
print("Server is running.")

while True:
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    coop_bool, coop_string = get_vacancies()

    if (coop_bool):
        body = "One or more coops are available. View below:\n{}".format(
            coop_string)
        send_email("Coop Available!", coop_string, recipients)
