import requests
from datetime import datetime, timedelta
from uagents import Agent, Context, Protocol
from ai_engine import UAgentResponse, UAgentResponseType
import os

# agent=Agent(name="agent", seed="sender")
provider = Protocol(name="provider", version="1.1")
# Define models
class Response(Model):
    is_available: bool

class MatchingRequest(Model):
    phone: str
    email: str
    pick_up_address: str
    drop_address: str
    pick_up_date: str
    time: str
    duration_of_delivery: str
    maximum_delivery_price: str
    courier_providers: str
    
class BookingRequest(Model):
    start: str
    end: str
    consumer: str
    summary: str
    description: str
    is_gcal_event: bool = False

TWILIO_BASE_URL = "https://api.twilio.com/2010-04-01"
TWILIO_MESSAGES_ENDPOINT = f"{TWILIO_BASE_URL}/Accounts/{ACCOUNT_ID}/Messages.json"

basic_request_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

# Function to create a new event in the calendar
def create_new_event(event, token, attendees):
    request_headers = get_header(token)

    body = {
        "summary": f"Booking confirmed",
        "description": event.description,
        "start": {"dateTime": event.start},
        "end": {"dateTime": event.end},
        "attendees": attendees,
    }
    event_list_params = {"alwaysIncludeEmail": "true"}

    response = requests.post(
        basic_request_url, 
        headers=request_headers, 
        params=event_list_params, 
        json=body
    )
    if response.status_code == 200:
        print("Event Created Successfully.")
    else:
        print("Event creation failed. Status code:", response.status_code)

# Function to send a WhatsApp message
def send_whatsapp_message(phone_number: str, message: str):
    global WP_FROM_NUMBER
    if not WP_FROM_NUMBER.startswith("whatsapp:"):
        WP_FROM_NUMBER = f"whatsapp:{WP_FROM_NUMBER}"
    if not phone_number.startswith("whatsapp:"):
        phone_number = f"whatsapp:{phone_number}"
    
    data = {"From": WP_FROM_NUMBER, "To": phone_number, "Body": message}
    
    try:
        response = requests.post(TWILIO_MESSAGES_ENDPOINT, data=data, auth=(ACCOUNT_ID, AUTH_TOKEN))
        response.raise_for_status()
        print("WhatsApp message sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send WhatsApp message: {str(e)}")

# Function to fetch events from provider's calendar
def fetch_provider_events(date, token):
    request_headers = get_header(token)
    start_time = datetime.strptime(date, "%Y-%m-%d")
    end_time = start_time + timedelta(days=1)

    params = {
        "timeMin": start_time.isoformat() + "Z",
        "timeMax": end_time.isoformat() + "Z",
        "singleEvents": True,
        "orderBy": "startTime",
    }

    response = requests.get(
        basic_request_url,
        headers=request_headers,
        params=params,
    )
    if response.status_code == 200:
        events = response.json().get("items", [])
        return events
    else:
        print("Failed to fetch events. Status code:", response.status_code)
        return []

# Function to get request headers
def get_header(token: str):
    return {"Accept": "application/json", "Authorization": f"Bearer {token}"}

# Agent handler for responding to matching requests
@provider.on_message(model=MatchingRequest, replies={UAgentResponse})
async def book_provider(ctx: Context, sender: str, msg: MatchingRequest):
    ctx.logger.info(f"Received matching request: {msg}")

    # # Respond to the matching request
    # await ctx.send(sender, Response(is_available=is_available))
     
    # Check provider's availability by fetching events from the calendar
    events = fetch_provider_events(msg.date, ACCESS_TOKEN)
    is_available = True
    
         # Perform availability check based on fetched events
    for event in events:
        event_start = datetime.fromisoformat(event["start"]["dateTime"])
        event_end = datetime.fromisoformat(event["end"]["dateTime"])
        requested_start = datetime.strptime(msg.date + " " + msg.time, "%Y-%m-%d %I:%M %p")
        requested_end = requested_start + timedelta(hours=1)

        # Check if the requested time slot overlaps with any existing event
        if event_start <= requested_end and event_end >= requested_start:
            is_available = False
            break  # No need to continue checking if one event overlaps

    if is_available:
    
        # Assuming a 1-hour time slot for the appointment
        start_time = datetime.strptime(msg.date + " " + msg.time, "%Y-%m-%d %I:%M %p")
        end_time = start_time + timedelta(hours=1)
        
        # Create an event in the provider's calendar
        event = BookingRequest(
            start=start_time.isoformat(), 
            end=end_time.isoformat(), 
            # consumer=msg.consumer_name,
            summary=f"Delivery",
            description=f"Delivering to {msg.city} at {msg.time}",
            is_gcal_event=True,
        )

        create_new_event(event, CALENDAR_TOKEN, [EMAIL_ID])  # Replace with actual attendee

        # Send a WhatsApp message to the provider
        whatsapp_message = f"You have a booking for {msg.date} at {msg.time}."
        send_whatsapp_message(ctx.phone_number, whatsapp_message)
    
        # Respond to the matching request
        await ctx.send(sender, UAgentResponse(message="Provider is booked", type=UAgentResponseType.FINAL))
        
    else:
        # Provider is not available
        await ctx.send(sender, UAgentResponse(message="Provider is not available", type=UAgentResponseType.FINAL))
        
# Message handler for handling booking requests
# @agent.on_message(model=MatchingRequest, replies=Response)

# async def respond_to_adapter(ctx: Context, sender: str, msg: MatchingRequest):
#     ctx.logger.info(f"session in respond_to_adapter: {ctx.session}, sender: {sender}")
#     ctx.logger.info(f"Message from adapter: {msg}")
    
#     # Check provider's availability by fetching events from the calendar
#     events = fetch_provider_events(msg.date, ACCESS_TOKEN)
#     is_available = True
    
#     # Perform availability check based on fetched events
#     for event in events:
#         event_start = datetime.fromisoformat(event["start"]["dateTime"])
#         event_end = datetime.fromisoformat(event["end"]["dateTime"])
#         requested_start = datetime.strptime(msg.date + " " + msg.time, "%Y-%m-%d %I:%M %p")
#         requested_end = requested_start + timedelta(hours=1)

#         # Check if the requested time slot overlaps with any existing event
#         if event_start <= requested_end and event_end >= requested_start:
#             is_available = False
#             break  # No need to continue checking if one event overlaps
 
#     await ctx.send(sender, Response(is_available=is_available))

agent.include(provider)