
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Use chat_service from service/chat_service.py
from service.chat_service import chat_service

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    user_id: str = "gaurav"

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    reply = chat_service(request.message, request.user_id)
    return {"reply": reply}

#uvicorn main:app --reload