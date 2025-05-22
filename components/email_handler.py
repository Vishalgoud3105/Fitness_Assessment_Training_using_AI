# components/email_handler.py — Enhanced Email Personalization

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from templates.email_types import email_templates

def send_custom_email(name, recipient_email, tone, prompt_key, performance, ideal):
    sender_email = "tony17stark07@gmail.com"
    sender_password = "fpqv delg ppwn impl"

    subject = f"🏋️ Fitness Report for {name}"
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email

    # Performance summary logic
    delta = performance - ideal
    if delta > 0:
        extra = f"🔥 You performed {abs(delta):.1f} above the ideal!"
    elif delta < 0:
        extra = f"✨ You're just {abs(delta):.1f} away from the ideal. Keep going!"
    else:
        extra = f"🎯 You hit the ideal target exactly!"

    # Build email content
    template = email_templates[tone][prompt_key]
    html_content = template.format(Name=name, Performance=f"{performance:.1f}", Encouragement=extra)

    message.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
    except Exception as e:
        raise RuntimeError(f"Email failed to send: {e}")
