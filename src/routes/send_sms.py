import os
import smtplib

from fastapi import APIRouter, HTTPException

from pydantic import BaseModel
from starlette.responses import JSONResponse

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from src import env

router = APIRouter()

account_sid = env.ACCOUNT_SID
auth_token = env.AUTH_TOKEN
client = Client(account_sid, auth_token)

# Define a Pydantic model for request body
class SMSRequest(BaseModel):
    phone_number: str
    message_body: str

@router.post('/send_sms_alert', operation_id='send_sms_alert')
async def send_sms_alert(sms_request: SMSRequest):
    try:
        message = client.messages.create(
            from_=env.PHONE_NUMBER_TWILIO,
            to=sms_request.phone_number,
            body=sms_request.message_body
        )
        return {'message': message.body}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_sms_response", operation_id='get_sms_response')
async def get_sms_response():
    resp = MessagingResponse()
    resp.message("Robots are coming! Hide!")
    return str(resp)

@router.get('/smtp')
async def send_sms():
    recipient = '+38670786664@carrier.com'  # Carrier's email-to-SMS gateway
    message = 'Hello from Python!'

    try:
        # Send email-to-SMS via SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(env.EMAIL, env.PASSWORD)
            server.sendmail(env.EMAIL, recipient, message)

        return JSONResponse(content={"message": "SMS sent successfully"}, status_code=200)

    except Exception as e:
        # Handle potential errors during SMTP process
        return JSONResponse(content={"error": str(e)}, status_code=500)