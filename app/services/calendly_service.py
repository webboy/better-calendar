import os
from datetime import datetime
import requests
from typing import List, Dict
from app.models.event import Event
from app.services.event_service import EventService


class CalendlyService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.calendly.com/scheduled_events"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.event_service = EventService()

    def fetch_events(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Fetch events from Calendly within the specified date range

        Args:
            start_date: ISO format date (YYYY-MM-DD)
            end_date: ISO format date (YYYY-MM-DD)
        """
        # Extract user UUID from the token
        user_info_response = requests.get(
            "https://api.calendly.com/users/me",
            headers=self.headers
        )
        if user_info_response.status_code != 200:
            raise Exception(f"Failed to fetch user info: {user_info_response.text}")

        user_uri = user_info_response.json()["resource"]["uri"]

        params = {
            "min_start_time": f"{start_date}T00:00:00Z",
            "max_start_time": f"{end_date}T23:59:59Z",
            "status": "active",
            "user": user_uri
        }

        response = requests.get(
            self.base_url,
            headers=self.headers,
            params=params
        )

        if response.status_code != 200:
            raise Exception(f"Failed to fetch Calendly events: {response.text}")

        return response.json().get("collection", [])

    def _transform_calendly_event(self, calendly_event: Dict) -> Event:
        """Transform Calendly event format to our Event model format"""
        start_time = datetime.fromisoformat(calendly_event["start_time"].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(calendly_event["end_time"].replace('Z', '+00:00'))

        return Event(
            id='',
            name=calendly_event["name"],
            description=calendly_event.get("description", "No description provided"),
            start_date=start_time.strftime("%d.%m.%Y"),
            start_time=start_time.strftime("%H:%M"),
            end_date=end_time.strftime("%d.%m.%Y"),
            end_time=end_time.strftime("%H:%M"),
            source="calendly",
            source_id=calendly_event["uri"].split('/')[-1]
        )

    def sync_events(self, start_date: str, end_date: str) -> int:
        """
        Sync Calendly events to local storage

        Args:
            start_date: Date in YYYY-MM-DD format
            end_date: Date in YYYY-MM-DD format

        Returns:
            Number of events synced
        """
        # Fetch events from Calendly
        calendly_events = self.fetch_events(start_date, end_date)

        # Transform to our Event format
        events = [self._transform_calendly_event(event) for event in calendly_events]

        # Get existing event IDs
        existing_ids = {event.id for event in self.event_service.events}

        # Add only new events
        sync_count = 0
        for event in events:
            if event.id not in existing_ids:
                try:
                    self.event_service.add_event(event)
                    sync_count += 1
                except ValueError as e:
                    print(f"Skipping event due to conflict: {event.name} - {str(e)}")

        return sync_count


def sync_calendly_events(api_key: str, start_date: str, end_date: str) -> str:
    """
    Command-line function to sync Calendly events

    Args:
        api_key: Calendly API key
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    try:
        sync_service = CalendlyService(api_key)
        events_synced = sync_service.sync_events(start_date, end_date)
        return f"Successfully synced {events_synced} new events from Calendly"
    except Exception as e:
        return f"Error syncing events: {str(e)}"