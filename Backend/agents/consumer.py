import requests
from datetime import datetime, timedelta
from uagents import Context
from pydantic import BaseModel
import os

# Define models
class Response(BaseModel):
    is_available: bool

class MatchingRequest(BaseModel):
    date: str
    time: str
    provider_name: str

class BookingRequest(BaseModel):
    start: str
    end: str
    consumer: str
    summary: str
    description: str
    is_gcal_event: bool = False

basic_request_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

# Mock functions for calendar and WhatsApp
def create_new_event(event, token, attendees):
    request_headers = get_header(token)

    body = {
        "summary": f"Booking confirmed for {event.summary}",
        "description": event.description,
        "start": {"dateTime": event.start},
        "end": {"dateTime": event.end},
        "attendees": attendees,
    }
    event_list_params = {"alwaysIncludeEmail": "true"}

    response = requests.post(
        basic_request_url, headers=request_headers, params=event_list_params, json=body
    )
    if response.status_code == 200:
        print("Event Created Successfully.")
    else:
        print("Event creation failed. Status code:", response.status_code)

WP_FROM_NUMBER = "+447897026355"
base_url = "https://api.twilio.com/2010-04-01"
endpoint = f"{base_url}/Accounts/{ACCOUNT_ID}/Messages.json"

def send_whatsapp_message(phone_number: str, message: str):
    global WP_FROM_NUMBER
    if not WP_FROM_NUMBER.startswith("whatsapp:"):
        WP_FROM_NUMBER = f"whatsapp:{WP_FROM_NUMBER}"
    if not phone_number.startswith("whatsapp:"):
        phone_number = f"whatsapp:{phone_number}"
    
    data = {"From": WP_FROM_NUMBER, "To": PHONE_NUMBER, "Body": message}
    
    try:
        response = requests.post(endpoint, data=data, auth=(ACCOUNT_ID, AUTH_TOKEN))
        response.raise_for_status()
        print("WhatsApp message sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send WhatsApp message: {str(e)}")

# Consumer Agent
@agent.on_message(model=MatchingRequest, replies=Response)
async def respond_to_consumer(ctx: Context, sender: str, msg: MatchingRequest):
    ctx.logger.info(f"Received request from consumer: {msg}")

    # Create an event in the consumer's calendar
    event_description = f"Meeting with {msg.provider_name}"
    event = BookingRequest(
        start=msg.date + "T" + msg.time,  # Combine date and time for start
        end=(datetime.strptime(msg.date, "%Y-%m-%d") + timedelta(hours=1)).isoformat(),  # End time, e.g., 1 hour later
        consumer="Consumer Name",  # Replace with actual consumer name
        summary=event_description,
        description="Description of the meeting",
        is_gcal_event=True,
    )

    create_new_event(event, CALENDER_TOKEN , EMAIL_ID)  # Replace with actual attendee

        # Send a message to the user on WhatsApp
    whatsapp_message = f"Provider {msg.provider_name} is matched for {msg.date} at {msg.time}. Event created in your calendar."
    send_whatsapp_message(ctx.phone_number, whatsapp_message)

        # Respond to the consumer
    await ctx.send(sender, Response(is_available=True))
    
# # Example usage
# if __name__ == "__main__":
#     # Mock context data
#     ctx = Context(calendar_token="your_calendar_token_here", phone_number="consumer_phone_number_here")

#     # Example matching request data
#     matching_request_data = {
#         "date": "2024-04-20",
#         "time": "10:00 AM",
#         "provider_name": "Example Provider"
#     }

#     # Convert data to MatchingRequest model
#     matching_request = MatchingRequest(**matching_request_data)

#     # Simulate message handling
#     # await respond_to_consumer(ctx, "Consumer", matching_request)
