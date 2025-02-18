from twilio.rest import Client
import os

class TwilioService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.sender_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.client = Client(self.account_sid, self.auth_token)

    def send(self, to, message_text):
        message = self.client.messages.create(to=to, from_=self.sender_number, body=message_text)

        return message