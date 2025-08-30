import React, { useState, useEffect } from 'react';
import { Container } from 'react-bootstrap';
import { AuthProvider, useAuth } from '../context/AuthContext';
import { AuthPage } from '../components/AuthPage';
import { Navigation } from '../components/Navigation';
import { AdminDashboard } from '../components/AdminDashboard';
import { Dashboard } from '../components/Dashboard';
import { SpendingForm } from '../components/SpendingForm';
import { SpendingCalendar } from '../components/SpendingCalendar';
import { useAuthenticatedFetch } from '../context/AuthContext';
import { DashboardStats, Spending, SpendingCreate } from '../types';
import { getTodayString } from '../utils/dateUtils';
import '../styles/custom.css';

// Main App Component wrapped in AuthProvider
export const App: React.FC = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

// Separate component that uses auth context
const AppContent: React.FC = () => {
  const { user, login, register, loading: authLoading, error: authError } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [spendings, setSpendings] = useState<Spending[]>([]);
  const [selectedDate, setSelectedDate] = useState(getTodayString());
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState<string>('calendar');
  const authenticatedFetch = useAuthenticatedFetch();

  // All hooks must be called before any conditional returns

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsResponse, spendingsResponse] = await Promise.all([
        authenticatedFetch('http://localhost:8000/api/spendings/dashboard'),
        authenticatedFetch('http://localhost:8000/api/spendings')
      ]);
      
      const dashboardStats = await statsResponse.json();
      const allSpendings = await spendingsResponse.json();
      
      setStats(dashboardStats);
      setSpendings(allSpendings);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (currentPage === 'calendar' && user) {
      loadData();
    }
  }, [currentPage, user]);

  // If user is not logged in, show auth page
  if (!user) {
    return (
      <AuthPage
        onLogin={login}
        onRegister={register}
        loading={authLoading}
        error={authError}
      />
    );
  }

  const handleAddSpending = async (spending: SpendingCreate) => {
    try {
      const response = await authenticatedFetch('http://localhost:8000/api/spendings/', {
        method: 'POST',
        body: JSON.stringify(spending),
      });
      const newSpending = await response.json();
      setSpendings(prev => [newSpending, ...prev]);
      // Refresh dashboard stats
      const statsResponse = await authenticatedFetch('http://localhost:8000/api/spendings/dashboard');
      const newStats = await statsResponse.json();
      setStats(newStats);
    } catch (error) {
      console.error('Failed to add spending:', error);
    }
  };

  const handleUpdateSpending = async (id: number, spending: SpendingCreate) => {
    try {
      const response = await authenticatedFetch(`http://localhost:8000/api/spendings/${id}`, {
        method: 'PUT',
        body: JSON.stringify(spending),
      });
      const updatedSpending = await response.json();
      setSpendings(prev => prev.map(s => s.id === id ? updatedSpending : s));
      // Refresh dashboard stats
      const statsResponse = await authenticatedFetch('http://localhost:8000/api/spendings/dashboard');
      const newStats = await statsResponse.json();
      setStats(newStats);
    } catch (error) {
      console.error('Failed to update spending:', error);
    }
  };

  const handleDeleteSpending = async (id: number) => {
    try {
      await authenticatedFetch(`http://localhost:8000/api/spendings/${id}`, {
        method: 'DELETE',
      });
      setSpendings(prev => prev.filter(s => s.id !== id));
      // Refresh dashboard stats
      const statsResponse = await authenticatedFetch('http://localhost:8000/api/spendings/dashboard');
      const newStats = await statsResponse.json();
      setStats(newStats);
    } catch (error) {
      console.error('Failed to delete spending:', error);
    }
  };

  if (loading && currentPage === 'calendar') {
    return (
      <>
        <Navigation currentPage={currentPage} onPageChange={setCurrentPage} />
        <Container fluid className="px-4 px-lg-5 pb-5" style={{ background: 'linear-gradient(135deg, #f8f9fc 0%, #e9ecf4 100%)', minHeight: '100vh' }}>
          <div className="text-center mt-5">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-3">Loading dashboard...</p>
          </div>
        </Container>
      </>
    );
  }

  return (
    <>
      <Navigation currentPage={currentPage} onPageChange={setCurrentPage} />
      
      {currentPage === 'calendar' && (
        <Container fluid className="px-4 px-lg-5 pb-5" style={{ background: 'linear-gradient(135deg, #f8f9fc 0%, #e9ecf4 100%)', minHeight: '100vh' }}>
          <div className="fade-in">
            <Dashboard stats={stats} />
          </div>
          
          <div className="mb-5 fade-in">
            <SpendingForm onSubmit={handleAddSpending} />
          </div>
          
          <div className="fade-in">
            <SpendingCalendar 
              spendings={spendings}
              selectedDate={selectedDate}
              onDateSelect={setSelectedDate}
              onUpdateSpending={handleUpdateSpending}
              onDeleteSpending={handleDeleteSpending}
            />
          </div>
        </Container>
      )}

      {currentPage === 'admin' && user?.is_admin && (
        <AdminDashboard />
      )}
    </>
  );
};
