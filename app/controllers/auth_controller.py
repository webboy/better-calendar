from typing import List
from app.services.user_service import UserService
from app.services.validation_service import ValidationService
from app.services.email_service import EmailService


class AuthController:

    def __init__(self):
        self.user_service = UserService()
        self.validation_service = ValidationService()
        self.email_service = EmailService()

    def register(self, args: List[str], wa_id: str, phone_number: str) -> str:
        email = args[0]

        # Validate email
        if not self.validation_service.validate_email(email):
            return f"""❌ Invalid Email Format
Please provide a valid email address.
Example: student@masterschool.com"""

        # Check if the email is in the user list
        user = self.user_service.get_user_by_email(email)

        # Generate a code
        code = self.user_service.generate_validation_code()

        # Save the validation code to the DB
        self.user_service.set_validation_code(email, code)

        # Send the code to the user via email
        self.email_service.send_email(user.email,'Better Calendar Verification Code',f'Your verification code is: {code}')

        return f"""👋 Hello {user.first_name}!

📧 We've sent a verification code to:
   {email}
To complete registration, use:
!validate {email} <code>"""

    def validate(self, args: List[str], wa_id: str, phone_number: str) -> str:
        email = args[0]
        code = args[1]

        # Validate email
        if not self.validation_service.validate_email(email):
            return f"""❌ Invalid Email Format
Please provide a valid email address.
Example: student@masterschool.com"""

        # Check if the email is in the user list
        user = self.user_service.get_user_by_email(email)

        # Check if the code is valid
        if user.validation_code != code:
            return f"""❌ Invalid Verification Code

The code you provided doesn't match our records.
Please check the code and try again.

Email: {email}
Provided Code: {code}"""

        # Save the wa_id and phone_number to the DB against the email
        self.user_service.link_whatsapp(email, wa_id, phone_number)

        return f"""✅ Registration Complete!

Welcome {user.first_name}! Your WhatsApp number has been successfully linked to your account.

You can now use all available commands.
Send !help to see what you can do."""