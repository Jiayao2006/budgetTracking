import React, { useState, useEffect } from 'react';
import { Container } from 'react-bootstrap';
import { Header } from '../components/Header';
import { Dashboard } from '../components/Dashboard';
import { SpendingForm } from '../components/SpendingForm';
import { SpendingCalendar } from '../components/SpendingCalendar';
import { api } from '../api';
import { DashboardStats, Spending, SpendingCreate } from '../types';
import { getTodayString } from '../utils/dateUtils';
import '../styles/custom.css';

export const App: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [spendings, setSpendings] = useState<Spending[]>([]);
  const [selectedDate, setSelectedDate] = useState(getTodayString());
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const [dashboardStats, allSpendings] = await Promise.all([
        api.getDashboardStats(),
        api.getSpendings()
      ]);
      setStats(dashboardStats);
      setSpendings(allSpendings);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAddSpending = async (spending: SpendingCreate) => {
    try {
      const newSpending = await api.createSpending(spending);
      setSpendings(prev => [newSpending, ...prev]);
      // Refresh dashboard stats
      const newStats = await api.getDashboardStats();
      setStats(newStats);
    } catch (error) {
      console.error('Failed to add spending:', error);
    }
  };

  const handleUpdateSpending = async (id: number, spending: SpendingCreate) => {
    try {
      const updatedSpending = await api.updateSpending(id, spending);
      setSpendings(prev => prev.map(s => s.id === id ? updatedSpending : s));
      // Refresh dashboard stats
      const newStats = await api.getDashboardStats();
      setStats(newStats);
    } catch (error) {
      console.error('Failed to update spending:', error);
    }
  };

  const handleDeleteSpending = async (id: number) => {
    try {
      await api.deleteSpending(id);
      setSpendings(prev => prev.filter(s => s.id !== id));
      // Refresh dashboard stats
      const newStats = await api.getDashboardStats();
      setStats(newStats);
    } catch (error) {
      console.error('Failed to delete spending:', error);
    }
  };

  if (loading) {
    return (
      <>
        <Header />
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
      <Header />
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
    </>
  );
};
