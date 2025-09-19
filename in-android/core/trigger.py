import smtplib
import socket
import platform
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config


class MailTrigger:
    def __init__(self):
        self.app_password = config("APP_PASSWORD", default=None)
        self.email_host = config("EMAIL_HOST", default=None)
        self.email_receiver = config("EMAIL_RECEIVER", default=None)
        if not all([self.app_password, self.email_host, self.email_receiver]):
            raise ValueError("Missing environment variables for email configuration")

    def _get_system_details(self) -> str:
        try:
            details = {
                "Hostname": socket.gethostname(),
                "Local IP": socket.gethostbyname(socket.gethostname()),
                "Platform": platform.system(),
                "Platform Release": platform.release(),
                "Platform Version": platform.version(),
                "Architecture": platform.machine(),
                "Processor": platform.processor(),
                "Python Version": platform.python_version(),
                "Node": platform.node(),
            }
            return "\n".join(f"{k}: {v}" for k, v in details.items())
        except Exception as e:
            return f"Could not fetch system details: {e}"

    def send_app_opened_alert(self):
        subject = "Alert Mail: Black Channel Application Opened"
        body = (
            "Black Channel Mobile Application was just opened.\n\n"
            "===== System Details =====\n"
            f"{self._get_system_details()}"
        )

        msg = MIMEMultipart()
        msg["From"] = self.email_host
        msg["To"] = self.email_receiver
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.email_host, self.app_password)
                server.sendmail(self.email_host, self.email_receiver, msg.as_string())
            print("[INFO] Alert email sent successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
