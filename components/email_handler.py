#`email_handler.py`
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from templates.email_types import email_templates

def send_test_email(name, receiver_email):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"
    subject = f"Fitness Report for {name}"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    body = email_templates.format(Name=name)
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        raise RuntimeError(f"Failed to send email: {e}")