/**
 * Contexto de autenticação para gerenciar estado global do usuário
 */

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { AUTH_STATUS } from '../utils/constants';
import authService from '../services/authService';

// Estado inicial
const initialState = {
  status: AUTH_STATUS.IDLE,
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
  telegramSync: {
    isLinked: false,
    telegramId: null,
    linkedAt: null,
    lastSync: null
  }
};

// Actions do reducer
const AUTH_ACTIONS = {
  SET_LOADING: 'SET_LOADING',
  SET_AUTHENTICATED: 'SET_AUTHENTICATED',
  SET_UNAUTHENTICATED: 'SET_UNAUTHENTICATED',
  SET_USER: 'SET_USER',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR',
  UPDATE_TELEGRAM_SYNC: 'UPDATE_TELEGRAM_SYNC',
  LOGOUT: 'LOGOUT'
};

// Reducer para gerenciar o estado de autenticação
const authReducer = (state, action) => {
  switch (action.type) {
    case AUTH_ACTIONS.SET_LOADING:
      return {
        ...state,
        isLoading: action.payload,
        status: action.payload ? AUTH_STATUS.LOADING : state.status
      };

    case AUTH_ACTIONS.SET_AUTHENTICATED:
      return {
        ...state,
        status: AUTH_STATUS.AUTHENTICATED,
        user: action.payload.user,
        isAuthenticated: true,
        isLoading: false,
        error: null
      };

    case AUTH_ACTIONS.SET_UNAUTHENTICATED:
      return {
        ...state,
        status: AUTH_STATUS.UNAUTHENTICATED,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
        telegramSync: initialState.telegramSync
      };

    case AUTH_ACTIONS.SET_USER:
      return {
        ...state,
        user: { ...state.user, ...action.payload },
        error: null
      };

    case AUTH_ACTIONS.SET_ERROR:
      return {
        ...state,
        status: AUTH_STATUS.ERROR,
        error: action.payload,
        isLoading: false
      };

    case AUTH_ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null,
        status: state.isAuthenticated ? AUTH_STATUS.AUTHENTICATED : AUTH_STATUS.UNAUTHENTICATED
      };

    case AUTH_ACTIONS.UPDATE_TELEGRAM_SYNC:
      return {
        ...state,
        telegramSync: {
          ...state.telegramSync,
          ...action.payload
        }
      };

    case AUTH_ACTIONS.LOGOUT:
      return {
        ...initialState,
        isLoading: false,
        status: AUTH_STATUS.UNAUTHENTICATED
      };

    default:
      return state;
  }
};

// Criação do contexto
const AuthContext = createContext({});

// Hook para usar o contexto
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  
  return context;
};

