# Toronto Housing Co-op Web Scraper

This program checks the availability of available co-ops [here](https://co-ophousingtoronto.coop/resources/find-a-coop/).

## How to use

1. Create a txt file named _email_addresses.txt_, and populate it with the desired email addresses to send notifications to, each on a newline.
1. Create a file named _counter.txt_ and fill the first 2 lines with 0.
   Ex:
   ```
   0
   0
   ```
1. In the _server.py_ file, edit the _admin_email_ to your email.
1. In the _send_email.py_, edit and replace my email with your own, so that emails are correctly send from your own email address.
1. Create a virtual env with `python -m venv <venv>` where _<venv>_ is the name of the virtual environment.
1. Install requirements with `pip install -r requirements.txt`.
1. On linux, start the server with `./instance start`. To stop, use `./instance stop`.
1. If on windows, must use process in the terminal. Start with `python ./server.py`.
1. Emails will be sent whenever a co-op availability is found, and weekly results will be sent on Sundays to admins.
