import os
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel

# Load the API key from environment variables
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Define the router
router = APIRouter()

# Define request schema
class ChatRequest(BaseModel):
    question: str

# Function to stream the response from OpenAI API
async def get_openai_response(request: ChatRequest):
    try:
        # Call OpenAI API without streaming
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": request.question}]
        )

        # Extract the full response text
        content = response.choices[0].message.content
        return {"answer": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting OpenAI response: {str(e)}")

# Define the POST route for the full response
@router.post("/")
async def chat_with_gpt(request: ChatRequest):
    return await get_openai_response(request)
