#!/usr/bin/env bash
# Build script for full-stack Render deployment

set -o errexit  # Exit on error

echo "🚀 Starting full-stack Render deployment..."

echo "🐍 Python version:"
python --version

echo "📦 Upgrading pip and build tools..."
python -m pip install --upgrade pip setuptools wheel

echo "📦 Installing Python dependencies with pre-compiled wheels..."
python -m pip install --only-binary=all -r requirements.txt || 
python -m pip install --no-cache-dir -r requirements.txt

echo "📝 Verifying Python installation..."
python -c "import fastapi; print('FastAPI installed')"
python -c "import uvicorn; print('Uvicorn installed')"
python -c "import sqlalchemy; print('SQLAlchemy installed')"

echo "🗄️ Setting up database tables..."
python deploy.py

echo "🌐 Installing Node.js..."
# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

echo "📁 Building frontend..."
cd ../frontend

echo "📦 Installing frontend dependencies..."
npm install --legacy-peer-deps

echo "🏗️ Building React app..."
npm run build

echo "� Moving frontend build to backend static folder..."
mkdir -p ../backend/static
cp -r dist/* ../backend/static/

echo "📁 Listing static files..."
ls -la ../backend/static/

cd ../backend

echo "✅ Full-stack deployment complete!"
echo "🎉 Frontend built and ready to serve!"
