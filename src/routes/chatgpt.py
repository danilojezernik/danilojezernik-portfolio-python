from fastapi import APIRouter, HTTPException
from openai import OpenAI

from src import env
from src.domain.chat_request import ChatRequest

# Load the API key from environment variables to authenticate with OpenAI
client = OpenAI(api_key=env.OPENAI_API_KEY)

# Define the router for your FastAPI app, allowing you to group routes
router = APIRouter()

# Asynchronous function to handle the call to the OpenAI API
# It takes the 'ChatRequest' object and passes the question to OpenAI's GPT-4 model
async def get_openai_response(request: ChatRequest):
    try:
        # Call the OpenAI API to generate a completion based on the user's question
        # The "model" specifies which version of GPT is used, and "messages" contains the user input
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": request.question}]
        )

        # Extract the response text from OpenAI's reply (the first choice in the list)
        content = response.choices[0].message.content
        return {"answer": content}  # Return the answer to the user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting OpenAI response: {str(e)}")


# Define a POST route for your FastAPI app. When a POST request is made to this route, it will
# call the 'chat_with_gpt' function and return the response generated by GPT-4.
@router.post("/")
async def chat_with_gpt(request: ChatRequest):
    # Forward the request to the OpenAI API handler function and return its response
    return await get_openai_response(request)
