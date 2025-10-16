from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.endpoints import chat, analyze, voice, auth, training
from api.middleware.auth import AuthMiddleware
from api.middleware.logging import LoggingMiddleware
from core.config import settings
from core.database import engine, Base
import logging

# Create database tables
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ایده AI API",
    description="API برای دستیار هوش مصنوعی پیشرفته ایده",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middlewares
app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(training.router, prefix="/api/v1/training", tags=["training"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(analyze.router, prefix="/api/v1/analyze", tags=["analyze"])
app.include_router(voice.router, prefix="/api/v1/voice", tags=["voice"])

@app.get("/")
async def root():
    return {
        "message": "خوش آمدید به API ایده AI",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@app.get("/api/v1/models")
async def get_available_models():
    """دریافت لیست مدل‌های موجود"""
    return {
        "models": [
            {"id": "aria", "name": "ایده (مدل اختصاصی)", "type": "text"},
            {"id": "gpt4", "name": "GPT-4 Turbo", "type": "text"},
            {"id": "claude", "name": "Claude 3 Opus", "type": "text"},
            {"id": "gemini", "name": "Google Gemini Pro", "type": "text"},
            {"id": "llama", "name": "Meta LLaMA 3", "type": "text"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)