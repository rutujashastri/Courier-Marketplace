from fastapi import FastAPI,  Request
from twilio.rest import Client

account_sid = 'ACf7c673f098935fbc462bf374eb171008'
auth_token = 'ebc59cb9a2d8e5b93cb62ba2c6e65d06'
client = Client(account_sid, auth_token)
app = FastAPI()

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    # Extract the necessary fields from the JSON data
    message_sid = data.get("MessageSid")
    from_number = data.get("From")
    to_number = data.get("To")
    body = data.get("Body")
    num_media = data.get("NumMedia")

    # Handle media-related parameters if media is present
    media_content_types = []
    media_urls = []

    if num_media > 0:
        for n in range(num_media):
            media_content_types.append(data.get(f"MediaContentType{n}"))
            media_urls.append(data.get(f"MediaUrl{n}"))

        # Process media content types and URLs here

    # Log the received message (you can replace this with your desired logic)
    print(f"Received message from {from_number} to {to_number}: {body}")
    return {"message": "Message received successfully"}

@app.get("/")
def get():
    return {"message": "Message received successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
