import time
from datetime import datetime
from scraping import *
from send_email import *

def create_txt_files():
    """
    Creates required text files
    """    
    file1 = open('log.txt', 'r+')
    file1.close()
    file2 = open('email_addresses.txt', 'r+')
    file2.close()
    file3 = open('counter.txt', 'r+')
    file3.close()

def get_time():
    """
    Gets full date in yyyy/mm/dd hh:mm format

    Returns:
        Strings: YYYY/MM/DD HH:MM
    """    
    now = datetime.now()
    current_time = now.strftime("Date: %Y/%m/%d Time: %H:%M")
    return current_time

def get_week_day():
    """
    Gets the Day of the week in a string

    Returns:
        String: Returns full weekday name
    """    
    now = datetime.now()
    week_day = now.strftime("%A")
    return week_day

def check_time():
    """
    Return the time in 24 hour clock format of %H

    Returns:
        Int: Returns int of current time
    """    
    now = datetime.now()
    check_time = now.strftime("%-H")
    check_time = int(check_time)
    return check_time

def get_email(email_text_file):
    """
    Create a list of emails from the email_addresses.txt file

    Args:
        x (list[str]): List of emails addresses.
        
    Returns:
        List[str]: Returns a list of strings with emails from text file.
    """     
    email_file = open(email_text_file, "r")
    email_list = []
    for email in email_file:
        if email.startswith("#"):
         None
        else:
            email = email.replace("\n", "")
            email_list.append(email)
    email_file.close()
    return email_list
    
def write_log(message):
    """
    For writing log files and printing to terminal

    Args:
        message (String): Prints to terminal and log.txt
    """    
    file = open("log.txt", "a")
    file.write(message + "\n")
    print(message)
    file.close

def edit_counter(total, total_positive, total_negative):
    """
    Adds the new totals to the counter.txt file

    Args:
        total (int): Total counts
        total_positive (int): total positive counts
        total_negative (int): total negative counts
    """    
    with open("./counter.txt", 'r') as f:
        lines = f.readlines()
        f.close()
    
    lines[0], lines[1], lines[2] = (str(total) + "\n"), (str(total_positive) + "\n"), (str(total_negative) + "\n") 
    
    with open("./counter.txt", "w") as f:
        f.writelines(lines)
        f.close()
    
create_txt_files()
recipients = get_email("./email_addresses.txt")
admin_email = "anthonyargatoff@gmail.com"

print(recipients)

open_counter = open("./counter.txt", "r" )
counter = open_counter.readlines()
total_times_checked = int(counter[0])
total_negative_results = int(counter[2])
total_positive_results = int(counter[1])
open_counter.close()

times_checked_weekly = 0
weekly_positive_results = 0
weekly_negative_results = 0
check_sent_admin_email = False

starttime = time.time()
time_interval = float(input("Enter search frequency in minutes:"))
print("Server is running with frequency of {:.0f} minutes.".format(time_interval))

while True:
    coop_bool, coop_string = get_vacancies()    
    
    if ( get_week_day() == "Sunday" and check_time() >= 9 and check_sent_admin_email == False):
        
        recipients = get_email("./email_addresses") # updates email list every week.
        
        total_times_checked += times_checked_weekly
        total_negative_results += weekly_negative_results
        total_positive_results += weekly_positive_results
        
        admin_body = "Here is the weekly report:\nInterval of search: {} minutes\nTimes searched this week: {}\nCo-op vacancies found this week: {}\nNo co-op vacancies found this week: {}\nTotal amount of co-ops found: {}\nTotal amount of co-ops not found: {}\nTotal times searched: {}\nPercentage of co-ops found: {}%\nSent at {} PST".format(time_interval, times_checked_weekly, weekly_positive_results, weekly_negative_results, total_positive_results, total_negative_results, total_times_checked, total_positive_results/total_times_checked, get_time())
        send_email("Toronto Co-op Housing Search: Weekly Report", admin_body, recipients)
        check_sent_admin_email = True

        edit_counter(total_times_checked, total_positive_results, total_negative_results)
        weekly_negative_results, weekly_positive_results, times_checked_weekly = 0
        
        write_log("Weekly report sent at {}".format(get_time()))
        send_email("Toronto Co-op Housing Search: Admin Report", get_test_results(), admin_email)
        write_log("Sent admin email at {}".format(get_time()))
    
    if( check_sent_admin_email == True and get_week_day() != "Sunday"):
        
        check_sent_admin_email = False
        write_log("Admin boolean set to false at {}".format(get_time()))
        
    if (coop_bool):
        
        body = "One or more coops are available. View below:\n{}View the website here: https://co-ophousingtoronto.coop/resources/find-a-coop/".format(
            coop_string)
        send_email("Toronto Co-op Housing Search: Coop Available!", body, recipients)
        write_log("System Time: {}. Co-op vacancy found. Sending email to {}. Next Update in 12 hours\n".format(get_time(), recipients))

        weekly_positive_results += 1
        times_checked_weekly += 1
        time.sleep(43200)
    else:
        
        write_log("System: {}. No co-op vacancies found. Next search in {:.0f} minutes.".format(get_time(), time_interval))
        times_checked_weekly += 1
        weekly_negative_results += 1
        time.sleep((time_interval * 60 ) - ((time.time() - starttime) % (60 *time_interval)))
    
