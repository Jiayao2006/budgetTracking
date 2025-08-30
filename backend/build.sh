#!/bin/bash

echo "🚀 Starting Render deployment..."

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🗄️ Setting up database tables..."
python deploy.py

echo "✅ Deployment preparation complete!"
