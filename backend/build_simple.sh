#!/usr/bin/env bash
# Simplified build script for Render deployment

set -o errexit  # Exit on error

echo "🚀 Starting Render deployment (simplified)..."

echo "🐍 Python version:"
python --version

# Guard against unsupported Python versions (e.g., 3.13 not yet supported by SQLAlchemy 2.0.23)
PYVER=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
case "$PYVER" in
  3.11|3.10|3.12|3.13)
    echo "✅ Python $PYVER acceptable (SQLAlchemy 2.0.35+ supports 3.13)"
    ;;
  *)
    echo "❌ Python $PYVER is not supported for this project yet. Ensure runtime.txt pins 3.11."
    echo "   Add runtime.txt with 'python-3.11.9' in the service root (backend/) on Render."
    exit 1
    ;;
esac

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
python -c "import sqlalchemy; print(f'SQLAlchemy {sqlalchemy.__version__} OK')"

echo "🗄️ Setting up database..."
python deploy.py

echo "✅ Backend deployment complete!"
