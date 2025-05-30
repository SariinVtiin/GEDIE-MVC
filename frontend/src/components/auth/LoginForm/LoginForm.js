// components/auth/LoginForm/LoginForm.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Button from '../../common/Button/Button';
import Input from '../../common/Input/Input';
import Alert from '../../common/Alert/Alert';
import { validateLoginForm } from '../../../utils/validation';
import { useAuth } from '../../../contexts/AuthContext';
import './LoginForm.css';

const LoginForm = ({ onSuccess }) => {
  const { login, isLoading, error, clearError } = useAuth();
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false
  });
  
  const [fieldErrors, setFieldErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);

  // Manipula mudanças nos campos
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const fieldValue = type === 'checkbox' ? checked : value;
    
    // Limpa erro do campo quando usuário começa a digitar
    if (fieldErrors[name]) {
      setFieldErrors(prev => ({ ...prev, [name]: null }));
    }
    
    // Limpa erro geral se existir
    if (error) {
      clearError();
    }
    
    setFormData(prev => ({
      ...prev,
      [name]: fieldValue
    }));
  };

  // Submete o formulário
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Valida formulário
    const validation = validateLoginForm(formData);
    
    if (!validation.isValid) {
      setFieldErrors(validation.errors);
      return;
    }
    
    try {
      await login(formData, formData.rememberMe);
      
      // Callback de sucesso
      if (onSuccess) {
        onSuccess();
      }
    } catch (error) {
      // Erro já é tratado no contexto
      console.error('Erro no login:', error);
    }
  };

  // Ícones para os campos
  const EmailIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
      <polyline points="22,6 12,13 2,6"/>
    </svg>
  );

  const LockIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
      <circle cx="12" cy="16" r="1"/>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    </svg>
  );

  return (
    <form className="login-form" onSubmit={handleSubmit} noValidate>
      <div className="login-form__header">
        <h1 className="login-form__title">Entrar no GEDIE</h1>
        <p className="login-form__subtitle">
          Gerencie suas despesas de forma inteligente
        </p>
      </div>

      {/* Erro geral */}
      {error && (
        <Alert type="error" closable onClose={clearError}>
          {error}
        </Alert>
      )}

      <div className="login-form__fields">
        {/* Campo Email */}
        <Input
          name="email"
          type="email"
          label="Email"
          placeholder="seu.email@exemplo.com"
          value={formData.email}
          onChange={handleChange}
          error={fieldErrors.email}
          icon={<EmailIcon />}
          iconPosition="left"
          autoComplete="email"
          required
          fullWidth
        />

        {/* Campo Senha */}
        <Input
          name="password"
          type="password"
          label="Senha"
          placeholder="Digite sua senha"
          value={formData.password}
          onChange={handleChange}
          error={fieldErrors.password}
          icon={<LockIcon />}
          iconPosition="left"
          autoComplete="current-password"
          required
          fullWidth
        />
      </div>

      {/* Opções adicionais */}
      <div className="login-form__options">
        <label className="login-form__checkbox">
          <input
            type="checkbox"
            name="rememberMe"
            checked={formData.rememberMe}
            onChange={handleChange}
          />
          <span className="login-form__checkbox-mark"></span>
          <span className="login-form__checkbox-label">Lembrar de mim</span>
        </label>

        <Link to="/forgot-password" className="login-form__forgot-link">
          Esqueceu a senha?
        </Link>
      </div>

      {/* Botão de submit */}
      <Button
        type="submit"
        variant="primary"
        size="lg"
        fullWidth
        loading={isLoading}
        disabled={isLoading}
      >
        {isLoading ? 'Entrando...' : 'Entrar'}
      </Button>

      {/* Link para cadastro */}
      <div className="login-form__footer">
        <p className="login-form__footer-text">
          Não tem uma conta?{' '}
          <Link to="/register" className="login-form__footer-link">
            Cadastre-se grátis
          </Link>
        </p>
      </div>

      {/* Integração com Telegram */}
      <div className="login-form__divider">
        <span>ou</span>
      </div>

      <div className="login-form__telegram">
        <Alert type="info" icon={true}>
          <strong>Já usa o bot do Telegram?</strong>
          <br />
          Faça login normalmente e depois sincronize sua conta nas configurações.
        </Alert>
      </div>
    </form>
  );
};

export default LoginForm;

