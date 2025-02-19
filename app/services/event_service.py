from typing import List, Dict
import json
from datetime import datetime, timedelta
from app.models.event import Event


class EventService:
    def __init__(self, file_path='storage/events.json'):
        self.file_path = file_path
        self.events: List[Event] = []
        self.load_events()

    def load_events(self) -> None:
        """Loads events from JSON file into Event objects"""
        try:
            with open(self.file_path, 'r') as json_file:
                events_data = json.load(json_file)
                self.events = [Event.from_dict(event_data) for event_data in events_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.events = []

    def save_events(self) -> None:
        """Saves events to JSON file"""
        with open(self.file_path, 'w') as json_file:
            json.dump([event.to_dict() for event in self.events], json_file, indent=4)

    def list_events(self, time_frame: str = 'all') -> List[Event]:
        """Returns events within the specified time frame"""
        if not self.events:
            raise ValueError("You have no upcoming events")

        now = datetime.now()

        # Convert string dates to datetime for comparison
        def is_event_in_timeframe(event: Event) -> bool:
            event_date = datetime.strptime(event.start_date, "%d.%m.%Y")
            if time_frame == 'day':
                return event_date.date() == now.date()
            elif time_frame == 'week':
                week_later = now + timedelta(weeks=1)
                return now.date() <= event_date.date() <= week_later.date()
            elif time_frame == 'month':
                month_later = now + timedelta(weeks=4)
                return now.date() <= event_date.date() <= month_later.date()
            return True  # 'all' timeframe

        return [event for event in self.events if is_event_in_timeframe(event)]

    def add_event(self, event: Event) -> None:
        """Adds a new event to the list"""
        # Check for time conflicts
        event_start = datetime.strptime(f"{event.start_date} {event.start_time}", "%d.%m.%Y %H:%M")
        event_end = datetime.strptime(f"{event.end_date} {event.end_time}", "%d.%m.%Y %H:%M")

        for existing_event in self.events:
            existing_start = datetime.strptime(
                f"{existing_event.start_date} {existing_event.start_time}",
                "%d.%m.%Y %H:%M"
            )
            existing_end = datetime.strptime(
                f"{existing_event.end_date} {existing_event.end_time}",
                "%d.%m.%Y %H:%M"
            )

            if event_start < existing_end and event_end > existing_start:
                raise ValueError(
                    f"Time Conflict: {existing_event.name} on {existing_event.start_date} "
                    f"at {existing_event.start_time} till {existing_event.end_time}"
                )

        self.events.append(event)
        self.save_events()

    def remove_event(self, event_id: str) -> None:
        """Removes an event by ID"""
        self.events = [event for event in self.events if event.id != event_id]
        self.save_events()

    def get_event_by_id(self, event_id: str) -> Event:
        """Gets an event by ID"""
        for event in self.events:
            if event.id == event_id:
                return event
        raise ValueError("Event not found")