from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
import os.path
import json
from typing import List, Dict
from app.models.event import Event
from app.services.event_service import EventService


class GoogleCalendarService:
    def __init__(self, credentials_path: str = 'credentials.json'):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        self.credentials_path = credentials_path
        self.event_service = EventService()

    def get_calendar_service(self):
        """Get an authorized Calendar API service instance"""
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)

    def sync_events(self, start_date: str, end_date: str) -> int:
        """
        Sync Google Calendar events to local storage

        Args:
            start_date: Date in YYYY-MM-DD format
            end_date: Date in YYYY-MM-DD format

        Returns:
            Number of events synced
        """
        service = self.get_calendar_service()

        # Get events from Google Calendar
        events_result = service.events().list(
            calendarId='primary',
            timeMin=f"{start_date}T00:00:00Z",
            timeMax=f"{end_date}T23:59:59Z",
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        # Get existing event IDs
        existing_ids = {event.id for event in self.event_service.events}

        # Add only new events
        sync_count = 0
        for google_event in events:
            if google_event['id'] not in existing_ids:
                try:
                    # Convert Google Calendar event to our format
                    start = google_event['start'].get('dateTime', google_event['start'].get('date'))
                    end = google_event['end'].get('dateTime', google_event['end'].get('date'))

                    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))

                    event = Event(
                        id='',
                        name=google_event['summary'],
                        description=google_event.get('description', 'No description provided'),
                        start_date=start_dt.strftime("%d.%m.%Y"),
                        start_time=start_dt.strftime("%H:%M"),
                        end_date=end_dt.strftime("%d.%m.%Y"),
                        end_time=end_dt.strftime("%H:%M"),
                        source="google",
                        source_id=google_event['id']
                    )

                    self.event_service.add_event(event)
                    sync_count += 1
                except ValueError as e:
                    print(f"Skipping event due to conflict: {google_event.get('summary')} - {str(e)}")

        return sync_count


def sync_google_calendar(credentials_path: str, start_date: str, end_date: str) -> str:
    """Command-line function to sync Google Calendar events"""
    try:
        sync_service = GoogleCalendarService(credentials_path)
        events_synced = sync_service.sync_events(start_date, end_date)
        return f"Successfully synced {events_synced} new events from Google Calendar"
    except Exception as e:
        return f"Error syncing events: {str(e)}"