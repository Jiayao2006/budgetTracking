# Budget Tracking Application

A responsive, mobile-friendly budget tracking web application with dashboard analytics, spending management, and interactive calendar.

## ✨ Features

✅ **Responsive Design**: Bootstrap-based UI that works on desktop, tablet, and mobile  
✅ **Dashboard Analytics**: Monthly spending totals, daily averages, top spending categories with icons  
✅ **Add Spending**: Modern form with date picker, category selection, location, and notes  
✅ **Interactive Calendar**: Visual calendar showing daily spending amounts with badges  
✅ **Edit Spending**: Click edit button to modify any existing spending entry  
✅ **Delete Spending**: Remove spending entries with confirmation modal  
✅ **Real-time Updates**: Dashboard and calendar refresh instantly when data changes  
✅ **Persistent Storage**: SQLite database for reliable data persistence  
✅ **Mobile Optimized**: Touch-friendly interface with responsive layout

## 🎨 Design Features

- **Bootstrap 5**: Modern, responsive component library
- **React Icons**: Intuitive icons for better user experience  
- **Color-coded Categories**: Different badge colors for spending categories
- **Card-based Layout**: Clean, organized information presentation
- **Modal Confirmations**: Safe deletion with user confirmation
- **Inline Editing**: Edit spending details directly in the calendar view

## 🛠 Technology Stack

**Backend**: FastAPI, SQLAlchemy, SQLite, CORS enabled  
**Frontend**: React + TypeScript + Vite, Bootstrap, react-calendar  
**Icons**: React Icons (Font Awesome)  
**Database**: SQLite with automatic table creation

## 🚀 Quick Start

### 1. Backend Setup

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install fastapi uvicorn[standard] sqlalchemy
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```cmd
cd frontend
npm install
npm run dev
```

### 3. Access the Application

- **Frontend**: http://localhost:5173 (or 5174 if 5173 is in use)
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📱 Usage Guide

### Dashboard
- View monthly spending total with money icon
- See daily average with calendar icon  
- Check top spending categories with tags icon

### Adding Spending
- Fill out the form with amount, date, category, location, and optional description
- Categories include: Food, Fashion, Transportation, Entertainment, Health, Education, Utilities, Shopping, Other
- Form resets automatically after submission

### Calendar Management
- **View**: Click any date to see spending details for that day
- **Edit**: Click the edit (pencil) icon on any spending item to modify it
- **Delete**: Click the trash icon and confirm to remove a spending entry
- **Visual Indicators**: Red badges show total spending amounts on calendar dates

### Mobile Experience
- Responsive design adapts to screen size
- Touch-friendly buttons and forms
- Scrollable spending lists on mobile
- Optimized calendar view for smaller screens

## 🔧 API Endpoints

- `GET /spendings/dashboard` - Dashboard statistics
- `POST /spendings` - Create new spending
- `PUT /spendings/{id}` - Update existing spending
- `DELETE /spendings/{id}` - Delete spending
- `GET /spendings` - List all spendings
- `GET /spendings/date/{date}` - Get spendings for specific date

## 💾 Database Schema

```sql
CREATE TABLE spendings (
    id INTEGER PRIMARY KEY,
    amount REAL NOT NULL,
    category VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

## 🧪 Development

Run backend tests:
```cmd
cd backend
pytest -q
```

The SQLite database (`budget.db`) is created automatically in the backend directory.

## 📱 Mobile Support

The application is fully responsive and mobile-optimized:
- Flexible grid layout that adapts to screen size
- Touch-friendly buttons and form controls
- Optimized calendar component for mobile devices
- Scrollable content areas for better mobile navigation

## ☁️ Deploying to Render (Updated)

1. Create a new Web Service on Render pointing at this repo.
2. Service root: set Root Directory to `backend`.
3. Build Command: `bash build_simple.sh`
4. Start Command: `python start_fullstack.py` (serves API + static React build if present).
5. Environment Variables:
    - `DATABASE_URL` = your Render Postgres URL (ensure it begins with `postgresql://`; replace any `postgres://`).
    - `JWT_SECRET_KEY` = long random string.
    - `ALLOWED_ORIGINS` = `*` or a comma-separated list of allowed domains.
6. First deploy should come up using backend only (static folder already committed). After verifying, you can switch Build Command to `bash build_fullstack.sh` to rebuild the frontend on each deploy.

### Why builds were failing
Earlier failures came from forcing installation of an explicit `pydantic-core` version whose wheel wasn't available for the Python version on Render, triggering a source (Rust) build which is blocked by the read-only filesystem. Solution:
* Removed explicit `pydantic-core` pin; rely on `pydantic==2.8.2` which pulls a matching pre-built wheel.
* Added `runtime.txt` (Python 3.11) to align with available wheels.
* `build_simple.sh` tries a wheels-only install first and falls back if needed.

### Troubleshooting
| Symptom | Fix |
|--------|-----|
| pydantic-core source compile attempt | Confirm no separate `pydantic-core` pin; Python 3.11; wheels-only step passes |
| DB connection errors | Trim whitespace in `DATABASE_URL`; ensure correct hostname & credentials |
| Static files 404 | Ensure `backend/static` contains build output or use `build_fullstack.sh` to generate it |
| CORS issues | Set `ALLOWED_ORIGINS=*` temporarily, tighten later |

### Switching to full rebuild
After first green deploy: change Build Command to `bash build_render_fullstack.sh` to build the React app during deployment instead of relying on committed static assets. The `build_render_fullstack.sh` script uses Render's pre-installed Node.js and has no sudo requirements.

### Python Version Pin
Because the Render service root is set to `backend`, a `runtime.txt` is also placed inside `backend/` to force Python 3.11 (the repo root `runtime.txt` is ignored when the service root is a subdirectory). If you still see Python 3.13 in build logs, clear build cache and redeploy, or set an env var `PYTHON_VERSION=3.11.9` / `RENDER_PYTHON_VERSION=3.11.9` (Render may honor either) then redeploy.

**Update**: If Render still defaults to Python 3.13, the requirements have been updated with SQLAlchemy 2.0.35+ which supports Python 3.13, so the build should now succeed regardless of Python version.

### Admin User Setup
The default admin credentials are:
- Email: `admin@budgettracker.com`
- Password: `admin123`

If you can't log in, run this command in the Render shell to reset the admin:
```bash
cd /opt/render/project/src/backend && python force_admin.py
```
