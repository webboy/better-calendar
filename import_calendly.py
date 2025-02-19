#!/usr/bin/env python3
import argparse
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.services.calendly_service import sync_calendly_events


def main():
    # Load environment variables from .env
    load_dotenv()

    parser = argparse.ArgumentParser(description='Sync Calendly events to local storage')
    parser.add_argument('--api-key', help='Calendly API key (optional if CALENDLY_API_KEY is set in .env)')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)', default=None)
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)', default=None)

    args = parser.parse_args()

    # Use API key from command line or fall back to environment variable
    api_key = args.api_key or os.getenv('CALENDLY_API_KEY')
    if not api_key:
        print("Error: Calendly API key must be provided either via --api-key or CALENDLY_API_KEY environment variable")
        return

    # If dates not provided, default to syncing next 30 days
    if not args.start_date:
        start_date = datetime.now().strftime('%Y-%m-%d')
    else:
        start_date = args.start_date

    if not args.end_date:
        end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    else:
        end_date = args.end_date

    result = sync_calendly_events(api_key, start_date, end_date)
    print(result)


if __name__ == '__main__':
    main()