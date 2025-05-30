// components/common/Loading/Loading.js
import React from 'react';
import './Loading.css';

const Loading = ({ 
  size = 'md', 
  color = 'primary', 
  text = null,
  overlay = false,
  className = '' 
}) => {
  const sizeClass = `loading--${size}`;
  const colorClass = `loading--${color}`;
  const overlayClass = overlay ? 'loading--overlay' : '';
  
  const loadingClassName = [
    'loading',
    sizeClass,
    colorClass,
    overlayClass,
    className
  ].filter(Boolean).join(' ');

  const LoadingSpinner = () => (
    <div className="loading__spinner">
      <svg
        className="loading__spinner-icon"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeDasharray="31.416"
          strokeDashoffset="31.416"
        />
      </svg>
    </div>
  );

  if (overlay) {
    return (
      <div className={loadingClassName}>
        <div className="loading__overlay-content">
          <LoadingSpinner />
          {text && <p className="loading__text">{text}</p>}
        </div>
      </div>
    );
  }

  return (
    <div className={loadingClassName}>
      <LoadingSpinner />
      {text && <p className="loading__text">{text}</p>}
    </div>
  );
};

export default Loading;






