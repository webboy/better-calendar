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
                self.events = self._sort_events(self.events)
        except (FileNotFoundError, json.JSONDecodeError):
            self.events = []

    def _sort_events(self, events: List[Event]) -> List[Event]:
        """Sorts events by start_date and start_time in ascending order"""
        return sorted(events,
                      key=lambda e: (
                          datetime.strptime(e.start_date, "%d.%m.%Y"),
                          datetime.strptime(e.start_time, "%H:%M")
                      ))

    def save_events(self) -> None:
        """Saves events to JSON file"""
        with open(self.file_path, 'w') as json_file:
            json.dump([event.to_dict() for event in self.events], json_file, indent=4)

    def list_events(self, time_frame: str = 'all') -> List[Event]:
        """Returns sorted events within the specified time frame"""
        self.load_events()

        if not self.events:
            raise ValueError("You have no upcoming events")

        now = datetime.now()

        def is_event_in_timeframe(event: Event) -> bool:
            event_date = datetime.strptime(event.start_date, "%d.%m.%Y")

            if time_frame == 'today':
                return event_date.date() == now.date()

            elif time_frame == 'tomorrow':
                tomorrow = now.date() + timedelta(days=1)
                return event_date.date() == tomorrow

            elif time_frame == 'this-week':
                start_of_week = now.date() - timedelta(days=now.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                return start_of_week <= event_date.date() <= end_of_week

            elif time_frame == 'next-week':
                start_of_next_week = now.date() + timedelta(days=7 - now.weekday())
                end_of_next_week = start_of_next_week + timedelta(days=6)
                return start_of_next_week <= event_date.date() <= end_of_next_week

            elif time_frame == 'this-month':
                return (event_date.year == now.year and
                        event_date.month == now.month)

            elif time_frame == 'next-month':
                if now.month == 12:
                    next_month_year = now.year + 1
                    next_month = 1
                else:
                    next_month_year = now.year
                    next_month = now.month + 1
                return (event_date.year == next_month_year and
                        event_date.month == next_month)

            return True  # 'all' timeframe

        filtered_events = [event for event in self.events if is_event_in_timeframe(event)]
        return self._sort_events(filtered_events)

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
        self.events = self._sort_events(self.events)
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