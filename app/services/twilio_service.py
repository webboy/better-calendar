import time
from typing import List
from twilio.rest import Client
from dotenv import load_dotenv
import os
import logging
from twilio.rest.api.v2010.account.message import MessageInstance


class TwilioService:
    MESSAGE_LIMIT = 1500  # Twilio's character limit per message

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

    def _segment_message(self, message_text: str) -> List[str]:
        """Split message into segments if it exceeds the character limit"""
        if len(message_text) <= self.MESSAGE_LIMIT:
            return [message_text]

        segments = []
        remaining_text = message_text

        while remaining_text:
            # Find the last space within the limit to avoid breaking words
            if len(remaining_text) > self.MESSAGE_LIMIT:
                split_index = remaining_text.rfind(' ', 0, self.MESSAGE_LIMIT)
                if split_index == -1:  # No space found, force split at limit
                    split_index = self.MESSAGE_LIMIT
            else:
                split_index = len(remaining_text)

            # Add segment number if there are multiple segments
            segment = remaining_text[:split_index]
            if len(message_text) > self.MESSAGE_LIMIT:
                segments.append(f"({len(segments) + 1}/{(len(message_text) - 1) // self.MESSAGE_LIMIT + 1}) {segment}")
            else:
                segments.append(segment)

            # Update remaining text
            remaining_text = remaining_text[split_index:].strip()

        return segments

    def _send_single_message(self, to: str, message_text: str) -> MessageInstance:
        """Send a single message and track its status"""
        logging.info(f"Attempting to send message to {to}")
        logging.info(f"Using sender number: {self.sender_number}")

        message = self.client.messages.create(
            to=to,
            from_=self.sender_number,
            body=message_text
        )

        logging.info(f"Message sent. SID: {message.sid}")
        logging.info(f"Initial status: {message.status}")

        # Track message status for a few seconds
        for _ in range(5):  # Check status 5 times
            updated_message = self.client.messages(message.sid).fetch()
            logging.info(f"Updated status: {updated_message.status}")

            if updated_message.status == 'delivered':
                break
            if updated_message.error_code:
                logging.error(f"Error code: {updated_message.error_code}")
                logging.error(f"Error message: {updated_message.error_message}")
                break
            time.sleep(2)  # Wait 2 seconds between checks

        return message

    def send(self, to: str, message_text: str) -> List[MessageInstance]:
        """
        Send message, automatically splitting into segments if needed

        Args:
            to: Recipient phone number
            message_text: Message content

        Returns:
            List of MessageInstance objects (one per segment)
        """
        try:
            messages = []
            segments = self._segment_message(message_text)

            for segment in segments:
                message = self._send_single_message(to, segment)
                messages.append(message)
                if len(segments) > 1:
                    time.sleep(1)  # Brief pause between segments

            return messages
        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            raise