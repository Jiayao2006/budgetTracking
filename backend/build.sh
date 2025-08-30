#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "🚀 Starting Render deployment..."

echo "� Python version:"
python --version

echo "�📦 Upgrading pip..."
python -m pip install --upgrade pip

echo "📦 Installing Python dependencies..."
python -m pip install -r requirements.txt

echo "📝 Verifying installation..."
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"
python -c "import uvicorn; print('Uvicorn: OK')"
python -c "import sqlalchemy; print(f'SQLAlchemy: {sqlalchemy.__version__}')"

echo "🗄️ Setting up database tables..."
python deploy.py

echo "✅ Deployment preparation complete!"
