#!/usr/bin/env bash
# Full-stack build script for Render deployment

set -o errexit  # Exit on error

echo "🚀 Starting full-stack Render deployment..."

echo "🐍 Python version:"
python --version

echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

echo "📦 Installing Python dependencies..."
python -m pip install -r requirements.txt

echo "📝 Verifying Python installation..."
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"
python -c "import uvicorn; print('Uvicorn: OK')"
python -c "import sqlalchemy; print(f'SQLAlchemy: {sqlalchemy.__version__}')"

echo "🗄️ Setting up database tables..."
python deploy.py

echo "🌐 Building frontend..."
cd ../frontend

echo "📦 Installing Node.js dependencies..."
npm install

echo "🏗️ Building React app for production..."
npm run build

echo "📁 Moving frontend build to backend static folder..."
mkdir -p ../backend/static
cp -r dist/* ../backend/static/

cd ../backend

echo "✅ Full-stack deployment preparation complete!"
