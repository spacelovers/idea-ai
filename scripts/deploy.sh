#!/bin/bash

echo "🚀 استقرار پروژه ایده AI..."

# Build Docker images
echo "🐳 ساخت images های Docker..."
docker-compose build

# Run tests
echo "🧪 اجرای تست‌ها..."
cd backend
python -m pytest tests/ -v

# Deploy
echo "☁️ استقرار..."
docker-compose up -d

echo "✅ استقرار کامل شد!"
echo "🌐 Backend: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"