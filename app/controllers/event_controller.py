from typing import List
from app.services.user_service import UserService

class EventController:
    def list_events(self, args: List[str], wa_id: str, phone_number: str) -> str:
        """Placeholder for list-events command - to be implemented"""
        # Instantiation of the user service
        user_service = UserService()

        # Check if the user is validated
        if not user_service.is_validated(wa_id, phone_number):
            raise Exception("User is not validated")

        # Placeholder for listing events. Read the list of events and return them

        return "List events command received"