// Provider do contexto
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Função para fazer login
  const login = async (credentials, rememberMe = false) => {
    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });

      const result = await authService.login(credentials, rememberMe);
      
      dispatch({
        type: AUTH_ACTIONS.SET_AUTHENTICATED,
        payload: { user: result.user }
      });

      // Atualiza status de sincronização do Telegram
      updateTelegramSyncStatus();

      return result;
    } catch (error) {
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: error.response?.data?.message || 'Erro ao fazer login'
      });
      throw error;
    }
  };

  // Função para fazer cadastro
  const register = async (userData) => {
    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });

      const result = await authService.register(userData);
      
      dispatch({
        type: AUTH_ACTIONS.SET_AUTHENTICATED,
        payload: { user: result.user }
      });

      return result;
    } catch (error) {
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: error.response?.data?.message || 'Erro ao fazer cadastro'
      });
      throw error;
    }
  };

  // Função para fazer logout
  const logout = async (silent = false) => {
    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      
      await authService.logout(silent);
      
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
      // Mesmo com erro, limpa o estado local
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    }
  };

  // Função para atualizar perfil
  const updateProfile = async (profileData) => {
    try {
      dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });

      const result = await authService.updateProfile(profileData);
      
      dispatch({
        type: AUTH_ACTIONS.SET_USER,
        payload: result.user
      });

      return result;
    } catch (error) {
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: error.response?.data?.message || 'Erro ao atualizar perfil'
      });
      throw error;
    }
  };

  // Função para alterar senha
  const changePassword = async (currentPassword, newPassword) => {
    try {
      dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });

      const result = await authService.changePassword(currentPassword, newPassword);
      return result;
    } catch (error) {
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: error.response?.data?.message || 'Erro ao alterar senha'
      });
      throw error;
    }
  };

  // Função para sincronizar com Telegram
  const syncWithTelegram = async (telegramCode) => {
    try {
      dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });

      const result = await authService.syncWithTelegram(telegramCode);
      
      // Atualiza dados do usuário
      if (result.user) {
        dispatch({
          type: AUTH_ACTIONS.SET_USER,
          payload: result.user
        });
      }

      // Atualiza status de sincronização
      updateTelegramSyncStatus();

      return result;
    } catch (error) {
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: error.response?.data?.message || 'Erro ao sincronizar com Telegram'
      });
      throw error;
    }
  };

  // Função para remover sincronização do Telegram
  const unsyncTelegram = async () => {
    try {
      dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });

      const result = await authService.unsyncTelegram();
      
      // Atualiza dados do usuário
      if (result.user) {
        dispatch({
          type: AUTH_ACTIONS.SET_USER,
          payload: result.user
        });
      }

      // Limpa status de sincronização
      dispatch({
        type: AUTH_ACTIONS.UPDATE_TELEGRAM_SYNC,
        payload: initialState.telegramSync
      });

      return result;
    } catch (error) {
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: error.response?.data?.message || 'Erro ao remover sincronização'
      });
      throw error;
    }
  };

  // Função para gerar código de sincronização
  const generateTelegramSyncCode = async () => {
    try {
      dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
      
      const result = await authService.generateTelegramSyncCode();
      return result;
    } catch (error) {
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: error.response?.data?.message || 'Erro ao gerar código'
      });
      throw error;
    }
  };

  // Função para atualizar status de sincronização do Telegram
  const updateTelegramSyncStatus = () => {
    const syncStatus = authService.getTelegramSyncStatus();
    dispatch({
      type: AUTH_ACTIONS.UPDATE_TELEGRAM_SYNC,
      payload: syncStatus
    });
  };

  // Função para excluir conta
  const deleteAccount = async (password) => {
    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });

      const result = await authService.deleteAccount(password);
      
      dispatch({ type: AUTH_ACTIONS.LOGOUT });

      return result;
    } catch (error) {
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: error.response?.data?.message || 'Erro ao excluir conta'
      });
      throw error;
    }
  };

  // Função para limpar erros
  const clearError = () => {
    dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
  };

  // Função para recarregar dados do usuário
  const reloadUser = async () => {
    try {
      const isValid = await authService.validateToken();
      
      if (isValid) {
        const user = authService.getCurrentUser();
        dispatch({
          type: AUTH_ACTIONS.SET_USER,
          payload: user
        });
        updateTelegramSyncStatus();
      } else {
        dispatch({ type: AUTH_ACTIONS.SET_UNAUTHENTICATED });
      }
    } catch (error) {
      console.error('Erro ao recarregar usuário:', error);
      dispatch({ type: AUTH_ACTIONS.SET_UNAUTHENTICATED });
    }
  };

  // Efeito para inicializar a autenticação
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });

        // Inicializa o serviço de autenticação
        await authService.initialize();
      } catch (error) {
        console.error('Erro ao inicializar autenticação:', error);
        dispatch({ type: AUTH_ACTIONS.SET_UNAUTHENTICATED });
      }
    };

    initializeAuth();
  }, []);

  // Listeners para eventos de autenticação
  useEffect(() => {
    const handleAuthInitialized = (event) => {
      const { user, isAuthenticated } = event.detail;
      
      if (isAuthenticated && user) {
        dispatch({
          type: AUTH_ACTIONS.SET_AUTHENTICATED,
          payload: { user }
        });
        updateTelegramSyncStatus();
      } else {
        dispatch({ type: AUTH_ACTIONS.SET_UNAUTHENTICATED });
      }
    };

    const handleAuthLogin = (event) => {
      const { user } = event.detail;
      dispatch({
        type: AUTH_ACTIONS.SET_AUTHENTICATED,
        payload: { user }
      });
      updateTelegramSyncStatus();
    };

    const handleAuthLogout = () => {
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    };

    const handleAccountDeleted = () => {
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    };

    // Adiciona listeners
    window.addEventListener('auth:initialized', handleAuthInitialized);
    window.addEventListener('auth:login', handleAuthLogin);
    window.addEventListener('auth:logout', handleAuthLogout);
    window.addEventListener('auth:account-deleted', handleAccountDeleted);

    // Remove listeners na limpeza
    return () => {
      window.removeEventListener('auth:initialized', handleAuthInitialized);
      window.removeEventListener('auth:login', handleAuthLogin);
      window.removeEventListener('auth:logout', handleAuthLogout);
      window.removeEventListener('auth:account-deleted', handleAccountDeleted);
    };
  }, []);

  // Valor do contexto
  const contextValue = {
    // Estado
    ...state,
    
    // Funções
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    syncWithTelegram,
    unsyncTelegram,
    generateTelegramSyncCode,
    deleteAccount,
    clearError,
    reloadUser
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;