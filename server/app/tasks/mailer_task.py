from app.core.config import settings
from app.core.settings import celery_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@celery_app.task(name="tasks.mailer_task.send_otp_email")
def send_otp_email(receiver: str, otp: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = settings.EMAIL_HOST
        msg["To"] = receiver
        msg["Subject"] = "Your OTP Code"

        body = f"Hello,\n\nYour OTP code is: {otp}\n\nThis code will expire in 5 minutes."
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587) 
        server.starttls()
        server.login(settings.EMAIL_HOST, settings.APP_PASSWORD)
        server.sendmail(settings.EMAIL_HOST, receiver, msg.as_string())
        server.quit()

        return {"status": "success", "message": "Email sent"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}
