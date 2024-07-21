from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Replace 'YOUR_API_KEY' with your actual Google Calendar API key
API_KEY = 'AIzaSyB5mF-9EeJFAFOJjVCc93LyjJu2KSwDJTQ'

def create_calendar_event(event_data):
    try:
        # Build the calendar service with the API key
        calendar_service = build('calendar', 'v3', developerKey=API_KEY)
        
        # Set the calendarId to 'primary' for the user's primary calendar
        calendar_id = 'primary'
        
        # Insert the event using the API key
        event = calendar_service.events().insert(calendarId=calendar_id, body=event_data).execute()
        print(f'Event created: {event.get("htmlLink")}')

    except HttpError as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    event_data = {
        'summary': 'Meeting with John',
        'description': 'Discuss project updates.',
        'start': {
            'dateTime': '2023-09-17T10:00:00+05:30',  # IST timezone offset (+5 hours and 30 minutes)
            'timeZone': 'Asia/Kolkata',  # Timezone for IST
        },
        'end': {
            'dateTime': '2023-09-17T11:00:00+05:30',  # IST timezone offset (+5 hours and 30 minutes)
            'timeZone': 'Asia/Kolkata',  # Timezone for IST
        },
    }

    create_calendar_event(event_data)
