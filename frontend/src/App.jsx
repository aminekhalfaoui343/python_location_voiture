import React, { useState, useEffect } from 'react';
import './styles/global.css';
import Header from './components/Header';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import CarsPage from './pages/CarsPage';
import CustomersPage from './pages/CustomersPage';
import RentalsPage from './pages/RentalsPage';
import MLPage from './pages/MLPage';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [loading, setLoading] = useState(false);

  const renderPage = () => {
    switch(currentPage) {
      case 'cars':
        return <CarsPage />;
      case 'customers':
        return <CustomersPage />;
      case 'rentals':
        return <RentalsPage />;
      case 'ml':
        return <MLPage />;
      case 'dashboard':
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="app">
      <Header />
      <div className="container">
        <Navigation currentPage={currentPage} onPageChange={setCurrentPage} />
        <main className="main-content">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}

export default App;
