import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

class EmailService:
    def __init__(self):
        load_dotenv()
        self.smtp_server = "smtp.zoho.eu"
        self.smtp_port = 465
        self.email = os.getenv("SMTP_EMAIL")
        self.password = os.getenv("SMTP_PASSWORD")

    def send_email(self, recipient_email, subject, body):
        global server
        msg = MIMEMultipart()
        msg["From"] = self.email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)  # Use SMTP_SSL for port 465
            server.login(self.email, self.password)
            server.sendmail(self.email, recipient_email, msg.as_string())

        except Exception as e:
            raise Exception(f"Error sending email: {str(e)}")
        finally:
            server.quit()


