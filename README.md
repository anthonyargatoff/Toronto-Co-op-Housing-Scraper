# Toronto Housing Co-op Web Scraper

This program checks the availability of available co-ops [here](https://co-ophousingtoronto.coop/resources/find-a-coop/) and will send email notifications to the recipients when a housing unit has an availabilty. It by default runs every 10 minutes, but can be edited in the code (main.py).

## How to use

1. Clone the repository onto your machine.
1. Fill out the emailAddresses.json file with the sending email information, as well as recipients (clients and admin recipients). 
   Ex:
   ```json
   {
      "emailAddresses": {
         "clientEmailAddresses": [
               "test1@gmail.com",
               "test2@gmail.com"
         ],
         "adminEmailAddresses": [
               "admin1@gmail.com",
               "admin2@gmail.com"
         ]        
      },
      "senderEmailCredentials": {
         "senderEmail": "sender@gmail.com",
         "senderPassword": "password",
         "senderServer": "smtp.gmail.com",
         "senderPort": "465"
      }
   }

   ```
1. Create a file named _counter.txt_ and fill the first 2 lines with 0. This is used for counting the total searches.
   Ex:
   ```
   0
   0
   ```
1. Create a virtual env with `python -m venv <venv>` where _<venv>_ is the name of the virtual environment.
1. Install requirements with `pip install -r requirements.txt`.
1. On linux, start the server with `./instance start`. To stop, use `./instance stop`.
1. If on windows, must use process in the terminal. Start with `python ./server.py`.
2. Emails will be sent whenever a co-op availability is found, and weekly results will be sent on Sundays to admins.
