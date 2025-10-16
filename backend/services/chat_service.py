from typing import List, Dict, Any
from datetime import datetime
import uuid
from services.ai_services import ai_service

class ChatService:
    def __init__(self):
        self.conversations: Dict[str, List[Dict]] = {}

    async def send_message(self, message: str, model: str = "aria", conversation_id: str = None) -> Dict[str, Any]:
        """ارسال پیام و دریافت پاسخ"""
        # Generate conversation ID if not provided
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        # Get AI response
        ai_response = await ai_service.process_message(message, model)

        # Store message in conversation history
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        message_data = {
            "id": str(uuid.uuid4()),
            "content": message,
            "sender": "user",
            "timestamp": datetime.now(),
            "model": model
        }

        response_data = {
            "id": str(uuid.uuid4()),
            "content": ai_response,
            "sender": "ai",
            "timestamp": datetime.now(),
            "model": model
        }

        self.conversations[conversation_id].extend([message_data, response_data])

        return {
            "response": ai_response,
            "conversation_id": conversation_id,
            "message_id": response_data["id"],
            "model": model,
            "timestamp": datetime.now()
        }

    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """دریافت تاریخچه مکالمه"""
        return self.conversations.get(conversation_id, [])

    def delete_conversation(self, conversation_id: str) -> bool:
        """حذف مکالمه"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False

# Singleton instance
chat_service = ChatService()