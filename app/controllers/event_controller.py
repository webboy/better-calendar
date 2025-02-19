from typing import List, Dict, Set
from app.services.user_service import UserService
from app.services.event_service import EventService

class EventController:
    TIMEFRAME_HEADERS: Dict[str, str] = {
        'today': "📅 Today's Events",
        'tomorrow': "📅 Tomorrow's Events",
        'this-week': "📅 This Week's Events",
        'next-week': "📅 Next Week's Events",
        'this-month': "📅 This Month's Events",
        'next-month': "📅 Next Month's Events"
    }

    VALID_TIMEFRAMES: Set[str] = set(TIMEFRAME_HEADERS.keys())

    HELP_TEXT = """
Available timeframes:
!events today   - Today's events (default)
!events tomorrow - Tomorrow's events
!events this-week - Current week's events
!events next-week - Next week's events
!events this-month - Current month's events
!events next-month - Next month's events"""

    def __init__(self):
        self.user_service = UserService()
        self.event_service = EventService()

    def list_events(self, args: List[str], wa_id: str, phone_number: str) -> str:
        """Lists events based on the specified timeframe"""
        # Get the user by WhatsApp ID
        user = self.user_service.get_user_by_wa_id(wa_id)

        # Parse timeframe argument if provided
        time_frame = args[0] if args else 'today'  # default to today's events

        # Validate timeframe parameter
        if time_frame not in self.VALID_TIMEFRAMES:
            return f"""❌ Invalid timeframe: {time_frame}
{self.HELP_TEXT}"""

        try:
            events = self.event_service.list_events(time_frame)

            if not events:
                return f"""📅 No Events Found
No events scheduled for the selected time frame.
{self.HELP_TEXT}"""

            # Build response with header and events
            response = f"{self.TIMEFRAME_HEADERS.get(time_frame)}\n"

            # Add events with emojis and formatting
            for i, event in enumerate(events, 1):
                response += f"\n{i}. {event.format_detailed()}"

            # Add help text footer
            response += f"\n{self.HELP_TEXT}"

            return response

        except ValueError as e:
            return f"""📅 No Events Found

{str(e)}
{self.HELP_TEXT}"""