from twilio.rest import Client


class TwilioService:
    def __init__(self):
        self.account_sid = "AC19d45fb931ecd5fd0a686e635796e508"
        self.auth_token = "9921bca9e615ac5ee449f73b8503e6c8"
        self.client = Client(self.account_sid, self.auth_token)

    def send(self, to, message):
        message = self.client.messages.create(to=to, from_="whatsapp:+14155238886", body=message)

        return message