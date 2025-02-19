from dataclasses import dataclass
from datetime import datetime
import re
import uuid
from typing import Literal

SourceType = Literal["better-calendar", "google", "calendly"]

@dataclass
class Event:
    id: str  # Will be UUID
    name: str
    description: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    source: SourceType
    source_id: str

    def __post_init__(self):
        """Ensure ID is always a valid UUID"""
        if not self.id:
            self.id = str(uuid.uuid4())
        try:
            uuid.UUID(self.id)
        except ValueError:
            # If current ID is not a valid UUID, use it as source_id and generate new UUID
            if not self.source_id:
                self.source_id = self.id
            self.id = str(uuid.uuid4())

    def __str__(self) -> str:
        return f"{self.name} on {self.start_date} at {self.start_time}"

    @property
    def day_name(self) -> str:
        """Get the day name (Monday, Tuesday, etc.) from start_date"""
        date_obj = datetime.strptime(self.start_date, "%d.%m.%Y")
        return date_obj.strftime("%A")

    @property
    def clean_description(self) -> str:
        """Returns the description with HTML tags removed"""
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', self.description)
        # Replace HTML entities
        clean_text = clean_text.replace('&nbsp;', ' ')
        clean_text = clean_text.replace('&amp;', '&')
        clean_text = clean_text.replace('&lt;', '<')
        clean_text = clean_text.replace('&gt;', '>')
        clean_text = clean_text.replace('&quot;', '"')
        # Remove extra whitespace
        clean_text = ' '.join(clean_text.split())
        return clean_text

    def get_status(self) -> str:
        """Returns the current status of the event"""
        now = datetime.now()

        # Convert event times to datetime objects
        start_datetime = datetime.strptime(f"{self.start_date} {self.start_time}", "%d.%m.%Y %H:%M")
        end_datetime = datetime.strptime(f"{self.end_date} {self.end_time}", "%d.%m.%Y %H:%M")

        if now < start_datetime:
            return "🔜 Upcoming"
        elif start_datetime <= now <= end_datetime:
            return "▶️ Ongoing"
        else:
            return "✅ Finished"

    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        """Create an Event instance from a dictionary"""
        return cls(
            id=data.get('id', ''),  # Empty string will trigger UUID generation
            name=data.get('name'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            start_time=data.get('start_time'),
            end_date=data.get('end_date'),
            end_time=data.get('end_time'),
            source=data.get('source',"better-calendar"),  # Default to better-calendar
            source_id=data.get('source_id', '')
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
            'end_time': self.end_time,
            'source': self.source,
            'source_id': self.source_id
        }

    def format_detailed(self) -> str:
        """Returns a detailed formatted string of the event with status"""
        return f"""{self.get_status()}: {self.name}
📝 {self.clean_description}
📆 {self.day_name}, {self.start_date}
⏰ {self.start_time} - {self.end_time}\n"""