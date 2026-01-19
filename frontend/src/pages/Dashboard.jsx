import React, { useState, useEffect } from 'react';
import { statsAPI } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    try {
      setLoading(true);
      const response = await statsAPI.getStatistics();
      setStats(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load statistics: ' + (err.response?.data?.detail || err.message));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      {error && <ErrorMessage message={error} onClose={() => setError(null)} />}
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🚗</div>
          <h3>Total Cars</h3>
          <p className="stat-value">{stats?.total_cars || 0}</p>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <h3>Available Cars</h3>
          <p className="stat-value">{stats?.available_cars || 0}</p>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">🔴</div>
          <h3>Rented Cars</h3>
          <p className="stat-value">{stats?.rented_cars || 0}</p>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <h3>Average Mileage</h3>
          <p className="stat-value">{stats?.average_mileage ? stats.average_mileage.toFixed(2) : 0} km</p>
        </div>
      </div>

      <div className="dashboard-info">
        <h3>System Overview</h3>
        <ul>
          <li>Total number of cars: <strong>{stats?.total_cars || 0}</strong></li>
          <li>Available cars ready for rental: <strong>{stats?.available_cars || 0}</strong></li>
          <li>Currently rented cars: <strong>{stats?.rented_cars || 0}</strong></li>
          <li>Average mileage: <strong>{stats?.average_mileage ? stats.average_mileage.toFixed(2) : 0} km</strong></li>
        </ul>
      </div>

      <button className="btn btn-primary" onClick={fetchStatistics}>
        Refresh Statistics
      </button>
    </div>
  );
}

export default Dashboard;
