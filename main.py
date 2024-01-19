#! ~/furlong_co-op_scraping/furlong/bin/python3

import time
from datetime import datetime
from scraping import *
from send_email import *
import json

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
    check_time = now.strftime("%H")
    check_time = int(check_time)
    return check_time

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


def sum_counter(add_total: int, add_weekly: int, text_file):
    """
    Sums the entered args with the current values in counter.text file.

    Args:
        add (int): New value to add to the counter. add_total is the first line, add_weekly is the second line in the counter.txt file. 
    """
    with open(text_file, 'r') as f:
        lines_from_file = f.readlines()
        f.close()

    lines_list = []
    for line in lines_from_file:
        line = line.replace("\n", "")
        lines_list.append(line)

    line_list_int = []
    for lines in lines_list:
        line_list_int.append(int(lines))

    to_add = [add_total, add_weekly]

    for i in range(len(line_list_int)):
        line_list_int[i] += to_add[i]

    lines_list = []
    for line_int in line_list_int:  # change back to string
        lines_list.append(str(line_int) + "\n")

    with open("./counter.txt", "w") as f:
        f.writelines(lines_list)
        f.close()


def get_counter(text_file):
    """
    Gets the values from the counter.txt file.

    Args:
        text_file (txt file): Test file.
    Returns:
        int: The integer values read from the text file. 1 is weekly total, 2 is overall total.
    """
    with open(text_file, 'r') as f:
        lines_from_file = f.readlines()
        f.close()

    lines_list = []
    for line in lines_from_file:
        line = line.replace("\n", "")
        lines_list.append(line)

    line_list_int = []
    for lines in lines_list:
        line_list_int.append(int(lines))

    return line_list_int[0], line_list_int[1]


def edit_counter(top_line, bottom_line, text_file):
    """
    Edits the "./counter.txt" file.

    Args:
        top_line (any): Set to an int, or "None" for no change.
        bottom_line (any): Int input, changes second line (weekly counter)
        text_file (.txt file): counter.txt file.
    """
    with open(text_file, 'r') as f:
        lines_from_file = f.readlines()
        f.close()

    lines_list = []
    for line in lines_from_file:
        line = line.replace("\n", "")
        lines_list.append(line)

    line_list_int = []
    for lines in lines_list:
        line_list_int.append(int(lines))

    if (top_line == None):
        line_list_int[1] = bottom_line
    else:
        line_list_int[0], line_list_int[1] = top_line, bottom_line

    lines_list = []
    for line_int in line_list_int:  # change back to string
        lines_list.append(str(line_int) + "\n")

    with open("./counter.txt", "w") as f:
        f.writelines(lines_list)
        f.close()


def wait_time(time_to_wait: float):
    """
    Enter time that program will sleep for, in minutes.

    Args:
        time_to_wait (float): Enter the time in minutes
    """
    time.sleep((time_to_wait * 60) -
               ((time.time() - start_time) % (60 * time_to_wait)))


f = open('emailAddresses.json')
data = json.load(f)

# Create a list of emails from json file
emailList = []
for i in data['emailAddresses']['clientEmailAddresses']:
    emailList.append(i)

# Assign the admin emailer
admin_email = []
for i in data['emailAddresses']['adminEmailAddresses']:
    admin_email.append(i)

# Assign sender email info
sender_email_address = data['senderEmailCredentials']['senderEmail']
sender_email_password = data['senderEmailCredentials']['senderPassword']
sender_email_server = data['senderEmailCredentials']['senderServer']
sender_email_port = data['senderEmailCredentials']['senderPort']

f.close()

check_sent_admin_email = False
coop_test = None
weekly_total = int()
total = int()

start_time = time.time()
time_interval = 10  # float(input("Enter search frequency in minutes:"))
print("Server is running with frequency of {:.0f} minutes.".format(
    time_interval))

while True:
    try:
        coop_bool, coop_string = get_vacancies()

        if (get_week_day() == "Sunday" and check_time() >= 9 and check_sent_admin_email == False):

            sum_counter(get_counter("counter.txt")[1], 0, "./counter.txt")
            weekly_admin_body = "Here is the weekly report:\nTotal searches this week: {}\nTotal searches: {}\nSent at {} PST".format(
                get_counter("./counter.txt")[1], get_counter("./counter.txt")[0], get_time())
            check_sent_admin_email = True
            send_email("Toronto Co-op Housing Search: Admin Report",
                       weekly_admin_body + "\n" + "\n" + get_test_results(), admin_email, sender_email_address, sender_email_password, sender_email_server, sender_email_port)
            write_log("Sent admin email at {} to {}".format(
                get_time(), admin_email))
            edit_counter(None, 0, "./counter.txt")

        if (check_sent_admin_email == True and get_week_day() != "Sunday"):

            check_sent_admin_email = False
            write_log("Admin boolean set to false at {}".format(get_time()))

        if (coop_bool):

            if (coop_string == coop_test):
                write_log(
                    "System: {}. Co-ops are available, but no new co-ops were found. Next search in {:.0f} minutes.".format(get_time(), time_interval))
                sum_counter(0, 1, "./counter.txt")
                wait_time(time_interval)

            else:
                coop_test = coop_string
                email_body_cp_avail = "One or more co-ops are available. View below:\n{}View the website here: https://co-ophousingtoronto.coop/resources/find-a-coop/".format(
                    coop_string)
                send_email(
                    "Toronto Co-op Housing Search: Coop Available!", email_body_cp_avail, emailList, sender_email_address, sender_email_password, sender_email_server, sender_email_port)
                write_log(
                    "System: {}. Co-op vacancy found. Sending email to {}. Next search in {:.0f} minutes.".format(get_time(), emailList, time_interval))
                sum_counter(0, 1, "./counter.txt")
                wait_time(time_interval)

        else:
            coop_test = None
            write_log(
                "System: {}. No co-op vacancies found. Next search in {:.0f} minutes.".format(get_time(), time_interval))
            sum_counter(0, 1, "./counter.txt")
            wait_time(time_interval)

    except Exception as error:
        print("Error {} occurred at {}. Next search attempt in {} minutes.".format(
            error, get_time(), time_interval))
        wait_time(time_interval)
