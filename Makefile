# Makefile for Idea AI Project
.PHONY: help install dev test build deploy clean

# Variables
PYTHON := python3
PIP := pip3
NPM := npm
DOCKER := docker
DOCKER_COMPOSE := docker-compose
VENV := venv
BACKEND_DIR := backend
FRONTEND_DIR := frontend/web
SCRIPTS_DIR := scripts

# Colors
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Help
help:
	@echo "$(GREEN)🎯 دستورات موجود برای پروژه ایده AI:$(NC)"
	@echo ""
	@echo "$(BLUE)📦 نصب و راه‌اندازی:$(NC)"
	@echo "  make install          - نصب تمام وابستگی‌ها"
	@echo "  make install-backend  - نصب وابستگی‌های backend"
	@echo "  make install-frontend - نصب وابستگی‌های frontend"
	@echo ""
	@echo "$(BLUE)🚀 توسعه:$(NC)"
	@echo "  make dev              - اجرای کامل پروژه در حالت توسعه"
	@echo "  make dev-backend      - اجرای backend در حالت توسعه"
	@echo "  make dev-frontend     - اجرای frontend در حالت توسعه"
	@echo ""
	@echo "$(BLUE)🧪 تست:$(NC)"
	@echo "  make test             - اجرای تمام تست‌ها"
	@echo "  make test-backend     - اجرای تست‌های backend"
	@echo "  make test-frontend    - اجرای تست‌های frontend"
	@echo "  make coverage         - اجرای تست‌ها با گزارش coverage"
	@echo ""
	@echo "$(BLUE)🏗️ ساخت:$(NC)"
	@echo "  make build            - ساخت تمام بخش‌ها"
	@echo "  make build-backend    - ساخت backend"
	@echo "  make build-frontend   - ساخت frontend"
	@echo "  make docker-build     - ساخت images های Docker"
	@echo ""
	@echo "$(BLUE)🐳 Docker:$(NC)"
	@echo "  make docker-up        - اجرای پروژه با Docker"
	@echo "  make docker-down      - توقف پروژه Docker"
	@echo "  make docker-logs      - مشاهده لاگ‌های Docker"
	@echo ""
	@echo "$(BLUE)🔧 ابزارها:$(NC)"
	@echo "  make lint             - بررسی کد با linters"
	@echo "  make format           - فرمت کردن کد"
	@echo "  make type-check       - بررسی نوع‌ها (type checking)"
	@echo "  make migrations       - ایجاد migrations جدید"
	@echo "  make migrate          - اعمال migrations"
	@echo ""
	@echo "$(BLUE)🧹 پاک‌سازی:$(NC)"
	@echo "  make clean            - پاک‌سازی فایل‌های موقت"
	@echo "  make clean-all        - پاک‌سازی کامل"
	@echo ""

# Installation
install: install-backend install-frontend
	@echo "$(GREEN)✅ تمام وابستگی‌ها نصب شدند$(NC)"

install-backend:
	@echo "$(BLUE)📦 نصب وابستگی‌های Backend...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(YELLOW)Creating Python virtual environment...$(NC)"; \
		$(PYTHON) -m venv $(VENV); \
	fi
	@echo "$(YELLOW)Activating virtual environment...$(NC)"
	@. $(VENV)/bin/activate && \
		$(PIP) install --upgrade pip && \
		$(PIP) install -e .[dev,voice,ml] && \
		echo "$(GREEN)✅ وابستگی‌های Backend نصب شدند$(NC)"

install-frontend:
	@echo "$(BLUE)📦 نصب وابستگی‌های Frontend...$(NC)"
	@cd $(FRONTEND_DIR) && \
		$(NPM) install && \
		echo "$(GREEN)✅ وابستگی‌های Frontend نصب شدند$(NC)"

# Development
dev: dev-backend dev-frontend

dev-backend:
	@echo "$(BLUE)🚀 اجرای Backend در حالت توسعه...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	@echo "$(BLUE)🚀 اجرای Frontend در حالت توسعه...$(NC)"
	@cd $(FRONTEND_DIR) && \
		$(NPM) run dev

# Testing
test: test-backend test-frontend
	@echo "$(GREEN)✅ تمام تست‌ها اجرا شدند$(NC)"

test-backend:
	@echo "$(BLUE)🧪 اجرای تست‌های Backend...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		python -m pytest tests/ -v --cov=backend --cov-report=html

test-frontend:
	@echo "$(BLUE)🧪 اجرای تست‌های Frontend...$(NC)"
	@cd $(FRONTEND_DIR) && \
		$(NPM) test

