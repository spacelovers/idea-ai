from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class BaseRequest(BaseModel):
    """مدل پایه برای درخواست‌ها"""
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatMessageRequest(BaseRequest):
    message: str = Field(..., min_length=1, max_length=4000)
    model: str = Field(default="aria")
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class AnalysisRequest(BaseRequest):
    text: str = Field(..., min_length=1)
    analysis_type: str = Field(default="sentiment")
    options: Optional[Dict[str, Any]] = None

class VoiceRequest(BaseRequest):
    audio_data: Optional[str] = None  # base64 encoded audio
    text: Optional[str] = None
    language: str = Field(default="fa")
    voice: str = Field(default="default")