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
    check_time = now.strftime("%H")
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


def edit_counter(total_to_add: int, total_positive_to_add: int, total_negative_to_add: int):
    """
    Sums the entered args with the current values in counter.text file.

    Args:
        total_to_add (int): The new total to add
        total_positive_to_add (int): Total positive occurrences
        total_negative_to_add (int): Total negative occurrences
    """
    with open("./counter.txt", 'r') as f:
        lines_from_file = f.readlines()
        f.close()

    lines_list = []
    for line in lines_from_file:
        if line.startswith("#"):
            None
        else:
            line = line.replace("\n", "")
            lines_list.append(line)

    line_list_int = []
    for lines in lines_list:
        line_list_int.append(int(lines))

    to_add = [total_to_add, total_positive_to_add, total_negative_to_add]

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
        int: The integer values read from the text file. 1 is total times checked, 2 is total times results found, 3 is total times results not found
    """
    with open(text_file, 'r') as f:
        lines_from_file = f.readlines()
        f.close()

    lines_list = []
    for line in lines_from_file:
        if line.startswith("#"):
            None
        else:
            line = line.replace("\n", "")
            lines_list.append(line)

    line_list_int = []
    for lines in lines_list:
        line_list_int.append(int(lines))

    return line_list_int[0], line_list_int[1], line_list_int[2]


def get_percentage(numerator: int, denominator: int):
    """
    Gets percentage and ensures no division by zero error.

    Args:
        numerator (int): Numerator
        denominator (int): Denominator

    Returns:
        Int: Returns result multiplied by 100
    """
    if denominator == 0:
        return 0
    else:
        return ((numerator / denominator) * 100)


def wait_time(time_to_wait: float):
    """
    Enter time that program will sleep for, in minutes.

    Args:
        time_to_wait (float): Enter the time in minutes
    """
    time.sleep((time_to_wait * 60) -
               ((time.time() - start_time) % (60 * time_to_wait)))


create_txt_files()
recipients = get_email("./email_addresses.txt")
admin_email = "anthonyargatoff@gmail.com"
check_sent_admin_email = False
coop_test = None

start_time = time.time()
time_interval = float(input("Enter search frequency in minutes:"))
print("Server is running with frequency of {:.0f} minutes.".format(
    time_interval))

while True:
    coop_bool, coop_string = get_vacancies()

    if (get_week_day() == "Sunday" and check_time() >= 9 and check_sent_admin_email == False):

        check_sent_admin_email = True
        # updates email list every week.
        recipients = get_email("./email_addresses.txt")
        total_times_checked, total_positive_results, total_negative_results = get_counter(
            "./counter.txt")
        weekly_message_body = "Here is the weekly report:\nTotal searches: {}\nInstances where a search found an available co-op: {}\nInstances where a search did not find an available co-op: {}\nPercentage of co-ops found over the times searched: {:.2f}%\nSent at {} PST".format(
            total_times_checked, total_positive_results, total_negative_results, get_percentage(total_positive_results, total_times_checked), get_time())
        send_email("Toronto Co-op Housing Search: Weekly Report",
                   weekly_message_body, recipients)
        write_log("Weekly report sent at {} to {}".format(
            get_time(), recipients))
        send_email("Toronto Co-op Housing Search: Admin Report",
                   get_test_results(), admin_email)
        write_log("Sent admin email at {} to {}".format(
            get_time(), admin_email))

    if (check_sent_admin_email == True and get_week_day() != "Sunday"):

        recipients = get_email("./email_addresses.txt")
        check_sent_admin_email = False
        write_log("Admin boolean set to false at {}".format(get_time()))

    if (coop_bool):

        if (coop_string == coop_test):
            write_log(
                "System: {}. Co-ops are available, but no new co-ops were found. Next search in {:.0f} minutes.".format(get_time(), time_interval))
            edit_counter(1, 1, 0)
            wait_time(time_interval)

        else:
            coop_test = coop_string
            body = "One or more co-ops are available. View below:\n{}View the website here: https://co-ophousingtoronto.coop/resources/find-a-coop/".format(
                coop_string)
            send_email(
                "Toronto Co-op Housing Search: Coop Available!", body, recipients)
            write_log(
                "System Time: {}. Co-op vacancy found. Sending email to {}. Next search in {:.0f} minutes.".format(get_time(), recipients, time_interval))
            edit_counter(1, 1, 0)
            wait_time(time_interval)

    else:
        coop_test = None
        write_log(
            "System: {}. No co-op vacancies found. Next search in {:.0f} minutes.".format(get_time(), time_interval))
        edit_counter(1, 0, 1)
        wait_time(time_interval)
