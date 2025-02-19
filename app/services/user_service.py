import json
import re
from typing import List, Optional, Dict
from app.models.user import User

class UserService:
    def __init__(self):
        """Initializes the UserService with users from a JSON file."""
        self.json_file = 'storage/users.json'
        self.users: Dict[str, User] = {}  # email -> User mapping
        self.load_users_from_json()

    def load_users_from_json(self) -> None:
        """Loads users from the JSON file containing an array of user objects."""
        try:
            with open(self.json_file, 'r') as file:
                user_list = json.load(file)  # Directly loads the array
                for user_data in user_list:
                    user = User.from_dict(user_data)
                    self.users[user.email] = user
        except FileNotFoundError:
            raise ValueError(f"Error: The file '{self.json_file}' was not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: The file '{self.json_file}' is not a valid JSON.")

    def save_users(self) -> None:
        """Saves users as an array to the JSON file."""
        with open(self.json_file, 'w') as file:
            json.dump(
                [user.to_dict() for user in self.users.values()],
                file,
                indent=4
            )

    def get_user_by_email(self, email: str) -> User:
        """Returns the user with the given email or raises ValueError."""
        if email in self.users:
            return self.users[email]
        raise ValueError("Sorry, we cannot find the email in our database. This app is only for Masterschool students.")

    def get_user_by_wa_id(self, wa_id: str) -> Optional[User]:
        """Returns the user with the given WhatsApp ID or None."""
        for user in self.users.values():
            if user.wa_id == wa_id:
                return user
        return None

    def link_whatsapp(self, email: str, wa_id: str, phone_number: str) -> None:
        """Links WhatsApp information to a user account."""
        user = self.get_user_by_email(email)
        self.users[email].update_whatsapp_info(phone_number, wa_id)
        self.save_users()


    def is_validated(self, wa_id: str) -> bool:
        """Checks if the user with given wa_id exists and is registered."""
        user = self.get_user_by_wa_id(wa_id)
        return user is not None and user.is_registered

    def get_all_users(self) -> List[User]:
        """Returns list of all users."""
        return list(self.users.values())

    def get_user_emails(self) -> List[str]:
        """Returns list of all user emails."""
        return list(self.users.keys())

    def generate_validation_code(self) -> str:
        """Generates a random 6-digit validation code."""
        import random
        return str(random.randint(100000, 999999))

    def set_validation_code(self, email: str, code: str) -> None:
        """Sets a new validation code for the user and returns it."""
        self.load_users_from_json()
        self.users[email].validation_code = code
        self.save_users()

    def verify_code(self, email: str, code: str) -> bool:
        """Verifies if the provided code matches the stored validation code."""
        user = self.get_user_by_email(email)
        return user.validation_code == code