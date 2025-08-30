# PostgreSQL Deployment Guide

## 🎯 Current Status
Your backend now supports both SQLite (development) and PostgreSQL (production)!

## 🔄 How It Works
- **No DATABASE_URL set**: Uses SQLite (development mode)
- **DATABASE_URL set**: Uses PostgreSQL (production mode)

## 🚀 Next Steps to Get PostgreSQL DATABASE_URL

### Option 1: Render (Recommended - Free)
1. Go to [render.com](https://render.com) and sign up
2. Create New → PostgreSQL
3. Fill details:
   - Name: `budget-tracker-db`
   - Database: `budget_tracker`
   - User: `budget_user`
   - Plan: **Free**
4. Copy the "External Database URL"
5. Set as environment variable: `DATABASE_URL=postgresql://...`

### Option 2: Supabase (Also Free)
1. Go to [supabase.com](https://supabase.com) and sign up
2. New project → Choose name and password
3. Settings → Database → Copy "URI" connection string
4. Set as environment variable: `DATABASE_URL=postgresql://...`

## 🧪 Testing Locally with PostgreSQL

### Create .env file:
```bash
# backend/.env
DATABASE_URL=postgresql://your_database_url_here
```

### Test the connection:
```bash
cd backend
python setup_database.py
```

### Start the server:
```bash
python -m uvicorn app.main:app --reload
```

## 🌐 Production Deployment

### Environment Variables to Set:
```
DATABASE_URL=postgresql://your_postgres_url
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
```

### Deploy Commands:
```bash
# Install dependencies
pip install -r requirements.txt

# Run database setup
python setup_database.py

# Start server
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## ✅ Benefits of This Setup

1. **Development**: Still uses SQLite - no changes needed
2. **Production**: Uses PostgreSQL automatically when DATABASE_URL is set
3. **Flexible**: Easy to switch between databases
4. **Persistent**: PostgreSQL data survives deployments
5. **Scalable**: Supports multiple concurrent users

## 🎉 Ready for Production!

Your app is now ready to deploy to any cloud platform with PostgreSQL support!
