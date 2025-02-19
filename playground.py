from app.services.twilio_service import TwilioService
import logging


# Set up logging
logging.basicConfig(
    filename=f"logs\\log-playground.log",
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

twilio_service = TwilioService()



def send_message(to: str, message: str):
    result = twilio_service.send(to, message)
    logging.info(f"Message result: {result}")



send_message("whatsapp:+491724184069", "Hello, World!")

