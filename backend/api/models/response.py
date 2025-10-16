from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class BaseResponse(BaseModel):
    """مدل پایه برای پاسخ‌ها"""
    success: bool = True
    message: Optional[str] = None
    timestamp: datetime = datetime.now()

class ChatResponse(BaseResponse):
    response: str
    conversation_id: str
    message_id: str
    model: str
    tokens_used: Optional[int] = None

class AnalysisResponse(BaseResponse):
    analysis_type: str
    results: Dict[str, Any]
    confidence: float
    processing_time: Optional[float] = None

class VoiceResponse(BaseResponse):
    text: Optional[str] = None
    audio_url: Optional[str] = None
    confidence: Optional[float] = None
    language: str = "fa"

class ErrorResponse(BaseResponse):
    success: bool = False
    error_code: str
    details: Optional[Dict[str, Any]] = None