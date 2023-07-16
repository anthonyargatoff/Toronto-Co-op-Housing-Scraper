# Toronto Housing Co-op Web Scraper
This program checks the availability of available co-ops [here](https://co-ophousingtoronto.coop/resources/find-a-coop/).

## How to use
1. Create a txt file named `email_addresses.txt`, and populate it with the desired email addresses to send notifications to, each on a newline.
1. In the *server.py* file, edit the *admin_email* to your email.
1. In the *send_email.py*, edit and replace my email with your own, so that emails are correctly send from your own email address.
2. Start with `python3 server.py` and enter the time interval.
3. Emails will be sent whenever a co-op availability is found, and weekly results will be sent on Sundays
