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

    def update_db(self):
        """Writes the current events to the JSON file."""
        with open(self.file_path, 'w') as json_file:
            json.dump(self.events, json_file, indent=4)

    def list_events(self, time_frame: str = 'all') -> List[str]:
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
            return f"{event_data['name']} on {event_data['day_name']} at {event_data['time']} till {event_data['end_time']}"
        elif time_frame == 'month' or time_frame == 'all':
            return f"{event_data['name']} on {event_data['date']} at {event_data['time']} till {event_data['end_time']}"
        else:
            return event_data['description']

    def add_events(self, host: str, location: str, event_name: str, event_date: str, event_time: str, guests: List[str], duration: int):
        """Adds a new event to the events list."""
        try:
            valid_date_time = datetime.strptime(f'{event_date} {event_time}', '%d-%m-%Y %H:%M:%S')
            event_start_timestamp = valid_date_time.timestamp()
            event_end_time = valid_date_time + timedelta(hours=duration)
            event_end_timestamp = event_end_time.timestamp()
        except ValueError:
            raise ValueError("Invalid date and time format")


        for existing_start_timestamp in map(float, self.events.keys()):
            existing_event = self.events[str(existing_start_timestamp)]
            existing_event_start = datetime.strptime(
                f"{existing_event['date']} {existing_event['time']}", '%d-%m-%Y %H:%M:%S'
            ).timestamp()
            existing_event_duration = existing_event.get('duration', 1)
            existing_event_end = existing_event_start + (existing_event_duration * 3600)

            if (event_start_timestamp < existing_event_end) and (event_end_timestamp > existing_event_start):
                raise ValueError(f"Time Conflict: {existing_event['name']} is on {existing_event['date']} at {existing_event['time']}")


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
            'duration': duration,
            'end_time': event_end_time.strftime('%H:%M:%S'),
            'description': f"{event_name} on {event_date} at {event_time} till {event_end_time.strftime('%H:%M:%S')}"
        }


        self.events[str(event_start_timestamp)] = event_data
        self.update_db()

    def remove_event(self, event_name: str):
        """Removes an event from the events list by name."""
        event_to_remove = None
        for timestamp, event in self.events.items():
            if event['name'] == event_name:
                event_to_remove = timestamp
                break

        if event_to_remove:
            del self.events[event_to_remove]
            self.update_db()
        else:
            raise KeyError("Event not found")

    def update_event(self, name: str, **kwargs: Any):
        """Updates an existing event with the given parameters."""
        event_to_update = None
        for timestamp, event in self.events.items():
            if event['name'] == name:
                event_to_update = timestamp
                break

        if event_to_update is None:
            raise KeyError("Event not found")

        for key, value in kwargs.items():
            if key in self.events[event_to_update]:
                self.events[event_to_update][key] = value
                if key == 'date':
                    self.update_date_related_fields(event_to_update, value)
            else:
                raise ValueError("Invalid Event Param")

        self.update_db()

    def update_date_related_fields(self, timestamp: str, date: str):
        """Updates the date-related fields for an event."""
        valid_date = datetime.strptime(date, '%d-%m-%Y')
        self.events[timestamp]['day_name'] = valid_date.strftime('%A')
        self.events[timestamp]['is_weekday'] = valid_date.weekday() < 5
        self.events[timestamp]['month_name'] = valid_date.strftime('%B')


