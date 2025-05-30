/**
 * Serviço de autenticação para o sistema GEDIE
 */

import { API_ENDPOINTS, SUCCESS_MESSAGES } from '../utils/constants';
import storage from '../utils/storage';
import httpClient from './httpClient';
import { toast } from 'react-hot-toast';

/**
 * Realiza login do usuário
 */
export const login = async (credentials, rememberMe = false) => {
  try {
    const response = await httpClient.post(API_ENDPOINTS.AUTH.LOGIN, {
      email: credentials.email.trim().toLowerCase(),
      password: credentials.password,
      rememberMe
    });

    const { user, accessToken, refreshToken, message } = response;

    // Armazena tokens e dados do usuário
    storage.auth.setTokens(accessToken, refreshToken, rememberMe);
    storage.user.setData(user);

    // Dispara evento de login bem-sucedido
    window.dispatchEvent(new CustomEvent('auth:login', { 
      detail: { user, accessToken } 
    }));

    toast.success(message || SUCCESS_MESSAGES.LOGIN_SUCCESS);

    return { user, accessToken, refreshToken };
  } catch (error) {
    console.error('Erro no login:', error);
    throw error;
  }
};

/**
 * Realiza cadastro de novo usuário
 */
export const register = async (userData) => {
  try {
    const response = await httpClient.post(API_ENDPOINTS.AUTH.REGISTER, {
      name: userData.name.trim(),
      email: userData.email.trim().toLowerCase(),
      password: userData.password,
      phone: userData.phone?.replace(/\D/g, '') || null,
      acceptTerms: userData.acceptTerms
    });

    const { user, accessToken, refreshToken, message } = response;

    // Armazena tokens e dados do usuário
    storage.auth.setTokens(accessToken, refreshToken, false);
    storage.user.setData(user);

    // Dispara evento de cadastro bem-sucedido
    window.dispatchEvent(new CustomEvent('auth:register', { 
      detail: { user, accessToken } 
    }));

    toast.success(message || SUCCESS_MESSAGES.REGISTER_SUCCESS);

    return { user, accessToken, refreshToken };
  } catch (error) {
    console.error('Erro no cadastro:', error);
    throw error;
  }
};

/**
 * Realiza logout do usuário
 */
export const logout = async (silent = false) => {
  try {
    // Tenta fazer logout no servidor (opcional)
    const refreshToken = storage.auth.getRefreshToken();
    if (refreshToken) {
      await httpClient.silentPost(API_ENDPOINTS.AUTH.LOGOUT, { refreshToken });
    }
  } catch (error) {
    console.warn('Erro ao fazer logout no servidor:', error);
  } finally {
    // Limpa dados locais independentemente do resultado
    storage.auth.clearTokens();
    storage.user.clearData();
    storage.telegram.clearSyncData();

    // Dispara evento de logout
    window.dispatchEvent(new CustomEvent('auth:logout'));

    if (!silent) {
      toast.success(SUCCESS_MESSAGES.LOGOUT_SUCCESS);
    }
  }
};

/**
 * Renova token de acesso
 */
export const refreshToken = async () => {
  try {
    const refreshToken = storage.auth.getRefreshToken();
    
    if (!refreshToken) {
      throw new Error('Token de refresh não encontrado');
    }

    const response = await httpClient.post(API_ENDPOINTS.AUTH.REFRESH, {
      refreshToken
    });

    const { accessToken, refreshToken: newRefreshToken } = response;

    // Atualiza tokens no storage
    storage.auth.setTokens(accessToken, newRefreshToken, storage.auth.getRememberMe());

    return { accessToken, refreshToken: newRefreshToken };
  } catch (error) {
    console.error('Erro ao renovar token:', error);
    
    // Se falhar, limpa autenticação
    await logout(true);
    throw error;
  }
};

/**
 * Verifica se o usuário está autenticado
 */
export const isAuthenticated = () => {
  return storage.auth.isAuthenticated();
};

/**
 * Obtém dados do usuário atual
 */
export const getCurrentUser = () => {
  return storage.user.getData();
};

/**
 * Obtém token de acesso atual
 */
export const getAccessToken = () => {
  return storage.auth.getAccessToken();
};

/**
 * Verifica e valida token atual
 */
export const validateToken = async () => {
  try {
    if (!isAuthenticated()) {
      return false;
    }

    // Faz uma requisição simples para validar o token
    const response = await httpClient.silentGet(API_ENDPOINTS.AUTH.PROFILE);
    
    // Atualiza dados do usuário se necessário
    if (response.user) {
      storage.user.setData(response.user);
    }

    return true;
  } catch (error) {
    console.warn('Token inválido:', error);
    
    // Tenta renovar o token
    try {
      await refreshToken();
      return true;
    } catch (refreshError) {
      console.error('Erro ao renovar token:', refreshError);
      await logout(true);
      return false;
    }
  }
};

/**
 * Solicita recuperação de senha
 */
export const forgotPassword = async (email) => {
  try {
    const response = await httpClient.post(API_ENDPOINTS.AUTH.FORGOT_PASSWORD, {
      email: email.trim().toLowerCase()
    });

    toast.success(response.message || 'Email de recuperação enviado com sucesso!');
    
    return response;
  } catch (error) {
    console.error('Erro ao solicitar recuperação de senha:', error);
    throw error;
  }
};

/**
 * Redefine senha com token
 */
export const resetPassword = async (token, newPassword) => {
  try {
    const response = await httpClient.post(API_ENDPOINTS.AUTH.RESET_PASSWORD, {
      token,
      password: newPassword
    });

    toast.success(response.message || 'Senha redefinida com sucesso!');
    
    return response;
  } catch (error) {
    console.error('Erro ao redefinir senha:', error);
    throw error;
  }
};

