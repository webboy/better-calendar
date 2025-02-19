# reminder_controller.py
from typing import List
from app.services.validation_service import ValidationService
from app.services.user_service import UserService


class ReminderController:
    def __init__(self):
        self.validation_service = ValidationService()
        self.user_service = UserService()

    def reminder(self, args: List[str], wa_id: str, phone_number: str) -> str:
        """Handle reminder time setting"""
        if not args:
            return f"""⚠️ Missing Reminder Time

Please specify a reminder time:
!reminder <time>

Valid times: 5, 10, or 15 minutes"""

        time_str = args[0]

        # Validate the reminder time
        if not self.validation_service.validate_reminder_time(time_str):
            return f"""❌ Invalid Reminder Time

The reminder time must be either 5, 10, or 15 minutes.
Example: !reminder 10"""

        # Get user and update reminder
        user = self.user_service.get_user_by_wa_id(wa_id)
        self.user_service.update_reminder(user.email, int(time_str))

        return f"""✅ Reminder Set Successfully

You will be notified {time_str} minutes before each event.
Current reminder setting: {time_str} minutes"""