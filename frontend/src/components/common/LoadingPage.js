// components/common/LoadingPage.js
import React from 'react';
import Loading from './Loading/Loading';

const LoadingPage = ({ message = "Carregando..." }) => {
  return (
    <div className="app-loading">
      <div style={{ textAlign: 'center' }}>
        <div style={{ marginBottom: 'var(--spacing-lg)' }}>
          <svg
            width="80"
            height="80"
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="50" cy="50" r="45" fill="url(#gradient)" />
            <path
              d="M30 40h40v6H30v-6zm0 12h40v6H30v-6zm0 12h28v6H30v-6z"
              fill="white"
            />
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#2563eb" />
                <stop offset="100%" stopColor="#10b981" />
              </linearGradient>
            </defs>
          </svg>
        </div>
        <Loading size="lg" text={message} />
      </div>
    </div>
  );
};

export default LoadingPage;