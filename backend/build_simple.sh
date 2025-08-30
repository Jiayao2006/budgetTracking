#!/usr/bin/env bash
# Simplified build script for Render deployment

set -o errexit  # Exit on error

echo "🚀 Starting Render deployment (simplified)..."

echo "🐍 Python version:"
python --version

echo "📦 Installing Python dependencies (binary wheels only first pass)..."
pip install --upgrade pip

# Prefer wheels only to avoid building Rust (pydantic-core). If any wheel missing, retry without restriction.
if ! pip install --only-binary=:all: -r requirements.txt; then
	echo "⚠️ Some wheels unavailable; retrying allowing source builds for remaining packages..."
	pip install -r requirements.txt
fi

echo "📝 Verifying installation..."
python -c "import fastapi; print('FastAPI OK')"
python -c "import uvicorn; print('Uvicorn OK')"

echo "🗄️ Setting up database..."
python deploy.py

echo "✅ Backend deployment complete!"
