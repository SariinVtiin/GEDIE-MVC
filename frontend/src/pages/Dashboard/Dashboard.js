// pages/Dashboard/Dashboard.js
import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import Button from '../../components/common/Button/Button';
import './Dashboard.css';

const DashboardPage = () => {
  const { user, logout, telegramSync } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    }
  };

  return (
    <div className="dashboard-page">
      <div className="dashboard-page__header">
        <div className="dashboard-page__user-info">
          <h1 className="dashboard-page__welcome">
            Olá, {user?.name || 'Usuário'}! 👋
          </h1>
          <p className="dashboard-page__subtitle">
            Bem-vindo ao seu painel de controle financeiro
          </p>
        </div>
        
        <div className="dashboard-page__actions">
          <Button variant="outline" onClick={handleLogout}>
            Sair
          </Button>
        </div>
      </div>

      <div className="dashboard-page__content">
        <div className="dashboard-page__stats">
          <div className="dashboard-page__stat-card">
            <h3>Status da Conta</h3>
            <p>Email: {user?.email}</p>
            {user?.phone && <p>Telefone: {user.phone}</p>}
          </div>

          <div className="dashboard-page__stat-card">
            <h3>Telegram</h3>
            {telegramSync.isLinked ? (
              <p>✅ Conectado (ID: {telegramSync.telegramId})</p>
            ) : (
              <p>❌ Não conectado</p>
            )}
          </div>
        </div>

        <div className="dashboard-page__placeholder">
          <h2>🚧 Dashboard em construção</h2>
          <p>
            Esta é uma versão inicial focada na autenticação. 
            O dashboard completo com gráficos e relatórios será implementado em breve!
          </p>
          
          <div className="dashboard-page__next-features">
            <h3>Próximas funcionalidades:</h3>
            <ul>
              <li>📊 Gráficos de gastos por categoria</li>
              <li>📈 Relatórios mensais e anuais</li>
              <li>🎯 Metas e orçamentos</li>
              <li>🤖 Sincronização com bot do Telegram</li>
              <li>📷 Upload de comprovantes</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
