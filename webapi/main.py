
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Use chat_service from service/chat_service.py
from service.chat_service import chat_service
from service.memory_service import get_user_memories

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
    user_id: str

class MemoriesRequest(BaseModel):
    user_id: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    reply = chat_service(request.message, request.user_id)
    return {"reply": reply}

@app.get("/api/memories")
async def get_memories(user_id: str):
    return get_user_memories(user_id)

#uvicorn main:app --reload