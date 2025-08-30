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
import { API_BASE } from '../config/api';
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
      console.log('Loading dashboard data...');
      
      const [statsResponse, spendingsResponse] = await Promise.all([
        authenticatedFetch(`${API_BASE}/api/spendings/dashboard`),
        authenticatedFetch(`${API_BASE}/api/spendings`)
      ]);
      
      console.log('Stats response status:', statsResponse.status);
      console.log('Spendings response status:', spendingsResponse.status);
      
      if (!statsResponse.ok) {
        console.error('Dashboard stats failed:', await statsResponse.text());
      }
      
      if (!spendingsResponse.ok) {
        console.error('Spendings fetch failed:', await spendingsResponse.text());
      }
      
      const dashboardStats = await statsResponse.json();
      const allSpendings = await spendingsResponse.json();
      
      console.log('Dashboard stats:', dashboardStats);
      console.log('All spendings count:', allSpendings.length);
      
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
      console.log('Attempting to create spending:', spending);
      console.log('API endpoint:', `${API_BASE}/api/spendings`);
      
      const response = await authenticatedFetch(`${API_BASE}/api/spendings`, {
        method: 'POST',
        body: JSON.stringify(spending),
      });
      
      console.log('Create spending response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Create spending failed:', errorText);
        throw new Error(`Failed to create spending: ${response.status} ${errorText}`);
      }
      
      const newSpending = await response.json();
      console.log('Created spending:', newSpending);
      
      setSpendings(prev => [newSpending, ...prev]);
      
      // Refresh dashboard stats
      const statsResponse = await authenticatedFetch(`${API_BASE}/api/spendings/dashboard`);
      if (statsResponse.ok) {
        const newStats = await statsResponse.json();
        setStats(newStats);
        console.log('Dashboard stats refreshed');
      }
    } catch (error) {
      console.error('Failed to add spending:', error);
      alert(`Failed to add spending: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const handleUpdateSpending = async (id: number, spending: SpendingCreate) => {
    try {
      const response = await authenticatedFetch(`${API_BASE}/api/spendings/${id}`, {
        method: 'PUT',
        body: JSON.stringify(spending),
      });
      const updatedSpending = await response.json();
      setSpendings(prev => prev.map(s => s.id === id ? updatedSpending : s));
      // Refresh dashboard stats
      const statsResponse = await authenticatedFetch(`${API_BASE}/api/spendings/dashboard`);
      const newStats = await statsResponse.json();
      setStats(newStats);
    } catch (error) {
      console.error('Failed to update spending:', error);
    }
  };

  const handleDeleteSpending = async (id: number) => {
    try {
      await authenticatedFetch(`${API_BASE}/api/spendings/${id}`, {
        method: 'DELETE',
      });
      setSpendings(prev => prev.filter(s => s.id !== id));
      // Refresh dashboard stats
      const statsResponse = await authenticatedFetch(`${API_BASE}/api/spendings/dashboard`);
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
