// components/auth/RegisterForm/RegisterForm.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Button from '../../common/Button/Button';
import Input from '../../common/Input/Input';
import Alert from '../../common/Alert/Alert';
import { validateRegisterForm, formatPhone } from '../../../utils/validation';
import { useAuth } from '../../../contexts/AuthContext';
import './RegisterForm.css';

const RegisterForm = ({ onSuccess }) => {
  const { register, isLoading, error, clearError } = useAuth();
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    acceptTerms: false
  });
  
  const [fieldErrors, setFieldErrors] = useState({});

  // Manipula mudanças nos campos
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    let fieldValue = type === 'checkbox' ? checked : value;
    
    // Formatação especial para telefone
    if (name === 'phone') {
      fieldValue = formatPhone(value);
    }
    
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
    const validation = validateRegisterForm(formData);
    
    if (!validation.isValid) {
      setFieldErrors(validation.errors);
      return;
    }
    
    try {
      await register(formData);
      
      // Callback de sucesso
      if (onSuccess) {
        onSuccess();
      }
    } catch (error) {
      // Erro já é tratado no contexto
      console.error('Erro no cadastro:', error);
    }
  };

  // Ícones para os campos
  const UserIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
      <circle cx="12" cy="7" r="4"/>
    </svg>
  );

  const EmailIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
      <polyline points="22,6 12,13 2,6"/>
    </svg>
  );

  const PhoneIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
    </svg>
  );

  const LockIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
      <circle cx="12" cy="16" r="1"/>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    </svg>
  );

  const passwordStrength = () => {
    const password = formData.password;
    if (!password) return { strength: 0, text: '' };
    
    let score = 0;
    let feedback = [];
    
    if (password.length >= 8) score++;
    else feedback.push('pelo menos 8 caracteres');
    
    if (/[a-z]/.test(password)) score++;
    else feedback.push('uma letra minúscula');
    
    if (/[A-Z]/.test(password)) score++;
    else feedback.push('uma letra maiúscula');
    
    if (/\d/.test(password)) score++;
    else feedback.push('um número');
    
    if (/[!@#$%^&*]/.test(password)) score++;
    
    const strengthLevels = [
      { strength: 0, text: 'Muito fraca', color: 'var(--error-color)' },
      { strength: 25, text: 'Fraca', color: 'var(--error-color)' },
      { strength: 50, text: 'Média', color: 'var(--warning-color)' },
      { strength: 75, text: 'Boa', color: 'var(--success-color)' },
      { strength: 100, text: 'Forte', color: 'var(--success-color)' }
    ];
    
    return {
      ...strengthLevels[score],
      feedback: feedback.length > 0 ? `Adicione: ${feedback.join(', ')}` : 'Senha segura!'
    };
  };

  const strength = passwordStrength();

  return (
    <form className="register-form" onSubmit={handleSubmit} noValidate>
      <div className="register-form__header">
        <h1 className="register-form__title">Criar Conta no GEDIE</h1>
        <p className="register-form__subtitle">
          Comece a organizar suas finanças hoje mesmo
        </p>
      </div>

      {/* Erro geral */}
      {error && (
        <Alert type="error" closable onClose={clearError}>
          {error}
        </Alert>
      )}

      <div className="register-form__fields">
        {/* Campo Nome */}
        <Input
          name="name"
          type="text"
          label="Nome completo"
          placeholder="Digite seu nome completo"
          value={formData.name}
          onChange={handleChange}
          error={fieldErrors.name}
          icon={<UserIcon />}
          iconPosition="left"
          autoComplete="name"
          required
          fullWidth
        />

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

        {/* Campo Telefone */}
        <Input
          name="phone"
          type="tel"
          label="Telefone"
          placeholder="(11) 99999-9999"
          value={formData.phone}
          onChange={handleChange}
          error={fieldErrors.phone}
          icon={<PhoneIcon />}
          iconPosition="left"
          autoComplete="tel"
          helperText="Opcional - formato brasileiro"
          fullWidth
        />

        {/* Campo Senha */}
        <div className="register-form__password-field">
          <Input
            name="password"
            type="password"
            label="Senha"
            placeholder="Crie uma senha segura"
            value={formData.password}
            onChange={handleChange}
            error={fieldErrors.password}
            icon={<LockIcon />}
            iconPosition="left"
            autoComplete="new-password"
            required
            fullWidth
          />
          
          {/* Indicador de força da senha */}
          {formData.password && (
            <div className="register-form__password-strength">
              <div className="register-form__strength-bar">
                <div 
                  className="register-form__strength-fill"
                  style={{ 
                    width: `${strength.strength}%`,
                    backgroundColor: strength.color
                  }}
                />
              </div>
              <div className="register-form__strength-text">
                <span style={{ color: strength.color }}>
                  {strength.text}
                </span>
                {strength.feedback && (
                  <span className="register-form__strength-feedback">
                    {strength.feedback}
                  </span>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Campo Confirmar Senha */}
        <Input
          name="confirmPassword"
          type="password"
          label="Confirmar senha"
          placeholder="Digite a senha novamente"
          value={formData.confirmPassword}
          onChange={handleChange}
          error={fieldErrors.confirmPassword}
          icon={<LockIcon />}
          iconPosition="left"
          autoComplete="new-password"
          required
          fullWidth
        />
      </div>

      {/* Checkbox de termos */}
      <div className="register-form__terms">
        <label className="register-form__checkbox">
          <input
            type="checkbox"
            name="acceptTerms"
            checked={formData.acceptTerms}
            onChange={handleChange}
          />
          <span className="register-form__checkbox-mark"></span>
          <span className="register-form__checkbox-label">
            Eu aceito os{' '}
            <Link to="/terms" target="_blank" className="register-form__terms-link">
              Termos de Uso
            </Link>
            {' '}e a{' '}
            <Link to="/privacy" target="_blank" className="register-form__terms-link">
              Política de Privacidade
            </Link>
          </span>
        </label>
        {fieldErrors.acceptTerms && (
          <span className="register-form__error">
            {fieldErrors.acceptTerms}
          </span>
        )}
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
        {isLoading ? 'Criando conta...' : 'Criar conta'}
      </Button>

      {/* Link para login */}
      <div className="register-form__footer">
        <p className="register-form__footer-text">
          Já tem uma conta?{' '}
          <Link to="/login" className="register-form__footer-link">
            Entre aqui
          </Link>
        </p>
      </div>

      {/* Informação sobre Telegram */}
      <div className="register-form__telegram-info">
        <Alert type="info" icon={true}>
          <strong>💡 Dica:</strong> Após criar sua conta, você pode sincronizar com nosso bot do Telegram (@gedie_bot) para registrar gastos rapidamente!
        </Alert>
      </div>
    </form>
  );
};

export default RegisterForm;

