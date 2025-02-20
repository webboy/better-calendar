#!/usr/bin/env python3
import requests
import json
import os
import sys
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.event_service import EventService
from app.models.event import Event


def convert_ms_event(event):
    """Convert Masterschool event format to Better Calendar format"""
    # Parse start and end times
    start = datetime.fromisoformat(event['start'].replace('Z', '+00:00'))
    end = datetime.fromisoformat(event['end'].replace('Z', '+00:00'))

    # Create description
    description = event.get('description', 'No description provided')

    # Add VC link if available
    if event.get('hasVc') and event.get('vcUrl'):
        description += f"\n\nJoin meeting: {event['vcUrl']}"

    # Add recording links if available
    if event.get('recordingLinks'):
        description += "\n\nRecordings:"
        for link in event['recordingLinks']:
            description += f"\n{link}"

    return {
        "id": "",  # Will be generated as UUID by Event class
        "name": event['title'],
        "description": description,
        "start_date": start.strftime("%d.%m.%Y"),
        "start_time": start.strftime("%H:%M"),
        "end_date": end.strftime("%d.%m.%Y"),
        "end_time": end.strftime("%H:%M"),
        "source": "masterschool",
        "source_id": event['id']
    }


def download_calendar_events(output_file: str = 'storage/masterschool_events.json') -> None:
    """
    Download calendar events from Masterschool API and save to a JSON file

    Args:
        output_file: Name of the output JSON file
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    # Load environment variables
    load_dotenv()

    # Initialize event service
    event_service = EventService()

    # API endpoint
    url = 'https://app.masterschool.com/api/ms-calendar-hub/get-events'

    # Headers
    token = os.getenv('MS_CALENDAR_TOKEN')
    if not token:
        raise ValueError("MS_CALENDAR_TOKEN not found in .env file")

    headers = {
        'Accept': 'application/json',
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
    }

    # Calculate date range (4 months)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=120)

    # Request body
    payload = {
        "calendarIds": [
            "74f5b1c8-3348-4a0a-8da9-0e04cbb8842f",
            "d05a9886-cdaf-46ac-afd7-e84eec7e9923"
        ],
        "from": start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "to": end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }

    try:
        # Make the POST request
        logging.info(f"Sending request to {url}")
        response = requests.post(url, headers=headers, json=payload)

        # Log response status
        logging.info(f"Response Status: {response.status_code}")

        # Raise an error for bad status codes
        response.raise_for_status()

        # Parse response JSON
        data = response.json()
        logging.info("Successfully received data")

        # Convert and add events
        events_added = 0
        events_skipped = 0

        for ms_event in data:
            try:
                # Convert to our format
                event_data = convert_ms_event(ms_event)
                event = Event.from_dict(event_data)

                # Try to add the event
                event_service.add_event(event)
                events_added += 1
                logging.info(f"Added event: {event.name}")

            except ValueError as e:
                events_skipped += 1
                logging.warning(f"Skipped event due to conflict: {ms_event.get('title')} - {str(e)}")
            except Exception as e:
                events_skipped += 1
                logging.error(f"Error processing event {ms_event.get('title')}: {str(e)}")

        logging.info(f"\nSync completed:")
        logging.info(f"Events added: {events_added}")
        logging.info(f"Events skipped: {events_skipped}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    download_calendar_events()