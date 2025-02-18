from typing import List, Dict, Any
import json
from datetime import datetime, timedelta


class EventService:

    def __init__(self, file_path='events.json'):
        self.file_path = file_path
        self.events = self.load_events()

    def load_events(self):
        try:
            with open(self.file_path, 'r') as json_file:
                return json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def list_events(self, time_frame: str = '') -> List[str]:
        """Returns a list of event descriptions within the specified time frame."""
        if not self.events:
            raise ValueError("You have no upcoming events")

        now = datetime.now()
        if time_frame == 'day':
            end_time = now + timedelta(days=1)
        elif time_frame == 'week':
            end_time = now + timedelta(weeks=1)
        elif time_frame == 'month':
            end_time = now + timedelta(weeks=4)
        else:
            return [self.format_event_description(event_data, 'all') for event_data in self.events.values()]

        filtered_events = [
            self.format_event_description(event_data, time_frame)
            for event_data in self.events.values()
            if now <= datetime.strptime(event_data['date'], '%d-%m-%Y') <= end_time
        ]

        return filtered_events

    def format_event_description(self, event_data: Dict, time_frame: str) -> str:
        """Formats event descriptions based on the time frame."""
        if time_frame == 'week':
            return f"{event_data['name']} on {event_data['day_name']} at {event_data['time']}"
        elif time_frame == 'month' or time_frame == 'all':
            return f"{event_data['name']} on {event_data['date']} at {event_data['time']}"
        else:
            return event_data['description']

    def update_db(self) :
        """Updates the JSON file with the current events."""
        with open(self.file_path, 'w') as file:
            json.dump(self.events, file, indent=4)

    def add_events(self, host: str, location: str, event_name: str, event_date: str, event_time: str, guests: List[str]):
        """Adds a new event to the events list."""
        try:
            valid_date_time = datetime.strptime(f'{event_date} {event_time}', '%d-%m-%Y %H:%M:%S')
        except ValueError:
            raise ValueError("Invalid date and time format")

        event_data = {
            'name': event_name,
            'host': host,
            'location': location,
            'date': event_date,
            'time': event_time,
            'day_name': valid_date_time.strftime('%A'),
            'is_weekday': valid_date_time.weekday() < 5,
            'month_name': valid_date_time.strftime('%B'),
            'guests': guests,
            'description': f"{event_name} on {event_date} at {event_time}"
        }

        self.events[event_name] = event_data
        self.update_db()

    def remove_event(self, event_name: str):
        """Removes an event from the events list."""
        if event_name in self.events:
            del self.events[event_name]
            self.update_db()
        else:
            raise KeyError("Event not found")

    def update_event(self, name: str, **kwargs: Any):
        """Updates an existing event with the given parameters."""
        if name not in self.events:
            raise KeyError("Event not found")

        for key, value in kwargs.items():
            if key in self.events[name]:
                self.events[name][key] = value
                if key == 'date':
                    self.update_date_related_fields(name, value)
            else:
                raise ValueError("Invalid Event Param")

        self.update_db()

    def update_date_related_fields(self, name: str, date: str):
        """Updates the date-related fields for an event."""
        valid_date = datetime.strptime(date, '%d-%m-%Y')
        self.events[name]['day_name'] = valid_date.strftime('%A')
        self.events[name]['is_weekday'] = valid_date.weekday() < 5
        self.events[name]['month_name'] = valid_date.strftime('%B')

