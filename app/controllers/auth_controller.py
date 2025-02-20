from typing import List
import os
from urllib.parse import quote
from app.services.user_service import UserService
from app.services.validation_service import ValidationService
from app.services.email_service import EmailService
from dotenv import load_dotenv


class AuthController:
    def __init__(self):
        load_dotenv()
        self.user_service = UserService()
        self.validation_service = ValidationService()
        self.email_service = EmailService()
        self.base_url = os.getenv('BASE_URL', 'http://localhost:3000')

    def _create_verification_email(self, user_name: str, email: str, code: str) -> tuple[str, str]:
        """
        Creates the email content for verification in both plain text and HTML formats

        Returns:
            tuple: (plain_text_content, html_content)
        """
        verification_link = f"{self.base_url}/verify?email={quote(email)}&code={code}"

        # Plain text version
        plain_text = f"""Hello {user_name}!

Thank you for using Better Calendar! To complete your registration, please enter this verification code in WhatsApp:

{code}

Or click this link to verify your email:
{verification_link}

If you didn't request this verification, please ignore this email.

Best regards,
Better Calendar Team"""

        # HTML version
        html_content = f"""
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <h2 style="color: #2c3e50;">Hello {user_name}!</h2>

    <p>Thank you for using What's Academy Better Calendar! To complete your registration, please use the verification code below:</p>

    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center;">
        <h1 style="color: #2c3e50; font-size: 32px; letter-spacing: 5px; margin: 0;">{code}</h1>
    </div>

    <p>Or click this button to verify your email:</p>

    <div style="text-align: center; margin: 25px 0;">
        <a href="{verification_link}" 
           style="background-color: #3498db; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">
           Verify Email
        </a>
    </div>

    <p style="color: #666; font-size: 14px;">If you didn't request this verification, please ignore this email.</p>

    <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">

    <p style="color: #666; font-size: 14px;">
        Best regards,<br>
        Better Calendar Team
    </p>
</body>
</html>"""

        return plain_text, html_content

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

        # Create and send verification email
        plain_text, html_content = self._create_verification_email(
            user_name=user.first_name,
            email=email,
            code=code
        )

        self.email_service.send_email(
            recipient_email=user.email,
            subject='Verify Your Better Calendar Account',
            body=plain_text,
            html_body=html_content
        )

        return f"""👋 Hello {user.first_name}!

📧 We've sent a verification code to:
   {email}

You can either:
1. Click the verification link in the email
2. Use this command:
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