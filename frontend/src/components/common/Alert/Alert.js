// components/common/Alert/Alert.js
import React from 'react';
import './Alert.css';

const Alert = ({
  children,
  type = 'info',
  title,
  closable = false,
  onClose,
  icon = true,
  className = '',
  ...props
}) => {
  const alertClasses = [
    'alert',
    `alert--${type}`,
    className
  ].filter(Boolean).join(' ');

  const getIcon = () => {
    if (!icon) return null;

    const iconProps = {
      width: "20",
      height: "20",
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "currentColor",
      strokeWidth: "2"
    };

    switch (type) {
      case 'success':
        return (
          <svg {...iconProps}>
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22,4 12,14.01 9,11.01"/>
          </svg>
        );
      case 'error':
        return (
          <svg {...iconProps}>
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
        );
      case 'warning':
        return (
          <svg {...iconProps}>
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        );
      default:
        return (
          <svg {...iconProps}>
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="16" x2="12" y2="12"/>
            <line x1="12" y1="8" x2="12.01" y2="8"/>
          </svg>
        );
    }
  };

  return (
    <div className={alertClasses} role="alert" {...props}>
      <div className="alert__content">
        {icon && (
          <div className="alert__icon">
            {getIcon()}
          </div>
        )}
        
        <div className="alert__body">
          {title && <div className="alert__title">{title}</div>}
          <div className="alert__message">{children}</div>
        </div>
      </div>
      
      {closable && (
        <button
          type="button"
          className="alert__close"
          onClick={onClose}
          aria-label="Fechar alerta"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      )}
    </div>
  );
};

export default Alert;
