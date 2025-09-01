import React, { useState, useEffect } from 'react';
import { Container } from 'react-bootstrap';
import { AuthProvider, useAuth } from '../context/AuthContext';
import { AuthPage } from '../components/AuthPage';
import { Navigation } from '../components/Navigation';
import { AdminDashboard } from '../components/AdminDashboard';
import { Dashboard } from '../components/Dashboard';
import { SpendingForm } from '../components/SpendingForm';
import { SpendingCalendar } from '../components/SpendingCalendar';
import { CurrencySettings } from '../components/CurrencySettings';
import { Labels } from '../components/Labels';
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
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState<string>('calendar');
  const [dataLoaded, setDataLoaded] = useState(false);
  const authenticatedFetch = useAuthenticatedFetch();

  // All hooks must be called before any conditional returns

  const loadData = async () => {
    if (!user) return;
    
    try {
      setLoading(true);
      console.log('🔄 Loading dashboard data for user:', user.email);
      console.log('🔐 Auth token present:', !!localStorage.getItem('token'));
      
      const [statsResponse, spendingsResponse] = await Promise.all([
        authenticatedFetch(`${API_BASE}/api/spendings/dashboard`),
        authenticatedFetch(`${API_BASE}/api/spendings`)
      ]);
      
      console.log('📊 Stats response status:', statsResponse.status);
      console.log('💰 Spendings response status:', spendingsResponse.status);
      
      if (!statsResponse.ok) {
        console.error('❌ Dashboard stats failed:', await statsResponse.text());
      }
      
      if (!spendingsResponse.ok) {
        const errorText = await spendingsResponse.text();
        console.error('❌ Spendings fetch failed:', errorText);
        console.error('❌ Spendings response status:', spendingsResponse.status);
        return;
      }
      
      const dashboardStats = await statsResponse.json();
      const allSpendings = await spendingsResponse.json();
      
      console.log('📊 Dashboard stats:', dashboardStats);
      console.log('💰 All spendings count:', allSpendings.length);
      console.log('💰 All spendings data:', allSpendings);
      
      setStats(dashboardStats);
      setSpendings(allSpendings);
      setDataLoaded(true);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user && currentPage === 'calendar' && !dataLoaded) {
      console.log('User authenticated, loading data for user:', user.email);
      console.log('Current loading state:', loading);
      console.log('Current stats:', stats);
      loadData();
    }
  }, [user, currentPage, dataLoaded]);
  
  // Ensure users are directed to home page after login/registration
  useEffect(() => {
    if (user) {
      console.log(`User ${user.email} logged in, redirecting to home page (calendar)`);
      setCurrentPage('calendar');
      // Reset data loaded state to ensure fresh data load for new user session
      setDataLoaded(false);
    } else {
      // User logged out, reset all state to initial values
      console.log('User logged out, resetting application state');
      setCurrentPage('calendar');
      setStats(null);
      setSpendings([]);
      setDataLoaded(false);
      setLoading(false);
    }
  }, [user]);
  
  // Debug logging for state changes
  useEffect(() => {
    console.log('App state changed:', {
      user: user?.email || 'none',
      currentPage,
      loading,
      authLoading,
      hasStats: !!stats,
      dataLoaded
    });
  }, [user, currentPage, loading, authLoading, stats, dataLoaded]);

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

  // Show loading while authenticating or when user just logged in but data isn't loaded yet
  if (authLoading) {
    return (
      <>
        <Navigation currentPage={currentPage} onPageChange={setCurrentPage} />
        <Container fluid className="px-4 px-lg-5 pb-5" style={{ background: 'linear-gradient(135deg, #f8f9fc 0%, #e9ecf4 100%)', minHeight: '100vh' }}>
          <div className="text-center mt-5">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-3">Authenticating...</p>
          </div>
        </Container>
      </>
    );
  }

  // Show loading while data is being fetched for calendar page
  if (user && currentPage === 'calendar' && loading) {
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

  console.log('AppContent render - About to return JSX:', {
    user: user?.email || 'none',
    currentPage,
    loading,
    dataLoaded
  });

  return (
    <>
      <Navigation currentPage={currentPage} onPageChange={setCurrentPage} />
      
      {currentPage === 'calendar' && (
        <div style={{ background: 'linear-gradient(135deg, #f8f9fc 0%, #e9ecf4 100%)', minHeight: '100vh', padding: '1rem 2rem' }}>
          {loading ? (
            <div className="text-center py-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              <p className="mt-3">Loading dashboard data...</p>
            </div>
          ) : (
            <div className="container-fluid">
              <div style={{ marginBottom: '2rem' }} className="fade-in">
                <Dashboard stats={stats} />
              </div>
              
              <div style={{ marginBottom: '2rem' }} className="fade-in">
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
            </div>
          )}
        </div>
      )}

      {currentPage === 'admin' && user?.is_admin && (
        <AdminDashboard />
      )}

      {currentPage === 'labels' && (
        <Labels />
      )}

      {currentPage === 'settings' && (
        <Container className="py-5">
          <div className="row justify-content-center">
            <div className="col-md-8 col-lg-6">
              <CurrencySettings />
            </div>
          </div>
        </Container>
      )}
    </>
  );
};
