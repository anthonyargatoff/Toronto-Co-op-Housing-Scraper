import smtplib
from email.mime.text import MIMEText


def send_email(subject, body, recipients):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login("autoanthonyemailer@gmail.com", "fivbeibqffhhaxbz")
        smtp_server.sendmail("autoanthonyemailer@gmail.com",
                             recipients, msg.as_string())
    print("Message sent to {}!".format(recipients))
