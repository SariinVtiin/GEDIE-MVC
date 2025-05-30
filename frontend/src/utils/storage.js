/**
 * Utilitário para gerenciar localStorage de forma segura
 */

import { STORAGE_KEYS } from './constants';

/**
 * Verifica se localStorage está disponível
 */
const isStorageAvailable = () => {
  try {
    const test = '__storage_test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch {
    return false;
  }
};

/**
 * Armazena um item no localStorage de forma segura
 */
export const setItem = (key, value) => {
  if (!isStorageAvailable()) {
    console.warn('localStorage não está disponível');
    return false;
  }

  try {
    const serializedValue = JSON.stringify(value);
    localStorage.setItem(key, serializedValue);
    return true;
  } catch (error) {
    console.error(`Erro ao armazenar item '${key}':`, error);
    return false;
  }
};

/**
 * Recupera um item do localStorage de forma segura
 */
export const getItem = (key, defaultValue = null) => {
  if (!isStorageAvailable()) {
    return defaultValue;
  }

  try {
    const item = localStorage.getItem(key);
    if (item === null) {
      return defaultValue;
    }
    return JSON.parse(item);
  } catch (error) {
    console.error(`Erro ao recuperar item '${key}':`, error);
    return defaultValue;
  }
};

/**
 * Remove um item do localStorage
 */
export const removeItem = (key) => {
  if (!isStorageAvailable()) {
    return false;
  }

  try {
    localStorage.removeItem(key);
    return true;
  } catch (error) {
    console.error(`Erro ao remover item '${key}':`, error);
    return false;
  }
};

/**
 * Limpa todo o localStorage
 */
export const clear = () => {
  if (!isStorageAvailable()) {
    return false;
  }

  try {
    localStorage.clear();
    return true;
  } catch (error) {
    console.error('Erro ao limpar localStorage:', error);
    return false;
  }
};

/**
 * Verifica se um item existe no localStorage
 */
export const hasItem = (key) => {
  if (!isStorageAvailable()) {
    return false;
  }

  return localStorage.getItem(key) !== null;
};

/**
 * Obtém todos os itens do localStorage com um prefixo específico
 */
export const getItemsByPrefix = (prefix) => {
  if (!isStorageAvailable()) {
    return {};
  }

  const items = {};
  
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(prefix)) {
        items[key] = getItem(key);
      }
    }
  } catch (error) {
    console.error(`Erro ao recuperar itens com prefixo '${prefix}':`, error);
  }

  return items;
};

/**
 * Remove todos os itens com um prefixo específico
 */
export const removeItemsByPrefix = (prefix) => {
  if (!isStorageAvailable()) {
    return false;
  }

  try {
    const keysToRemove = [];
    
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(prefix)) {
        keysToRemove.push(key);
      }
    }

    keysToRemove.forEach(key => localStorage.removeItem(key));
    return true;
  } catch (error) {
    console.error(`Erro ao remover itens com prefixo '${prefix}':`, error);
    return false;
  }
};

// Funções específicas para tokens de autenticação
export const auth = {
  /**
   * Armazena tokens de autenticação
   */
  setTokens: (accessToken, refreshToken, rememberMe = false) => {
    setItem(STORAGE_KEYS.ACCESS_TOKEN, accessToken);
    
    if (rememberMe) {
      setItem(STORAGE_KEYS.REFRESH_TOKEN, refreshToken);
      setItem(STORAGE_KEYS.REMEMBER_ME, true);
    }
  },

  /**
   * Recupera token de acesso
   */
  getAccessToken: () => {
    return getItem(STORAGE_KEYS.ACCESS_TOKEN);
  },

  /**
   * Recupera token de refresh
   */
  getRefreshToken: () => {
    return getItem(STORAGE_KEYS.REFRESH_TOKEN);
  },

  /**
   * Verifica se o usuário escolheu "lembrar-me"
   */
  getRememberMe: () => {
    return getItem(STORAGE_KEYS.REMEMBER_ME, false);
  },

  /**
   * Remove tokens de autenticação
   */
  clearTokens: () => {
    removeItem(STORAGE_KEYS.ACCESS_TOKEN);
    removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    removeItem(STORAGE_KEYS.REMEMBER_ME);
  },

  /**
   * Verifica se o usuário está autenticado (tem token válido)
   */
  isAuthenticated: () => {
    return hasItem(STORAGE_KEYS.ACCESS_TOKEN);
  }
};

