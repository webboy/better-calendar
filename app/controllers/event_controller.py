from typing import List
from app.services.user_service import UserService
from app.services.event_service import EventService


class EventController:

    def __init__(self):
        self.user_service = UserService()
        self.event_service = EventService()

    def list_events(self, args: List[str], wa_id: str, phone_number: str) -> str:
        """Lists events based on the specified timeframe"""
        # Get the user by WhatsApp ID
        user = self.user_service.get_user_by_wa_id(wa_id)

        # Parse timeframe argument if provided
        time_frame = args[0] if args else 'day'  # default to today's events

        try:
            events = self.event_service.list_events(time_frame)

            if not events:
                return f"""📅 No Events Found
No events scheduled for the selected time frame.

Try:
!events day   - Today's events
!events week  - This week's events
!events month - This month's events
!events all   - All upcoming events"""

            # Create header based on timeframe
            headers = {
                'day': "📅 Today's Events",
                'week': "📅 This Week's Events",
                'month': "📅 This Month's Events",
                'all': "📅 All Upcoming Events"
            }

            response = f"{headers.get(time_frame, '📅 Events')}\n"

            # Add events with emojis and formatting
            for i, event in enumerate(events, 1):
                response += f"\n{i}. {event}"

            # Add footer with command help
            response += f"""

Available timeframes:
!events day   - Today's events
!events week  - This week's events
!events month - This month's events
!events all   - All upcoming events"""

            return response

        except ValueError as e:
            return f"""📅 No Events Found

{str(e)}

Available commands:
!events day   - Today's events
!events week  - This week's events
!events month - This month's events
!events all   - All upcoming events"""