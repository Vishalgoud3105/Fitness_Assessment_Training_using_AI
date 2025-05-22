import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from templates.email_types import email_templates

def send_custom_email(name, recipient_email, tone, prompt_key):
    sender_email = "your_email@example.com"
    sender_password = "your_app_password"  # Use app password, not your real Gmail password

    subject = f"🏋️ Fitness Report for {name}"
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email

    # Get the selected email template
    html_content = email_templates[tone][prompt_key].format(Name=name)
    part = MIMEText(html_content, "html")
    message.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
    except Exception as e:
        raise RuntimeError(f"Email failed to send: {e}")
