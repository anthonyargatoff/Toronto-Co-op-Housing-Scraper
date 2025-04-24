import os
from send_email import send_email
import sqlite3

def adminReport():
    con = sqlite3.connect("toronto.db")
    cur = con.cursor()
    query = cur.execute("SELECT totalCount, weeklyCount FROM statistics;")
    result = query.fetchone()
    
    cur.execute("UPDATE statistics SET weeklyCount = 0;")
    
    admin = os.getenv("ADMIN_EMAIL_ADDRESSES")
    adminList = ''
    if (admin.find(",") != -1):
        adminList = admin.split(",")
    else:
        adminList = [admin]
    
    send_email(
        subject="Admin weekly report",
        body="Weekly Searches: {0}\nTotal Searches: {1}".format(result[1], result[0]),
        recipients=adminList,
        email_account=os.getenv("SENDER_EMAIL"),
        email_password=os.getenv("SENDER_PASSWORD"),
        email_server=os.getenv("SENDER_SERVER"),
        email_server_port_number=os.getenv("SENDER_PORT"),
    )
    print("Sending admin report")
    
    con.close()
    
if __name__ == "__main__":
    adminReport()