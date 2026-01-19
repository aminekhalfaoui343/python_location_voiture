import React from 'react';

function SuccessMessage({ message, onClose }) {
  React.useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className="success-banner">
      <div className="success-content">
        <span className="success-icon">✓</span>
        <span className="success-text">{message}</span>
        <button className="success-close" onClick={onClose}>✕</button>
      </div>
    </div>
  );
}

export default SuccessMessage;