coverage:
	@echo "$(BLUE)📊 اجرای تست‌ها با گزارش Coverage...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		python -m pytest tests/ -v --cov=backend --cov-report=term-missing --cov-report=html

# Building
build: build-backend build-frontend
	@echo "$(GREEN)✅ تمام بخش‌ها ساخته شدند$(NC)"

build-backend:
	@echo "$(BLUE)🏗️ ساخت Backend...$(NC)"
	@. $(VENV)/bin/activate && \
		$(PIP) install --upgrade build && \
		python -m build

build-frontend:
	@echo "$(BLUE)🏗️ ساخت Frontend...$(NC)"
	@cd $(FRONTEND_DIR) && \
		$(NPM) run build

# Docker
docker-build:
	@echo "$(BLUE)🐳 ساخت Images های Docker...$(NC)"
	@$(DOCKER_COMPOSE) build

docker-up:
	@echo "$(BLUE)🐳 اجرای پروژه با Docker...$(NC)"
	@$(DOCKER_COMPOSE) up -d

docker-down:
	@echo "$(YELLOW)⏹️ توقف پروژه Docker...$(NC)"
	@$(DOCKER_COMPOSE) down

docker-logs:
	@echo "$(BLUE)📋 مشاهده لاگ‌های Docker...$(NC)"
	@$(DOCKER_COMPOSE) logs -f

docker-restart:
	@echo "$(BLUE)🔄 راه‌اندازی مجدد Docker...$(NC)"
	@$(DOCKER_COMPOSE) restart

# Code Quality
lint:
	@echo "$(BLUE)🔍 بررسی کد با Linters...$(NC)"
	@. $(VENV)/bin/activate && \
		flake8 $(BACKEND_DIR) && \
		cd $(FRONTEND_DIR) && \
		$(NPM) run lint
	@echo "$(GREEN)✅ بررسی کد کامل شد$(NC)"

format:
	@echo "$(BLUE)🎨 فرمت کردن کد...$(NC)"
	@. $(VENV)/bin/activate && \
		black $(BACKEND_DIR) && \
		isort $(BACKEND_DIR)
	@cd $(FRONTEND_DIR) && \
		$(NPM) run format
	@echo "$(GREEN)✅ فرمت کردن کد کامل شد$(NC)"

type-check:
	@echo "$(BLUE)🔎 بررسی نوع‌ها (Type Checking)...$(NC)"
	@. $(VENV)/bin/activate && \
		mypy $(BACKEND_DIR)
	@echo "$(GREEN)✅ بررسی نوع‌ها کامل شد$(NC)"

# Database
migrations:
	@echo "$(BLUE)📝 ایجاد Migration جدید...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		alembic revision --autogenerate -m "$(message)"

migrate:
	@echo "$(BLUE)🔄 اعمال Migrations...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		alembic upgrade head

migrate-rollback:
	@echo "$(YELLOW)↩️ بازگردانی Migration...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		alembic downgrade -1

# Deployment
deploy: build docker-build docker-up
	@echo "$(GREEN)✅ استقرار کامل شد$(NC)"

deploy-prod:
	@echo "$(BLUE)☁️ استقرار در محیط production...$(NC)"
	@$(DOCKER_COMPOSE) -f docker-compose.prod.yml up -d

# AI Models
train-model:
	@echo "$(BLUE)🤖 آموزش مدل AI...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		python -m scripts.training.train

evaluate-model:
	@echo "$(BLUE)📊 ارزیابی مدل AI...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		python -m scripts.evaluation.evaluate

# Data Management
process-data:
	@echo "$(BLUE)📁 پردازش داده‌ها...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		python -m scripts.data.process

backup-data:
	@echo "$(BLUE)💾 پشتیبان‌گیری از داده‌ها...$(NC)"
	@bash $(SCRIPTS_DIR)/backup.sh

# Monitoring
monitor:
	@echo "$(BLUE)📈 راه‌اندازی مانیتورینگ...$(NC)"
	@bash $(SCRIPTS_DIR)/monitor.sh

logs:
	@echo "$(BLUE)📋 مشاهده لاگ‌ها...$(NC)"
	@tail -f backend/logs/idea-ai.log

# Setup
setup: install
	@echo "$(BLUE)⚙️ راه‌اندازی اولیه پروژه...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		python -c "from core.database import engine, Base; Base.metadata.create_all(bind=engine)"
	@cp .env.example .env
	@echo "$(GREEN)✅ راه‌اندازی اولیه کامل شد$(NC)"
	@echo "$(YELLOW)📝 لطفاً فایل .env را ویرایش کنید$(NC)"