// Funções específicas para dados do usuário
export const user = {
  /**
   * Armazena dados do usuário
   */
  setData: (userData) => {
    setItem(STORAGE_KEYS.USER_DATA, userData);
  },

  /**
   * Recupera dados do usuário
   */
  getData: () => {
    return getItem(STORAGE_KEYS.USER_DATA);
  },

  /**
   * Atualiza dados específicos do usuário
   */
  updateData: (updates) => {
    const currentData = getItem(STORAGE_KEYS.USER_DATA, {});
    const updatedData = { ...currentData, ...updates };
    setItem(STORAGE_KEYS.USER_DATA, updatedData);
  },

  /**
   * Remove dados do usuário
   */
  clearData: () => {
    removeItem(STORAGE_KEYS.USER_DATA);
  }
};

// Funções específicas para configurações
export const settings = {
  /**
   * Define tema da aplicação
   */
  setTheme: (theme) => {
    setItem(STORAGE_KEYS.THEME, theme);
  },

  /**
   * Recupera tema da aplicação
   */
  getTheme: () => {
    return getItem(STORAGE_KEYS.THEME, 'light');
  },

  /**
   * Define idioma da aplicação
   */
  setLanguage: (language) => {
    setItem(STORAGE_KEYS.LANGUAGE, language);
  },

  /**
   * Recupera idioma da aplicação
   */
  getLanguage: () => {
    return getItem(STORAGE_KEYS.LANGUAGE, 'pt-BR');
  }
};

// Funções específicas para sincronização com Telegram
export const telegram = {
  /**
   * Armazena dados de sincronização com Telegram
   */
  setSyncData: (syncData) => {
    setItem(STORAGE_KEYS.TELEGRAM_SYNC, syncData);
  },

  /**
   * Recupera dados de sincronização com Telegram
   */
  getSyncData: () => {
    return getItem(STORAGE_KEYS.TELEGRAM_SYNC);
  },

  /**
   * Remove dados de sincronização com Telegram
   */
  clearSyncData: () => {
    removeItem(STORAGE_KEYS.TELEGRAM_SYNC);
  },

  /**
   * Verifica se está sincronizado com Telegram
   */
  isSynced: () => {
    const syncData = getItem(STORAGE_KEYS.TELEGRAM_SYNC);
    return syncData && syncData.isLinked;
  }
};

/**
 * Limpa todos os dados da aplicação
 */
export const clearAllAppData = () => {
  auth.clearTokens();
  user.clearData();
  telegram.clearSyncData();
  
  // Remove outros dados específicos da aplicação
  removeItemsByPrefix('gedie_');
};

/**
 * Migra dados de versões antigas (se necessário)
 */
export const migrateData = () => {
  // Implementar migrações de dados se necessário
  // Por exemplo, mudanças na estrutura de dados entre versões
  const version = getItem('app_version', '1.0.0');
  
  // Exemplo de migração
  if (version === '1.0.0') {
    // Migrar dados específicos
    setItem('app_version', '1.1.0');
  }
};

/**
 * Exporta dados para backup
 */
export const exportData = () => {
  if (!isStorageAvailable()) {
    return null;
  }

  const data = {};
  const appKeys = Object.values(STORAGE_KEYS);
  
  appKeys.forEach(key => {
    if (hasItem(key)) {
      data[key] = getItem(key);
    }
  });

  return {
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    data
  };
};

/**
 * Importa dados de backup
 */
export const importData = (backupData) => {
  if (!backupData || !backupData.data) {
    return false;
  }

  try {
    Object.entries(backupData.data).forEach(([key, value]) => {
      setItem(key, value);
    });
    return true;
  } catch (error) {
    console.error('Erro ao importar dados:', error);
    return false;
  }
};

export default {
  setItem,
  getItem,
  removeItem,
  clear,
  hasItem,
  getItemsByPrefix,
  removeItemsByPrefix,
  auth,
  user,
  settings,
  telegram,
  clearAllAppData,
  migrateData,
  exportData,
  importData,
  isStorageAvailable
};