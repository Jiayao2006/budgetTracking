#!/usr/bin/env bash
# Simple fullstack build script that uses Render's pre-installed Node

set -o errexit  # Exit on error

echo "🚀 Starting simplified full-stack Render deployment..."

echo "🐍 Python version:"
python --version

echo "📦 Installing Python dependencies (binary wheels only first pass)..."
pip install --upgrade pip

# Prefer wheels only to avoid building Rust (pydantic-core). If any wheel missing, retry without restriction.
if ! pip install --only-binary=:all: -r requirements.txt; then
    echo "⚠️ Some wheels unavailable; retrying allowing source builds for remaining packages..."
    pip install -r requirements.txt
fi

echo "📝 Verifying Python installation..."
python -c "import fastapi; print('FastAPI OK')"
python -c "import uvicorn; print('Uvicorn OK')"
python -c "import sqlalchemy; print(f'SQLAlchemy OK')"

echo "🗄️ Setting up database tables..."
python deploy.py

echo "🌐 Using Render's pre-installed Node.js..."
node --version
npm --version

# Check if frontend directory exists at the expected location
if [ -d "../frontend" ]; then
    echo "📁 Building frontend..."
    cd ../frontend

    echo "📦 Installing frontend dependencies..."
    npm install --legacy-peer-deps

    echo "🏗️ Building React app..."
    npm run build

    echo "📦 Moving frontend build to backend static folder..."
    mkdir -p ../backend/static
    cp -r dist/* ../backend/static/
    
    echo "📁 Listing static files..."
    ls -la ../backend/static/
    
    cd ../backend
else
    echo "⚠️ Frontend directory not found at ../frontend. Skipping frontend build."
    echo "⚠️ Will use existing static files if available."
fi

echo "✅ Full-stack deployment complete!"
