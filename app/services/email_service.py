import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from typing import Optional


class EmailService:
    def __init__(self):
        load_dotenv()
        self.smtp_server = "smtp.zoho.eu"
        self.smtp_port = 465
        self.email = os.getenv("SMTP_EMAIL")
        self.password = os.getenv("SMTP_PASSWORD")

        # Validate credentials
        if not all([self.email, self.password]):
            raise ValueError(
                "Missing email credentials. Please ensure SMTP_EMAIL and SMTP_PASSWORD "
                "are set in your .env file"
            )

    def send_email(self, recipient_email: str, subject: str, body: str,
                   html_body: Optional[str] = None) -> None:
        """
        Send an email with both plain text and HTML versions

        Args:
            recipient_email: Recipient's email address
            subject: Email subject
            body: Plain text version of the email
            html_body: Optional HTML version of the email
        """
        # Create message container - the correct MIME type is multipart/alternative
        msg = MIMEMultipart('alternative')
        msg["From"] = self.email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Always attach the plain text version first
        msg.attach(MIMEText(body, 'plain'))

        # Attach the HTML version if provided
        # If both plain text and HTML are provided, email clients will
        # usually show the HTML version if they support it
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email, self.password)
                server.send_message(msg)
        except Exception as e:
            raise Exception(f"Error sending email: {str(e)}")