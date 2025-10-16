#!/bin/bash

echo "🚀 راه‌اندازی پروژه ایده AI..."

# Create virtual environment
echo "📦 ایجاد محیط مجازی Python..."
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
echo "📥 نصب dependencies های Backend..."
cd backend
pip install -r requirements.txt

# Install frontend dependencies
echo "📥 نصب dependencies های Frontend..."
cd ../frontend/web
npm install

echo "✅ راه‌اندازی کامل شد!"
echo "🎯 برای اجرای Backend: cd backend && uvicorn api.main:app --reload"
echo "🎯 برای اجرای Frontend: cd frontend/web && npm run dev"