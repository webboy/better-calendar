#!/usr/bin/env python3
import json
import os
import sys
import logging
from datetime import datetime

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.event import Event
from app.services.event_service import EventService


def seed_events(seed_file: str = 'seeds/events_seed.json') -> None:
    """
    Seed events from JSON file into the event storage

    Args:
        seed_file: Path to the seed JSON file
    """
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    try:
        # Initialize event service
        event_service = EventService()

        # Read seed file
        logging.info(f"Reading seed file: {seed_file}")
        with open(seed_file, 'r') as f:
            seed_data = json.load(f)

        # Track statistics
        total_events = len(seed_data)
        added_events = 0
        skipped_events = 0

        # Process each event
        for event_data in seed_data:
            try:
                # Add source information
                event_data['source'] = 'better-calendar'
                event_data['source_id'] = ''  # Will be replaced with UUID

                # Create event instance
                event = Event.from_dict(event_data)

                # Add to storage
                event_service.add_event(event)
                added_events += 1
                logging.info(f"Added event: {event.name}")

            except ValueError as e:
                skipped_events += 1
                logging.warning(f"Skipped event due to conflict: {event_data.get('name')} - {str(e)}")
            except Exception as e:
                skipped_events += 1
                logging.error(f"Error processing event {event_data.get('name')}: {str(e)}")

        # Log summary
        logging.info(f"\nSeeding completed:")
        logging.info(f"Total events in seed file: {total_events}")
        logging.info(f"Successfully added: {added_events}")
        logging.info(f"Skipped: {skipped_events}")

    except FileNotFoundError:
        logging.error(f"Seed file not found: {seed_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in seed file: {seed_file}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    seed_file = 'seeds\\events_seed.json'
    if len(sys.argv) > 1:
        seed_file = sys.argv[1]

    seed_events(seed_file)