# What's Academy - Better Calendar

A comprehensive calendar management system designed for Masterschool students, integrating multiple calendar sources into a unified platform with WhatsApp notifications.

## Features

- **Multi-Source Calendar Integration**
  - Google Calendar sync
  - Calendly integration
  - Masterschool Calendar sync
  - Local calendar management

- **WhatsApp Integration**
  - Event notifications
  - Command-line interface via WhatsApp
  - Interactive event management

- **Email Verification**
  - Secure user verification process
  - HTML email templates
  - Verification link support

## Setup

1. Clone the repository:
```bash
git clone https://github.com/webboy/better-calendar.git
cd better-calendar
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_number

# Email Configuration
SMTP_EMAIL=your_email
SMTP_PASSWORD=your_password

# Calendar APIs
GOOGLE_CREDENTIALS_PATH=path/to/credentials.json
MS_CALENDAR_TOKEN=your_token
CALENDLY_API_KEY=your_key

# Application
BASE_URL=http://your-domain.com
```

## Usage

### CLI Commands

1. Import events from Google Calendar:
```bash
python cli/import_google_calendar.py
```

2. Import events from Calendly:
```bash
python cli/import_calendly.py
```

3. Import Masterschool events:
```bash
python cli/import_masterschool.py
```

4. Seed sample events:
```bash
python cli/event_seeder.py
```

### WhatsApp Commands

- `!help` - Show available commands
- `!register <email>` - Start registration process
- `!validate <email> <code>` - Complete registration
- `!events` - List upcoming events
- `!events today` - Show today's events
- `!events tomorrow` - Show tomorrow's events
- `!events this-week` - Show this week's events
- `!events next-week` - Show next week's events
- `!reminder <5, 10, 15>` - Set event reminder on 5 ,10, or 15 minutes

## Project Structure

```
better-calendar/
├── app/
│   ├── models/
│   │   └── event.py
│   └── services/
│       ├── calendly_service.py
│       ├── email_service.py
│       ├── event_service.py
│       ├── google_calendar_service.py
│       └── twilio_service.py
├── cli/
│   ├── download_masterschool_calendar.py
│   ├── import_calendly.py
│   ├── import_google_calendar.py
│   └── event_seeder.py
├── storage/
│   └── events.json
└── app.py
```

## Local Development

1. Start the Flask server:
```bash
python app.py
```

2. Test the webhook:
```bash
curl -X POST http://localhost:5000/webhook -d "Body=!help"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.