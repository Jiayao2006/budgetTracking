// API Configuration
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_BASE = isDevelopment 
  ? 'http://localhost:8000'  // For development
  : '';  // For production - relative path

export { API_BASE };
