import re

class ValidationService:

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address"""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return False
        return True