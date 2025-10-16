from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

router = APIRouter()

class ChatMessage(BaseModel):
    id: str
    content: str
    sender: str  # 'user' or 'ai'
    timestamp: datetime
    model: Optional[str] = "aria"

class ChatRequest(BaseModel):
    message: str
    model: str = "aria"
    conversation_id: Optional[str] = None
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    message_id: str
    model: str
    timestamp: datetime

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """ارسال پیام و دریافت پاسخ از AI"""
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # Process message through AI service
        # This would connect to actual AI models
        ai_response = f"پاسخ به: {request.message} (مدل: {request.model})"

        return ChatResponse(
            response=ai_response,
            conversation_id=conversation_id,
            message_id=str(uuid.uuid4()),
            model=request.model,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{conversation_id}")
async def get_chat_history(conversation_id: str):
    """دریافت تاریخچه مکالمه"""
    # This would fetch from database
    return {
        "conversation_id": conversation_id,
        "messages": [],
        "total_messages": 0
    }

@router.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """حذف مکالمه"""
    return {"message": "مکالمه با موفقیت حذف شد", "conversation_id": conversation_id}