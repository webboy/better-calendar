from flask import Flask, request
import logging
from datetime import datetime
from app.services.router_service import RouterService
from app.services.twilio_service import TwilioService
from app.routes.routes import configure_routes

# services
twilio = TwilioService()

# Routing
router = RouterService()
router = configure_routes(router)

app = Flask('Better Calendar')

# Set up logging
logging.basicConfig(
    filename=f"logs\\log-{datetime.now().strftime('%Y-%m-%d')}.log",
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


@app.route('/webhook', methods=['POST'])
def webhook():
    # Get message details
    incoming_msg = request.values.get('Body', '')
    wa_id = request.values.get('WaId', '')
    phone_number = request.values.get('From', '')
    use_twilio = request.values.get('use_twilio', 'true').lower() == 'true'

    # Log request details
    logging.info(f"Message: {incoming_msg}")
    logging.info(f"WA ID: {wa_id}")
    logging.info(f"Phone: {phone_number}")
    logging.info(f"Using Twilio: {use_twilio}")

    try:
        response = router.route(incoming_msg, wa_id, phone_number)
        logging.info(f"Response: {response}")

        # Only send via Twilio if use_twilio is True
        if use_twilio:
            twilio.send(phone_number, response)
            logging.info("Response sent via Twilio")
        else:
            logging.info("Skipping Twilio send (use_twilio=false)")

        return str(response)

    except Exception as e:
        error_message = f"""🚨 Uhh Ohh, looks like there was an error: {str(e)} """
        logging.error(f"Error occurred: {error_message}")

        if use_twilio:
            twilio.send(phone_number, error_message)

        return error_message


if __name__ == '__main__':
    app.run(debug=True)