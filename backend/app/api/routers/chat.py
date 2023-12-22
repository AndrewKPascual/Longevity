from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
from llama_index.llms.types import MessageRole
from llama_index.llms.base import ChatMessage
# Make sure to import VectorStoreIndex correctly based on your project's structure.

app = FastAPI()  # Use FastAPI's instance

class _Message(BaseModel):
    role: MessageRole
    content: str

class _ChatData(BaseModel):
    messages: List[_Message]

# Define a function to handle the chat logic.
async def handle_chat(chat_engine, last_message, messages):
    # Implement this function to handle the chat logic.
    # For example, you might call chat_engine.stream_chat(...) here,
    # but remember to adapt it to return the full response rather than streaming.
    pass

@app.post("/")  # Route at the root of the serverless function
async def chat(data: _ChatData):
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    last_message = data.messages.pop()
    if last_message.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )

    messages = [ChatMessage(role=m.role, content=m.content) for m in data.messages]

    # Initialize your chat engine with the correct parameters.
    index = VectorStoreIndex(...)  # Replace ... with actual initialization parameters.
    chat_engine = index.as_chat_engine(chat_mode='condense_plus_context', verbose=True)

    # Call the handle_chat function to process the messages and generate a response.
    response = await handle_chat(chat_engine, last_message, messages)

    # Return the response in a format that the frontend expects.
    return {"response": response}
