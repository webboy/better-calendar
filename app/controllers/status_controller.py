# app/controllers/status_controller.py
class StatusController:
    def __init__(self):
        self.reminders = {}  # Store user reminders, keyed by username

    def get_reminder(self, username):
        reminder_time = self.reminders.get(username, None)
        if reminder_time:
            return f"Your reminder is set to {reminder_time} minutes."
        else:
            return "You don't have a reminder."

    def set_reminder(self, username, time_in_minutes):
        self.reminders[username] = time_in_minutes
