// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/common/ProtectedRoute';
import PublicRoute from './components/common/PublicRoute';
import LoginPage from './pages/Login/Login';
import RegisterPage from './pages/Register/Register';
import DashboardPage from './pages/Dashboard/Dashboard';
import LoadingPage from './components/common/LoadingPage';
import './App.css';

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <Router>
          <Routes>
            {/* Rotas públicas (apenas para não autenticados) */}
            <Route
              path="/login"
              element={
                <PublicRoute>
                  <LoginPage />
                </PublicRoute>
              }
            />
            <Route
              path="/register"
              element={
                <PublicRoute>
                  <RegisterPage />
                </PublicRoute>
              }
            />

            {/* Rotas protegidas (apenas para autenticados) */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />

            {/* Rota raiz - redireciona baseado na autenticação */}
            <Route
              path="/"
              element={<Navigate to="/dashboard" replace />}
            />

            {/* Rota 404 */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>

          {/* Toast notifications */}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'var(--background-primary)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-lg)',
                fontSize: 'var(--font-sm)',
                maxWidth: '400px',
              },
              success: {
                iconTheme: {
                  primary: 'var(--success-color)',
                  secondary: 'white',
                },
              },
              error: {
                iconTheme: {
                  primary: 'var(--error-color)',
                  secondary: 'white',
                },
              },
              loading: {
                iconTheme: {
                  primary: 'var(--primary-color)',
                  secondary: 'white',
                },
              },
            }}
          />
        </Router>
      </AuthProvider>
    </div>
  );
}

export default App;