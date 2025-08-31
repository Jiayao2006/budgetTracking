// API Configuration
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_BASE = isDevelopment 
  ? 'http://localhost:8000'  // For development
  : 'https://budget-tracker-fullstack.onrender.com';  // For production - use full URL

export { API_BASE };
