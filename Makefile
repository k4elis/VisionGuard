.PHONY: help install dev-backend dev-frontend build up down logs clean

help:
	@echo "VisionGuard - Available Commands"
	@echo "================================"
	@echo "install         - Install backend dependencies"
	@echo "dev-backend     - Run backend in development mode"
	@echo "dev-frontend    - Run frontend in development mode"
	@echo "build           - Build Docker containers"
	@echo "up              - Start Docker containers"
	@echo "down            - Stop Docker containers"
	@echo "logs            - View Docker logs"
	@echo "clean           - Clean up generated files"

install:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install

dev-backend:
	. venv/bin/activate && python main.py

dev-frontend:
	cd frontend && npm run dev

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf venv
	rm -rf frontend/node_modules
	rm -rf frontend/build
