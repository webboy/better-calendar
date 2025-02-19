from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Event:
    id: str
    name: str
    description: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str

    def __str__(self) -> str:
        return f"{self.name} on {self.start_date} at {self.start_time}"

    @property
    def day_name(self) -> str:
        """Get the day name (Monday, Tuesday, etc.) from start_date"""
        date_obj = datetime.strptime(self.start_date, "%d.%m.%Y")
        return date_obj.strftime("%A")

    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        """Create an Event instance from a dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            start_time=data.get('start_time'),
            end_date=data.get('end_date'),
            end_time=data.get('end_time')
        )

    def to_dict(self) -> dict:
        """Convert Event instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'start_time': self.start_time,
            'end_date': self.end_date,
            'end_time': self.end_time
        }

    def format_detailed(self) -> str:
        """Returns a detailed formatted string of the event"""
        return f"""📅 {self.name}
📝 {self.description}
📆 {self.day_name}, {self.start_date}
⏰ {self.start_time} - {self.end_time}"""