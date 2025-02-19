# validation_service.py
import re
from typing import List

class ValidationService:
    VALID_REMINDER_TIMES = [5, 10, 15]

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address"""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return False
        return True

    def validate_reminder_time(self, time_str: str) -> bool:
        """Validate reminder time"""
        try:
            time = int(time_str)
            return time in self.VALID_REMINDER_TIMES
        except ValueError:
            return False