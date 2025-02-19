import time

from twilio.rest import Client
from dotenv import load_dotenv
import os
import logging

from twilio.rest.api.v2010.account.message import MessageInstance


class TwilioService:
    def __init__(self):
        load_dotenv()
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.sender_number = os.getenv('TWILIO_PHONE_NUMBER')

        # Validate credentials
        if not all([self.account_sid, self.auth_token, self.sender_number]):
            raise ValueError(
                "Missing Twilio credentials. Please ensure TWILIO_ACCOUNT_SID, "
                "TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER are set in your .env file"
            )

        # Initialize Twilio client
        self.client = Client(self.account_sid, self.auth_token)

    def send(self, to, message_text) -> MessageInstance:
        try:
            logging.info(f"Attempting to send message to {to}")
            logging.info(f"Using sender number: {self.sender_number}")

            message = self.client.messages.create(
                to=to,
                from_=self.sender_number,
                body=message_text
            )

            logging.info(f"Message sent successfully. SID: {message.sid}")
            logging.info(f"Message status: {message.status}")

            # Track message status for a few seconds
            for _ in range(5):  # Check status 5 times
                # Fetch updated message status
                updated_message = self.client.messages(message.sid).fetch()
                logging.info(f"Updated status: {updated_message.status}")
                # Check if the status is delivered
                if updated_message.status == 'delivered':
                    break
                if updated_message.error_code:
                    logging.error(f"Error code: {updated_message.error_code}")
                    logging.error(f"Error message: {updated_message.error_message}")
                    break
                time.sleep(2)  # Wait 2 seconds between checks

            logging.info(f"Message sent successfully: {message.sid}")
            return message
        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            raise