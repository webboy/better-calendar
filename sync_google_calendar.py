#!/usr/bin/env python3
import argparse
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.services.google_calendar_service import sync_google_calendar


def main():
    # Load environment variables from .env
    load_dotenv()

    parser = argparse.ArgumentParser(description='Sync Google Calendar events to local storage')
    parser.add_argument('--credentials',
                        help='Path to Google Calendar credentials.json (optional if GOOGLE_CREDENTIALS_PATH is set in .env)')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)', default=None)
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)', default=None)

    args = parser.parse_args()

    # Use credentials path from command line or fall back to environment variable or default
    credentials_path = args.credentials or os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')

    # If dates not provided, default to syncing next 30 days
    if not args.start_date:
        start_date = datetime.now().strftime('%Y-%m-%d')
    else:
        start_date = args.start_date

    if not args.end_date:
        end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    else:
        end_date = args.end_date

    result = sync_google_calendar(credentials_path, start_date, end_date)
    print(result)


if __name__ == '__main__':
    main()