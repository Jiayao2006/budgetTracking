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