# Cleaning
clean:
	@echo "$(YELLOW)🧹 پاک‌سازی فایل‌های موقت...$(NC)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".coverage" -delete
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@cd $(FRONTEND_DIR) && \
		rm -rf dist build .next .nuxt
	@echo "$(GREEN)✅ پاک‌سازی کامل شد$(NC)"

clean-all: clean
	@echo "$(YELLOW)🧹 پاک‌سازی کامل...$(NC)"
	@rm -rf $(VENV)
	@cd $(FRONTEND_DIR) && \
		rm -rf node_modules
	@$(DOCKER_COMPOSE) down -v --rmi all
	@echo "$(GREEN)✅ پاک‌سازی کامل شد$(NC)"

# Service Management
start-services:
	@echo "$(BLUE)🚀 راه‌اندازی سرویس‌ها...$(NC)"
	@$(DOCKER_COMPOSE) up -d redis postgres

stop-services:
	@echo "$(YELLOW)⏹️ توقف سرویس‌ها...$(NC)"
	@$(DOCKER_COMPOSE) down

# Health Check
health:
	@echo "$(BLUE)🏥 بررسی سلامت سرویس‌ها...$(NC)"
	@curl -f http://localhost:8000/health || echo "$(RED)❌ Backend unhealthy$(NC)"
	@curl -f http://localhost:3000 || echo "$(RED)❌ Frontend unhealthy$(NC)"
	@echo "$(GREEN)✅ بررسی سلامت کامل شد$(NC)"

# Documentation
docs:
	@echo "$(BLUE)📚 ساخت مستندات...$(NC)"
	@. $(VENV)/bin/activate && \
		cd docs && \
		make html

serve-docs:
	@echo "$(BLUE)🌐 راه‌اندازی مستندات...$(NC)"
	@. $(VENV)/bin/activate && \
		cd docs/_build/html && \
		python -m http.server 8001

# Security
security-check:
	@echo "$(BLUE)🔒 بررسی امنیتی...$(NC)"
	@. $(VENV)/bin/activate && \
		bandit -r $(BACKEND_DIR)
	@cd $(FRONTEND_DIR) && \
		$(NPM) audit

update-dependencies:
	@echo "$(BLUE)🔄 بروزرسانی وابستگی‌ها...$(NC)"
	@. $(VENV)/bin/activate && \
		$(PIP) install --upgrade -r requirements.txt
	@cd $(FRONTEND_DIR) && \
		$(NPM) update

# Database Management
db-shell:
	@echo "$(BLUE)🛠️ ورود به shell دیتابیس...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		python -m scripts.utils.db_shell

db-reset:
	@echo "$(RED)⚠️ بازنشانی دیتابیس (تمام داده‌ها پاک می‌شوند)...$(NC)"
	@read -p "آیا مطمئن هستید؟ (y/N): " confirm && \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		rm -f idea_ai.db && \
		python -c "from core.database import engine, Base; Base.metadata.create_all(bind=engine)" && \
		echo "$(GREEN)✅ دیتابیس بازنشانی شد$(NC)"; \
	else \
		echo "$(YELLOW)❌ عملیات لغو شد$(NC)"; \
	fi

# Version Management
bump-version:
	@echo "$(BLUE)🔢 افزایش نسخه...$(NC)"
	@. $(VENV)/bin/activate && \
		bump2version patch

bump-minor:
	@echo "$(BLUE)🔢 افزایش نسخه جزئی...$(NC)"
	@. $(VENV)/bin/activate && \
		bump2version minor

bump-major:
	@echo "$(BLUE)🔢 افزایش نسخه اصلی...$(NC)"
	@. $(VENV)/bin/activate && \
		bump2version major

# Development Tools
shell:
	@echo "$(BLUE)🐍 راه‌اندازی Python Shell...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		ipython

notebook:
	@echo "$(BLUE)📓 راه‌اندازی Jupyter Notebook...$(NC)"
	@. $(VENV)/bin/activate && \
		cd $(BACKEND_DIR) && \
		jupyter notebook

# Production
production-setup: install
	@echo "$(BLUE)☁️ راه‌اندازی محیط Production...$(NC)"
	@cp .env.production .env
	@. $(VENV)/bin/activate && \
		$(PIP) install .[prod]
	@echo "$(GREEN)✅ محیط Production راه‌اندازی شد$(NC)"

# Default target
.DEFAULT_GOAL := help
