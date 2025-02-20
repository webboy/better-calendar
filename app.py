from flask import Flask, request, render_template_string
import logging
from datetime import datetime
from app.services.router_service import RouterService
from app.services.twilio_service import TwilioService
from app.services.user_service import UserService
from app.services.validation_service import ValidationService
from app.routes.routes import configure_routes

# services
twilio = TwilioService()
user_service = UserService()
validation_service = ValidationService()

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

# HTML template for verification response
VERIFY_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>What's Academy Better Calendar - Email Verification</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            text-align: center;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .success {
            color: #2ecc71;
            font-size: 64px;
            margin: 0;
        }
        .error {
            color: #e74c3c;
            font-size: 64px;
            margin: 0;
        }
        h1 {
            color: #2c3e50;
            margin-top: 10px;
        }
        p {
            color: #666;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        {% if success %}
            <div class="success">✓</div>
            <h1>Verification Successful!</h1>
            <p>Welcome {{ name }}! Your email has been verified.</p>
            <p>You can now close this window and continue using Better Calendar in WhatsApp.</p>
        {% else %}
            <div class="error">✕</div>
            <h1>Verification Failed</h1>
            <p>{{ error_message }}</p>
            <p>Please try again or contact support if the problem persists.</p>
        {% endif %}
    </div>
</body>
</html>
"""

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

@app.route('/verify', methods=['GET'])
def verify():
    # Get verification parameters
    email = request.args.get('email', '')
    code = request.args.get('code', '')

    # Log verification attempt
    logging.info(f"Verification attempt for email: {email}")

    try:
        # Validate email format
        if not validation_service.validate_email(email):
            return render_template_string(
                VERIFY_TEMPLATE,
                success=False,
                error_message="Invalid email format."
            )

        # Get user and verify code
        user = user_service.get_user_by_email(email)
        if not user:
            return render_template_string(
                VERIFY_TEMPLATE,
                success=False,
                error_message="Email not found."
            )

        if user.validation_code != code:
            return render_template_string(
                VERIFY_TEMPLATE,
                success=False,
                error_message="Invalid verification code."
            )

        # If we have a WhatsApp ID stored, complete the verification
        if user.wa_id:
            user_service.link_whatsapp(email, user.wa_id, user.phone_number)

        # Send success message through Twilio
        twilio.send(user.phone_number, "🎉 Your email has been verified! You can now use Better Calendar in WhatsApp.")

        return render_template_string(
            VERIFY_TEMPLATE,
            success=True,
            name=user.first_name
        )

    except Exception as e:
        logging.error(f"Error during verification: {str(e)}")
        return render_template_string(
            VERIFY_TEMPLATE,
            success=False,
            error_message="An error occurred during verification. Please try again."
        )

if __name__ == '__main__':
    app.run(debug=True)