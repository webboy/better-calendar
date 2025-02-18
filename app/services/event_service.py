from typing import List, Dict, Any
import json
from datetime import datetime


class EventService:

    def __init__(self, file_path: str = 'events.json'):
        self.file_path = file_path
        self.events = self.load_events()

    def load_events(self) -> Dict[str, Any]:
        try:
            with open(self.file_path, 'r') as json_file:
                return json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def list_events(self) -> List[str]:
        """Returns a list of event descriptions."""
        if self.events:
            return [event_data['description'] for event_data in self.events.values()]
        else:
            raise ValueError("You have no upcoming events")

    def update_db(self) -> None:
        """Updates the JSON file with the current events."""
        with open(self.file_path, 'w') as file:
            json.dump(self.events, file, indent=4)

    def add_events(self, host: str, location: str, event_name: str, event_date: str, event_time: str, guests: List[str]) -> None:
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

    def remove_event(self, event_name: str) -> None:
        """Removes an event from the events list."""
        if event_name in self.events:
            del self.events[event_name]
            self.update_db()
        else:
            raise KeyError("Event not found")

    def update_event(self, name: str, **kwargs: Any) -> None:
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

    def update_date_related_fields(self, name: str, date: str) -> None:
        """Updates the date-related fields for an event."""
        valid_date = datetime.strptime(date, '%d-%m-%Y')
        self.events[name]['day_name'] = valid_date.strftime('%A')
        self.events[name]['is_weekday'] = valid_date.weekday() < 5
        self.events[name]['month_name'] = valid_date.strftime('%B')



#Small tests
es = EventService()
# print(es.list_events())
es.add_events('nem', 'zoom', "Joud and kehalit", "10-10-2010", "10:10:10", ['Joud', "kehalit"])
es.update_event("Joud and kehalit", date="11-11-2011", time="11:11:11")
