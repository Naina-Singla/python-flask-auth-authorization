import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()


SMTP_SERVER = "smtp.gmail.com"    
SMTP_PORT = 587
EMAIL = os.getenv("MY_EMAIL")       
PASSWORD = os.getenv("MY_EMAIL_PWD")


def send_mail(to_address, subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)
    print("Mail sent!")


