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

    # Log specific message details
    logging.info(f"Message: {incoming_msg}")
    logging.info(f"WA ID: {wa_id}")
    logging.info(f"Phone: {phone_number}")

    # Get response from the router
    try:
        response = router.route(incoming_msg, wa_id, phone_number)

        # Logging
        logging.info(f"Response: {response}")

        # Send response string back to the user
        twilio.send(phone_number, response)

        return str(response)

    except Exception as e:
        twilio.send(phone_number, 'Error. Please try later.')


if __name__ == '__main__':
    app.run(debug=True)