/**
 * Verifica email com token
 */
export const verifyEmail = async (token) => {
  try {
    const response = await httpClient.post(API_ENDPOINTS.AUTH.VERIFY_EMAIL, {
      token
    });

    // Atualiza dados do usuário
    if (response.user) {
      storage.user.setData(response.user);
    }

    toast.success(response.message || SUCCESS_MESSAGES.EMAIL_VERIFIED);
    
    return response;
  } catch (error) {
    console.error('Erro ao verificar email:', error);
    throw error;
  }
};

/**
 * Atualiza perfil do usuário
 */
export const updateProfile = async (profileData) => {
  try {
    const response = await httpClient.put(API_ENDPOINTS.AUTH.PROFILE, {
      name: profileData.name?.trim(),
      email: profileData.email?.trim().toLowerCase(),
      phone: profileData.phone?.replace(/\D/g, '') || null,
      timezone: profileData.timezone,
      language: profileData.language
    });

    // Atualiza dados do usuário no storage
    if (response.user) {
      storage.user.setData(response.user);
    }

    toast.success(response.message || SUCCESS_MESSAGES.PROFILE_UPDATED);
    
    return response;
  } catch (error) {
    console.error('Erro ao atualizar perfil:', error);
    throw error;
  }
};

/**
 * Altera senha do usuário
 */
export const changePassword = async (currentPassword, newPassword) => {
  try {
    const response = await httpClient.post('/auth/change-password', {
      currentPassword,
      newPassword
    });

    toast.success(response.message || SUCCESS_MESSAGES.PASSWORD_CHANGED);
    
    return response;
  } catch (error) {
    console.error('Erro ao alterar senha:', error);
    throw error;
  }
};

/**
 * Sincroniza conta com Telegram
 */
export const syncWithTelegram = async (telegramCode) => {
  try {
    const response = await httpClient.post(API_ENDPOINTS.USERS.SYNC_TELEGRAM, {
      code: telegramCode.trim()
    });

    // Atualiza dados de sincronização
    if (response.syncData) {
      storage.telegram.setSyncData(response.syncData);
    }

    // Atualiza dados do usuário
    if (response.user) {
      storage.user.setData(response.user);
    }

    toast.success(response.message || SUCCESS_MESSAGES.SYNC_SUCCESS);
    
    return response;
  } catch (error) {
    console.error('Erro ao sincronizar com Telegram:', error);
    throw error;
  }
};

/**
 * Remove sincronização com Telegram
 */
export const unsyncTelegram = async () => {
  try {
    const response = await httpClient.delete(API_ENDPOINTS.USERS.SYNC_TELEGRAM);

    // Remove dados de sincronização
    storage.telegram.clearSyncData();

    // Atualiza dados do usuário
    if (response.user) {
      storage.user.setData(response.user);
    }

    toast.success(response.message || 'Sincronização removida com sucesso!');
    
    return response;
  } catch (error) {
    console.error('Erro ao remover sincronização:', error);
    throw error;
  }
};

/**
 * Verifica status de sincronização com Telegram
 */
export const getTelegramSyncStatus = () => {
  const syncData = storage.telegram.getSyncData();
  const user = getCurrentUser();
  
  return {
    isLinked: syncData?.isLinked || false,
    telegramId: syncData?.telegramId || user?.telegramId || null,
    linkedAt: syncData?.linkedAt || null,
    lastSync: syncData?.lastSync || null
  };
};

/**
 * Gera código de sincronização com Telegram
 */
export const generateTelegramSyncCode = async () => {
  try {
    const response = await httpClient.post('/auth/generate-telegram-code');
    
    return {
      code: response.code,
      expiresAt: response.expiresAt,
      instructions: response.instructions
    };
  } catch (error) {
    console.error('Erro ao gerar código de sincronização:', error);
    throw error;
  }
};

/**
 * Exclui conta do usuário
 */
export const deleteAccount = async (password) => {
  try {
    const response = await httpClient.delete(API_ENDPOINTS.USERS.DELETE, {
      data: { password }
    });

    // Limpa todos os dados locais
    storage.clearAllAppData();

    // Dispara evento de exclusão de conta
    window.dispatchEvent(new CustomEvent('auth:account-deleted'));

    toast.success(response.message || 'Conta excluída com sucesso!');
    
    return response;
  } catch (error) {
    console.error('Erro ao excluir conta:', error);
    throw error;
  }
};

/**
 * Inicializa o serviço de autenticação
 */
export const initialize = async () => {
  try {
    // Migra dados se necessário
    storage.migrateData();

    // Se está autenticado, valida o token
    if (isAuthenticated()) {
      const isValid = await validateToken();
      
      if (isValid) {
        // Dispara evento de inicialização bem-sucedida
        const user = getCurrentUser();
        window.dispatchEvent(new CustomEvent('auth:initialized', { 
          detail: { user, isAuthenticated: true } 
        }));
      }
    } else {
      // Dispara evento de não autenticado
      window.dispatchEvent(new CustomEvent('auth:initialized', { 
        detail: { user: null, isAuthenticated: false } 
      }));
    }
  } catch (error) {
    console.error('Erro ao inicializar autenticação:', error);
    
    // Em caso de erro, assume não autenticado
    window.dispatchEvent(new CustomEvent('auth:initialized', { 
      detail: { user: null, isAuthenticated: false } 
    }));
  }
};

export default {
  login,
  register,
  logout,
  refreshToken,
  isAuthenticated,
  getCurrentUser,
  getAccessToken,
  validateToken,
  forgotPassword,
  resetPassword,
  verifyEmail,
  updateProfile,
  changePassword,
  syncWithTelegram,
  unsyncTelegram,
  getTelegramSyncStatus,
  generateTelegramSyncCode,
  deleteAccount,
  initialize
};
