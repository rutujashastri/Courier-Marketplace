from __future__ import print_function
from fastapi import FastAPI, HTTPException
from twilio.rest import Client
from dotenv import load_dotenv
from databases import Database
from sqlalchemy import create_engine, Column, String, MetaData, Table, JSON, Boolean, DECIMAL, inspect
from fastapi.middleware.cors import CORSMiddleware
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from uagents import Agent, Model
import uuid
import os
import requests
import os.path

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.readonly']

def createEvent():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

            # creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    event = {
    'summary': 'Courier Delivery event',
    'location': 'Pune Institute of Computer Technology, Pune',
    'description': 'Courier Package to be delivered soon',
    'start': {
        'dateTime': '2024-05-26T15:00:00+05:30',
        'timeZone': 'Asia/Kolkata',
    },
    'end': {
        'dateTime': '2024-05-28T21:30:00+05:30',
        'timeZone': 'Asia/Kolkata',
    },
    'attendees': [
        {'email': 'yash.pande@fetch.ai', 'displayName': 'Yash Pande'},
        # {'email': 'shreyal.nagle@fetch.ai', 'displayName': 'Shreyal Nagle'},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
        ],
    },
}


    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

app = FastAPI()

# CORS setup
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ConsumerAgentMapping(Model):
    email: str
    agent_address: str

# Load environment variables
load_dotenv()

# Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
verify_sid = os.getenv("VERIFY_SID")

# Twilio client
client = Client(account_sid, auth_token)

# Database setup
DATABASE_URL = "postgresql://user:password@localhost:5432/courier-marketplace"
database = Database(DATABASE_URL)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("user_id", String, primary_key=True, index=True),
    Column("name", String(255)),
    Column("phone_number", String(20)),
    Column("email", String(255)),
    Column("agent_address", String(255)),
    Column("calendar_permission_file", JSON),
    Column("is_courier", Boolean),
    Column("fast_price", DECIMAL(10, 2)),
    Column("normal_pace_price", DECIMAL(10, 2)),
    Column("slow_price", DECIMAL(10, 2)),
)

engine = create_engine(DATABASE_URL)

# Check if the 'users' table exists, if not, create it
inspector = inspect(engine)
if not inspector.has_table("users"):
    metadata.create_all(engine)


@app.on_event("startup")
async def startup_event():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()


@app.post("/send-otp")
async def send_otp(data: dict):
    phone_number = data.get("phone_number")
    if not phone_number:
        raise HTTPException(
            status_code=422, detail="Invalid data: phone_number is required"
        )

    # Send OTP using Twilio
    otp_verification = client.verify.v2.services(verify_sid).verifications.create(
        to=phone_number, channel="sms"
    )
    print(data)

    return {"status": "OTP sent successfully"}

token_var = ""

def settoken(token):
    global token_var
    token_var = token

def gettoken():
    global token_var
    return token_var


def get_agent_address():
    token = gettoken()
    try:
        response = requests.get("https://agentverse.ai/v1/hosting/agents", headers={
            "Authorization": f"bearer {token}"

        })

        if response.status_code == 200:
            agent_data = response.json()
            print("Agent Data:", agent_data)

            if 'objects' in agent_data and isinstance(agent_data['objects'], list) and agent_data['objects']:
                
                first_agent = agent_data['objects'][0]
                return first_agent.get('address', 'Agent address not found')
            else:
                return "Agent address not found"
        else:
            return "Failed to retrieve agent address"

        

    except Exception as e:
        return str(e)


@app.post("/verify-otp")
async def verify_otp(data: dict):
    phone_number = data.get("phone_number")
    otp_code = data.get("otp_code")
    email = data.get("emailID", None)
    token = data.get("token")
    settoken(token)
    # print(token, email, phone_number, otp_code)

    if not phone_number or not otp_code:
        raise HTTPException(
            status_code=422, detail="Invalid data: phone_number and otp_code are required"
        )

    try:
        # Verify OTP using Twilio
        verification_check = client.verify.v2.services(verify_sid).verification_checks.create(
            to=phone_number, code=otp_code
        )

        # If verification is successful, send WhatsApp message and return success status
        if verification_check.status == "approved":
            # Your code for sending a WhatsApp message
            message = client.messages.create(
                from_="whatsapp:+447883319771",
                body="Welcome to Courier Marketplace",
                to=f"whatsapp:{phone_number}",
            )
            print(message.sid)

            return {"status": "OTP verification successful and welcome message sent"}
        else:
            raise HTTPException(status_code=400, detail="Invalid OTP")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/register-user")
async def register_user(data: dict):
    # Extract data from the request
    name = data.get("name")
    role = data.get("role")
    fast_price = data.get("fast_price")
    normal_pace_price = data.get("normal_pace_price")
    slow_price = data.get("slow_price")
    phone_number = data.get("phone_number")
    email = data.get("emailID")
    calendar_token = data.get("calendar_token")
    token1 = gettoken()
    print("Token: ",token1)

    # Handle role-specific logic
    if role == "consumer":
        # If the role is consumer, set courier-related fields to None
        fast_price = None
        normal_pace_price = None
        slow_price = None
        agent_name = "Consumer agent"
    elif role == "courierProvider":
        agent_name = "Provider agent"
    else:
        agent_name = "My newest agent"

    is_courier = True if role == "courierProvider" else False
    data = {"name": agent_name}
    response = requests.post("https://agentverse.ai/v1/hosting/agents", json=data, headers={
        "Authorization": f"bearer {token1}"
    })
    print ("response: "+str(response))
    agent_address = get_agent_address()
    print(agent_address)
    adapter_agent_address="agent1qg2z25gcuq7xkras5a4tanr7z9uvclhzqc7m0356s7e255lq38wqqx4dqqm"
    agent= Agent(name=agent_name, seed=agent_address)
    await agent._ctx.send(adapter_agent_address, ConsumerAgentMapping(email=email, agent_address=agent_address))

    try:
        # Perform database insertion
        async with database.transaction():
            user_id = str(uuid.uuid4())
            await database.execute(users.insert().values(
                user_id=user_id,
                name=name,
                phone_number=phone_number,
                email=email,
                agent_address=agent_address,
                calendar_permission_file= calendar_token,
                is_courier=is_courier,
                fast_price=fast_price,
                normal_pace_price=normal_pace_price,
                slow_price=slow_price,
            ))
            createEvent()
            # Check if the request was successful
            if response.status_code == 200:
                return {"status": "User registered successfully"}
            else:
                raise HTTPException(
                    status_code=400, detail="Failed to register user's agent")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application
    uvicorn.run(app, host="127.0.0.1", port=8001)
