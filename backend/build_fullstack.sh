#!/usr/bin/env bash
# Build script for full-stacecho "� Moving frontend build to backend static folder..."
mkdir -p ../backend/static
cp -r dist/* ../backend/static/ Render deployment

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

echo "🌐 Installing Node.js without sudo on Render..."
# Install Node.js using nvm-like approach for Render (no sudo)
export NODE_VERSION=18.18.2
export NVM_DIR="$HOME/.nvm"
mkdir -p $NVM_DIR
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install $NODE_VERSION
nvm use $NODE_VERSION

# Print Node.js and npm versions
echo "Node.js version: $(node -v)"
echo "npm version: $(npm -v)"

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
