// pages/Register/Register.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import RegisterForm from '../../components/auth/RegisterForm/RegisterForm';
import { useAuth } from '../../contexts/AuthContext';
import './Register.css';

const RegisterPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  // Redireciona se já estiver autenticado
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  // Callback para cadastro bem-sucedido
  const handleRegisterSuccess = () => {
    toast.success('Conta criada com sucesso! Bem-vindo ao GEDIE!');
    navigate('/dashboard', { replace: true });
  };

  return (
    <div className="register-page">
      <div className="register-page__background">
        <div className="register-page__background-pattern"></div>
      </div>
      
      <div className="register-page__container">
        {/* Seção de informações */}
        <div className="register-page__info">
          <div className="register-page__brand">
            <div className="register-page__logo">
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
            <h2 className="register-page__brand-name">GEDIE</h2>
            <p className="register-page__brand-tagline">
              Sua jornada financeira começa aqui
            </p>
          </div>

          <div className="register-page__benefits">
            <h3 className="register-page__benefits-title">
              Tudo que você precisa para organizar suas finanças
            </h3>
            
            <div className="register-page__benefits-list">
              <div className="register-page__benefit">
                <span className="register-page__benefit-icon">🚀</span>
                <div>
                  <strong>Configuração rápida</strong>
                  <p>Comece a usar em menos de 2 minutos</p>
                </div>
              </div>
              
              <div className="register-page__benefit">
                <span className="register-page__benefit-icon">🔒</span>
                <div>
                  <strong>100% Seguro</strong>
                  <p>Seus dados protegidos com criptografia avançada</p>
                </div>
              </div>
              
              <div className="register-page__benefit">
                <span className="register-page__benefit-icon">📈</span>
                <div>
                  <strong>Insights inteligentes</strong>
                  <p>Descubra padrões nos seus gastos</p>
                </div>
              </div>
              
              <div className="register-page__benefit">
                <span className="register-page__benefit-icon">🎯</span>
                <div>
                  <strong>Metas personalizadas</strong>
                  <p>Defina objetivos e acompanhe seu progresso</p>
                </div>
              </div>
            </div>
          </div>

          <div className="register-page__testimonial">
            <blockquote>
              "O GEDIE transformou a maneira como controlo meus gastos. 
              A integração com Telegram é genial!"
            </blockquote>
            <cite>— Maria S., usuária desde 2024</cite>
          </div>
        </div>

        {/* Formulário */}
        <div className="register-page__form-container">
          <RegisterForm onSuccess={handleRegisterSuccess} />
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
