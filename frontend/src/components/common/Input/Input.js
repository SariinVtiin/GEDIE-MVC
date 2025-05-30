// components/common/Input/Input.js
import React, { useState, forwardRef } from 'react';
import './Input.css';

const Input = forwardRef(({
  type = 'text',
  label,
  placeholder,
  value,
  onChange,
  onBlur,
  onFocus,
  error,
  disabled = false,
  required = false,
  fullWidth = false,
  size = 'md',
  icon = null,
  iconPosition = 'left',
  clearable = false,
  helperText,
  maxLength,
  autoComplete,
  name,
  id,
  className = '',
  ...props
}, ref) => {
  const [showPassword, setShowPassword] = useState(false);
  const [focused, setFocused] = useState(false);

  const inputId = id || name || `input-${Math.random().toString(36).substr(2, 9)}`;
  const isPassword = type === 'password';
  const hasError = !!error;
  const hasValue = value && value.toString().length > 0;

  const containerClasses = [
    'input-container',
    `input-container--${size}`,
    fullWidth ? 'input-container--full-width' : '',
    hasError ? 'input-container--error' : '',
    disabled ? 'input-container--disabled' : '',
    focused ? 'input-container--focused' : '',
    hasValue ? 'input-container--has-value' : '',
    className
  ].filter(Boolean).join(' ');

  const inputClasses = [
    'input',
    icon ? `input--with-icon-${iconPosition}` : '',
    isPassword || clearable ? 'input--with-action' : ''
  ].filter(Boolean).join(' ');

  const handleFocus = (e) => {
    setFocused(true);
    onFocus?.(e);
  };

  const handleBlur = (e) => {
    setFocused(false);
    onBlur?.(e);
  };

  const handleClear = () => {
    if (onChange) {
      const syntheticEvent = {
        target: { value: '', name, type }
      };
      onChange(syntheticEvent);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const getInputType = () => {
    if (isPassword) {
      return showPassword ? 'text' : 'password';
    }
    return type;
  };

  return (
    <div className={containerClasses}>
      {label && (
        <label htmlFor={inputId} className="input-label">
          {label}
          {required && <span className="input-label__required">*</span>}
        </label>
      )}
      
      <div className="input-wrapper">
        {icon && iconPosition === 'left' && (
          <span className="input-icon input-icon--left">
            {icon}
          </span>
        )}
        
        <input
          ref={ref}
          id={inputId}
          name={name}
          type={getInputType()}
          value={value || ''}
          onChange={onChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
          placeholder={placeholder}
          disabled={disabled}
          required={required}
          maxLength={maxLength}
          autoComplete={autoComplete}
          className={inputClasses}
          aria-invalid={hasError}
          aria-describedby={
            hasError ? `${inputId}-error` : 
            helperText ? `${inputId}-helper` : undefined
          }
          {...props}
        />
        
        {icon && iconPosition === 'right' && (
          <span className="input-icon input-icon--right">
            {icon}
          </span>
        )}
        
        {/* Botão para mostrar/ocultar senha */}
        {isPassword && (
          <button
            type="button"
            className="input-action input-action--password"
            onClick={togglePasswordVisibility}
            aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
            tabIndex={-1}
          >
            {showPassword ? (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
            )}
          </button>
        )}
        
        {/* Botão de limpar */}
        {clearable && hasValue && !disabled && (
          <button
            type="button"
            className="input-action input-action--clear"
            onClick={handleClear}
            aria-label="Limpar campo"
            tabIndex={-1}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        )}
      </div>
      
      {/* Mensagem de erro */}
      {hasError && (
        <span id={`${inputId}-error`} className="input-error">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
          {error}
        </span>
      )}
      
      {/* Texto de ajuda */}
      {helperText && !hasError && (
        <span id={`${inputId}-helper`} className="input-helper">
          {helperText}
        </span>
      )}
    </div>
  );
});

Input.displayName = 'Input';

export default Input;

