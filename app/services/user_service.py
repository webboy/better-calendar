import json
import re
from typing import List

class UserService:
    def __init__(self, json_file: str):
        """Initializes the UserService with the list of approved users from a JSON file."""
        self.json_file = json_file
        self.user_emails = self.load_users_from_json()

    def load_users_from_json(self) -> List[str]:
        """Loads the list of approved users from the JSON file."""
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                return data.get('approved_users', [])
        except FileNotFoundError:
            raise ValueError(f"Error: The file '{self.json_file}' was not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: The file '{self.json_file}' is not a valid JSON.")

    def is_validated(self, wa_id: str, phone_number: str) -> bool:
        """Checks if the user is validated based on their wa_id and phone_number.
        Placeholder: In real use case, it should check against the database."""
        # Assuming validation would occur here (you can modify it as needed)
        # Currently, it returns True for the sake of example.
        return True

    def get_user_by_wa_id(self, wa_id: str) -> str:
        """Returns the user associated with the given wa_id.
        Placeholder: Can be expanded to fetch user info based on wa_id."""
        return "User"  # Placeholder

    def get_user_list(self) -> List[str]:
        """Returns the list of all approved user emails."""
        return self.user_emails

    def save_users(self, users: List[str]) -> None:
        """Adds new users to the JSON file (appends to the list)."""
        self.user_emails.extend(users)
        with open(self.json_file, 'w') as file:
            json.dump({"approved_users": self.user_emails}, file, indent=4)

    def get_user_by_email(self, email: str) -> bool:
        """Returns True if the email exists in the list of approved users, otherwise False."""
        if email in self.user_emails:
            return True
        else:
            raise ValueError("Sorry, we cannot find the email in our database. This app is only for Masterschool students.")

    def invalid_input(self, email: str) -> None:
        """Checks if the input email is in a valid format. Raises ValueError if invalid."""
        #validating basic email structure (user@example.com)
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError(f"Invalid email format: {email}. Please provide a valid email address.")

# Example usage
user_service = UserService('users.json')

# Test for email validation
try:
    email_input = 'jud@gmail.com'  # This email will be invalid for testing purposes
    user_service.invalid_input(email_input)  # This will raise ValueError if invalid format
    user_exists = user_service.get_user_by_email(email_input)
    print(user_exists)  # This will print True if the email is found, or the exception message is raised.
except ValueError as e:
    print(e)  # Handle exception and print message if the email is not valid or not found.
