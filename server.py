import time
from datetime import datetime
from scraping import *
from send_email import *

def get_time():
    """
    Gets full date in yyyy/mm/dd hh:mm format

    Returns:
        _type_: string
    """    
    now = datetime.now()
    current_time = now.strftime("Date: %Y/%m/%d Time: %H:%M")
    return current_time

def get_week_day():
    """
    Gets the Day of the week in a string

    Returns:
        _type_: string
    """    
    now = datetime.now()
    week_day = now.strftime("%A")
    return week_day

def check_time():
    """
    Return the time in 24 hour clock format of %H

    Returns:
        _type_: int
    """    
    now = datetime.now()
    check_time = now.strftime("%-H")
    check_time = int(check_time)
    return check_time

def get_email(x):
    """
    Create a list of emails from the email_addresses.txt file

    Args:
        x (_type_): list of strings
    """     
    email_file = open("./email_addresses.txt", "r")
    for email in email_file:
        if email.startswith("#"):
         None
        else:
            email = email.replace("\n", "")
            x.append(email)
    email_file.close()
    
def write_log(message):
    """
    For writing log files and printing to terminal

    Args:
        message (_type_): string
    """    
    file = open("log.txt", "a")
    file.write(message + "\n")
    print(message)
    file.close

recipients = []
get_email(recipients)
times_checked_weekly = 0

open_total_times = open("./total_times_checked.txt", "r" )
times_checked_total = int(open_total_times.read())
open_total_times.close()

negative_results = 0
positive_results = 0
check_sent_admin_email = False

starttime = time.time()
time_interval = float(input("Enter search frequency in minutes:"))
print("Server is running with frequency of {:.0f} minutes.".format(time_interval))

while True:
    coop_bool, coop_string = get_vacancies()    
    
    if ( get_week_day() == "Sunday" and check_time() >= 9 and check_sent_admin_email == False):
        
        times_checked_total += times_checked_weekly
        admin_body = "Here is the weekly report:\nInterval of search: {} minutes\nTimes searched this week: {}\nTotal times searched: {}\nCo-op vacancies found this week: {}\nNo co-op vacancies found this week: {}\nSent at {} PST".format(time_interval, times_checked_weekly, times_checked_total, positive_results, negative_results, get_time())
        send_email("Toronto Co-op Housing Search: Weekly Report", admin_body, recipients)
        check_sent_admin_email = True
        
        open_total_times = open("total_times_checked.txt", "w")
        open_total_times.write(times_checked_total)
        open_total_times.close        
        negative_results, positive_results, times_checked_weekly = 0
        
        write_log("Weekly report sent at {}".format(get_time()))
    
    if( check_sent_admin_email == True and get_week_day() != "Sunday"):
        
        check_sent_admin_email = False
        write_log("Admin boolean set to false at {}".format(get_time()))
        
    if (coop_bool):
        
        body = "One or more coops are available. View below:\n{}View the website here: https://co-ophousingtoronto.coop/resources/find-a-coop/".format(
            coop_string)
        send_email("Toronto Co-op Housing Search: Coop Available!", body, recipients)
        write_log("System Time: {}. Co-op vacancy found. Sending email to {}. Next Update in 12 hours\n".format(get_time(), recipients))

        positive_results += 1
        times_checked_weekly += 1
        time.sleep(43200)
    else:
        
        write_log("System: {}. No co-op vacancies found. Next search in {:.0f} minutes.".format(get_time(), time_interval))
        times_checked_weekly += 1
        negative_results += 1
        time.sleep((time_interval * 60 ) - ((time.time() - starttime) % (60 *time_interval)))
    
