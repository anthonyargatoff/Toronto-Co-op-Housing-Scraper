import smtplib
from email.mime.text import MIMEText


def send_email(subject:str, body:str, recipients:list[str]):
    """
    Sends an email with subject, body and recipients

    Args:
        subject (string): Email subject
        body (string): Email body
        recipients (list[str]): A list of email addresses to be sent to.
    """    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "autoanthonyemailer@gmail.com"
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login("autoanthonyemailer@gmail.com", "fivbeibqffhhaxbz")
        smtp_server.sendmail("autoanthonyemailer@gmail.com",
                             recipients, msg.as_string())