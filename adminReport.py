from dotenv import load_dotenv
import os
from send_email import send_email
import sqlite3

def adminReport():
    con = sqlite3.connect("toronto.db")
    cur = con.cursor()
    query = cur.execute("SELECT totalCount, weeklyCount FROM statistics;")
    result = query.fetchone()
    
    adminList = os.getenv("ADMIN_EMAIL_ADDRESSES").split(",")
    send_email(
        subject="Admin weekly report",
        body="Weekly Searches: {0}\nTotal Searches: {1}".format(result[1], result[0]),
        recipients=adminList,
        email_account=os.getenv("SENDER_EMAIL"),
        email_password=os.getenv("SENDER_PASSWORD"),
        email_server=os.getenv("SENDER_SERVER"),
        email_server_port_number=os.getenv("SENDER_PORT"),
    )
    
if __name__ == "__main__":
    adminReport()