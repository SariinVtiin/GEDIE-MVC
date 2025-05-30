// pages/Login/Login.js
import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import LoginForm from '../../components/auth/LoginForm/LoginForm';
import { useAuth } from '../../contexts/AuthContext';
import './Login.css';

const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated } = useAuth();

  // Redireciona se já estiver autenticado
  useEffect(() => {
    if (isAuthenticated) {
      const from = location.state?.from?.pathname || '/dashboard';
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, location]);

  // Callback para login bem-sucedido
  const handleLoginSuccess = () => {
    const from = location.state?.from?.pathname || '/dashboard';
    toast.success('Login realizado com sucesso!');
    navigate(from, { replace: true });
  };

  return (
    <div className="login-page">
      <div className="login-page__background">
        <div className="login-page__background-pattern"></div>
      </div>
      
      <div className="login-page__container">
        <div className="login-page__content">
          {/* Logo/Branding */}
          <div className="login-page__brand">
            <div className="login-page__logo">
              <svg
                width="60"
                height="60"
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
            <h2 className="login-page__brand-name">GEDIE</h2>
            <p className="login-page__brand-tagline">
              Gerenciador de Despesas Inteligente
            </p>
          </div>

          {/* Formulário */}
          <div className="login-page__form-container">
            <LoginForm onSuccess={handleLoginSuccess} />
          </div>
        </div>

        {/* Features/Benefits */}
        <div className="login-page__features">
          <h3 className="login-page__features-title">
            Por que escolher o GEDIE?
          </h3>
          <div className="login-page__features-list">
            <div className="login-page__feature">
              <div className="login-page__feature-icon">💰</div>
              <div className="login-page__feature-text">
                <strong>Controle Total</strong>
                <span>Gerencie todas suas despesas em um só lugar</span>
              </div>
            </div>
            <div className="login-page__feature">
              <div className="login-page__feature-icon">🤖</div>
              <div className="login-page__feature-text">
                <strong>IA Inteligente</strong>
                <span>Categorização automática com análise de comprovantes</span>
              </div>
            </div>
            <div className="login-page__feature">
              <div className="login-page__feature-icon">📱</div>
              <div className="login-page__feature-text">
                <strong>Bot Telegram</strong>
                <span>Registre gastos rapidamente pelo WhatsApp</span>
              </div>
            </div>
            <div className="login-page__feature">
              <div className="login-page__feature-icon">📊</div>
              <div className="login-page__feature-text">
                <strong>Relatórios Detalhados</strong>
                <span>Visualize seus dados com gráficos interativos</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;





