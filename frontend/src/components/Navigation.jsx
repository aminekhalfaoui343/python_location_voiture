import React from 'react';

function Navigation({ currentPage, onPageChange }) {
  const menuItems = [
    { id: 'dashboard', label: '📊 Dashboard', icon: '📊' },
    { id: 'cars', label: '🚗 Cars', icon: '🚗' },
    { id: 'customers', label: '👤 Customers', icon: '👤' },
    { id: 'rentals', label: '🔄 Rentals', icon: '🔄' },
    { id: 'ml', label: '🤖 ML Predictor', icon: '🤖' },
  ];

  return (
    <nav className="navigation">
      <ul className="nav-menu">
        {menuItems.map(item => (
          <li key={item.id}>
            <button
              className={`nav-link ${currentPage === item.id ? 'active' : ''}`}
              onClick={() => onPageChange(item.id)}
            >
              {item.label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default Navigation;
