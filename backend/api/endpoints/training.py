from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import io
import asyncio
from datetime import datetime
import uuid

router = APIRouter()

class TrainingRequest(BaseModel):
    dataset_id: str
    model_name: str = "aria"
    epochs: int = 10
    learning_rate: float = 0.001

class TrainingStatus(BaseModel):
    id: str
    status: str  # pending, training, completed, failed
    progress: float
    start_time: datetime
    end_time: Optional[datetime]
    message: str

# ذخیره وضعیت آموزش‌ها
training_statuses = {}

@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    try:
        # بررسی نوع فایل
        if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
            raise HTTPException(status_code=400, detail="Only Excel and CSV files are supported")

        # خواندن فایل
        contents = await file.read()

        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))

        # بررسی ساختار دیتاست
        required_columns = ['question', 'answer']  # ستون‌های مورد انتظار
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400,
                detail=f"Dataset must contain columns: {required_columns}"
            )

        # ایجاد شناسه برای دیتاست
        dataset_id = str(uuid.uuid4())

        # ذخیره دیتاست (در حالت واقعی در دیتابیس ذخیره شود)
        dataset_info = {
            "id": dataset_id,
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns),
            "upload_time": datetime.utcnow()
        }

        return {
            "dataset_id": dataset_id,
            "message": "Dataset uploaded successfully",
            "info": dataset_info
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing dataset: {str(e)}")

@router.post("/start-training")
async def start_training(request: TrainingRequest, background_tasks: BackgroundTasks):
    training_id = str(uuid.uuid4())

    training_status = TrainingStatus(
        id=training_id,
        status="pending",
        progress=0.0,
        start_time=datetime.utcnow(),
        message="Training queued"
    )

    training_statuses[training_id] = training_status

    # شروع آموزش در پس‌زمینه
    background_tasks.add_task(train_model, training_id, request)

    return {
        "training_id": training_id,
        "message": "Training started successfully"
    }

@router.get("/training-status/{training_id}")
async def get_training_status(training_id: str):
    if training_id not in training_statuses:
        raise HTTPException(status_code=404, detail="Training not found")

    return training_statuses[training_id]

async def train_model(training_id: str, request: TrainingRequest):
    """تابع شبیه‌سازی شده برای آموزش مدل"""
    try:
        training_statuses[training_id].status = "training"
        training_statuses[training_id].message = "Starting model training..."

        # شبیه‌سازی فرآیند آموزش
        for epoch in range(request.epochs):
            await asyncio.sleep(1)  # شبیه‌سازی زمان آموزش

            progress = (epoch + 1) / request.epochs * 100
            training_statuses[training_id].progress = progress
            training_statuses[training_id].message = f"Training epoch {epoch + 1}/{request.epochs}"

            # شبیه‌سازی خطاهای احتمالی
            if progress > 50 and progress < 60:
                if request.model_name == "custom":
                    training_statuses[training_id].status = "failed"
                    training_statuses[training_id].message = "Training failed due to convergence issues"
                    return

        # تکمیل آموزش
        training_statuses[training_id].status = "completed"
        training_statuses[training_id].progress = 100.0
        training_statuses[training_id].end_time = datetime.utcnow()
        training_statuses[training_id].message = "Training completed successfully"

    except Exception as e:
        training_statuses[training_id].status = "failed"
        training_statuses[training_id].message = f"Training failed: {str(e)}"