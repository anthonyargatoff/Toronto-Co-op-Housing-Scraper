import smtplib
from email.mime.text import MIMEText


def send_email(subject:str, body:str, recipients:list[str], email_account:str, email_password:str, email_server:str, email_server_port_number:int):
    """
    _summary_ Sends an email with google email.

    Args:
        subject (str): The subject line of the email.
        body (str): The email body.
        recipients (list[str]): Recipients of email.
        email_account (str): Account the email is sent from.
        email_password (str): Password for the sender email account. 
        email_server (str): The SMTP server name (probably google SMTP servers).
        email_server_port_number (int): The port number of the SMTP server.
    """      
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_account
    msg['To'] = ', '.join(recipients) if len(recipients) > 1 else recipients[0]
    with smtplib.SMTP_SSL(email_server, email_server_port_number) as smtp_server:
        smtp_server.login(email_account, email_password)
        smtp_server.sendmail(email_account,
                             recipients, msg.as_string())