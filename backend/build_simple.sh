#!/usr/bin/env bash
# Simplified build script for Render deployment

set -o errexit  # Exit on error

echo "🚀 Starting Render deployment (simplified)..."

echo "🐍 Python version:"
python --version

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install --only-binary=all fastapi==0.104.1 uvicorn==0.24.0 sqlalchemy==2.0.23 pydantic==2.4.2 pydantic-core==2.10.1 python-multipart==0.0.6 python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 bcrypt==4.0.1 python-dotenv==1.0.0 psycopg2-binary==2.9.9 alembic==1.13.0

echo "📝 Verifying installation..."
python -c "import fastapi; print('FastAPI OK')"
python -c "import uvicorn; print('Uvicorn OK')"

echo "🗄️ Setting up database..."
python deploy.py

echo "✅ Backend deployment complete!"
