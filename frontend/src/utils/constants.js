/**
 * Constantes utilizadas na aplicação GEDIE
 */

// URLs da API
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    VERIFY_EMAIL: '/auth/verify-email',
    FORGOT_PASSWORD: '/auth/forgot-password',
    RESET_PASSWORD: '/auth/reset-password',
    PROFILE: '/auth/profile'
  },
  USERS: {
    PROFILE: '/users/profile',
    UPDATE: '/users/update',
    DELETE: '/users/delete',
    SYNC_TELEGRAM: '/users/sync-telegram'
  },
  EXPENSES: {
    LIST: '/expenses',
    CREATE: '/expenses',
    UPDATE: '/expenses',
    DELETE: '/expenses',
    STATS: '/expenses/stats',
    EXPORT: '/expenses/export'
  },
  CATEGORIES: {
    LIST: '/categories',
    CREATE: '/categories',
    UPDATE: '/categories',
    DELETE: '/categories'
  },
  DASHBOARD: {
    OVERVIEW: '/dashboard/overview',
    CHARTS: '/dashboard/charts',
    REPORTS: '/dashboard/reports'
  }
};

// Chaves do localStorage
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'gedie_access_token',
  REFRESH_TOKEN: 'gedie_refresh_token',
  USER_DATA: 'gedie_user_data',
  REMEMBER_ME: 'gedie_remember_me',
  THEME: 'gedie_theme',
  LANGUAGE: 'gedie_language',
  TELEGRAM_SYNC: 'gedie_telegram_sync'
};

// Status de autenticação
export const AUTH_STATUS = {
  IDLE: 'idle',
  LOADING: 'loading',
  AUTHENTICATED: 'authenticated',
  UNAUTHENTICATED: 'unauthenticated',
  ERROR: 'error'
};

// Tipos de toast/notificação
export const TOAST_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
  LOADING: 'loading'
};

// Categorias padrão de gastos
export const DEFAULT_CATEGORIES = [
  {
    name: 'Alimentação',
    icon: '🍔',
    color: '#ef4444',
    type: 'expense'
  },
  {
    name: 'Transporte',
    icon: '🚗',
    color: '#3b82f6',
    type: 'expense'
  },
  {
    name: 'Casa',
    icon: '🏠',
    color: '#10b981',
    type: 'expense'
  },
  {
    name: 'Saúde',
    icon: '💊',
    color: '#f59e0b',
    type: 'expense'
  },
  {
    name: 'Lazer',
    icon: '🎬',
    color: '#8b5cf6',
    type: 'expense'
  },
  {
    name: 'Roupas',
    icon: '👕',
    color: '#f97316',
    type: 'expense'
  },
  {
    name: 'Educação',
    icon: '📚',
    color: '#06b6d4',
    type: 'expense'
  },
  {
    name: 'Outros',
    icon: '💳',
    color: '#6b7280',
    type: 'expense'
  }
];

// Períodos para relatórios
export const REPORT_PERIODS = {
  TODAY: 'today',
  WEEK: 'week',
  MONTH: 'month',
  QUARTER: 'quarter',
  YEAR: 'year',
  CUSTOM: 'custom'
};

// Status de requisições HTTP
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503
};

// Mensagens de erro padrão
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Erro de conexão. Verifique sua internet.',
  SERVER_ERROR: 'Erro interno do servidor. Tente novamente.',
  UNAUTHORIZED: 'Sessão expirada. Faça login novamente.',
  FORBIDDEN: 'Você não tem permissão para esta ação.',
  NOT_FOUND: 'Recurso não encontrado.',
  VALIDATION_ERROR: 'Dados inválidos. Verifique os campos.',
  EMAIL_ALREADY_EXISTS: 'Este email já está cadastrado.',
  INVALID_CREDENTIALS: 'Email ou senha inválidos.',
  GENERIC_ERROR: 'Algo deu errado. Tente novamente.'
};

// Mensagens de sucesso
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: 'Login realizado com sucesso!',
  REGISTER_SUCCESS: 'Cadastro realizado com sucesso!',
  LOGOUT_SUCCESS: 'Logout realizado com sucesso!',
  PROFILE_UPDATED: 'Perfil atualizado com sucesso!',
  PASSWORD_CHANGED: 'Senha alterada com sucesso!',
  EMAIL_VERIFIED: 'Email verificado com sucesso!',
  EXPENSE_CREATED: 'Gasto registrado com sucesso!',
  EXPENSE_UPDATED: 'Gasto atualizado com sucesso!',
  EXPENSE_DELETED: 'Gasto excluído com sucesso!',
  CATEGORY_CREATED: 'Categoria criada com sucesso!',
  SYNC_SUCCESS: 'Sincronização realizada com sucesso!'
};

// Configurações de validação
export const VALIDATION_CONFIG = {
  PASSWORD_MIN_LENGTH: 8,
  NAME_MIN_LENGTH: 2,
  NAME_MAX_LENGTH: 50,
  EMAIL_MAX_LENGTH: 100,
  DESCRIPTION_MAX_LENGTH: 255,
  CATEGORY_NAME_MAX_LENGTH: 30
};

// Configurações de paginação
export const PAGINATION_CONFIG = {
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100]
};

// Configurações de upload
export const UPLOAD_CONFIG = {
  MAX_FILE_SIZE: 5 * 1024 * 1024, // 5MB
  ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/webp'],
  MAX_FILES: 1
};

// Configurações de formato de data
export const DATE_FORMATS = {
  DISPLAY: 'dd/MM/yyyy',
  API: 'yyyy-MM-dd',
  DATETIME: 'dd/MM/yyyy HH:mm',
  TIME: 'HH:mm'
};

// Configurações de moeda
export const CURRENCY_CONFIG = {
  LOCALE: 'pt-BR',
  CURRENCY: 'BRL',
  SYMBOL: 'R$',
  DECIMAL_PLACES: 2
};

// Temas disponíveis
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  AUTO: 'auto'
};

// Idiomas disponíveis
export const LANGUAGES = {
  PT_BR: 'pt-BR',
  EN_US: 'en-US',
  ES_ES: 'es-ES'
};

// Configurações de performance
export const PERFORMANCE_CONFIG = {
  DEBOUNCE_DELAY: 300,
  THROTTLE_DELAY: 1000,
  CACHE_TTL: 5 * 60 * 1000, // 5 minutos
  REQUEST_TIMEOUT: 30000 // 30 segundos
};

// Regex patterns
export const REGEX_PATTERNS = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PASSWORD: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/,
  PHONE: /^\(\d{2}\)\s\d{4,5}-\d{4}$/,
  CPF: /^\d{3}\.\d{3}\.\d{3}-\d{2}$/,
  NAME: /^[a-zA-ZÀ-ÿ\s]{2,50}$/,
  CURRENCY: /^\d+([,.]?\d{2})?$/
};

// Configurações do Telegram Bot
export const TELEGRAM_CONFIG = {
  BOT_USERNAME: '@gedie_bot',
  SYNC_CODE_LENGTH: 6,
  SYNC_CODE_EXPIRY: 10 * 60 * 1000 // 10 minutos
};

// Configurações de analytics
export const ANALYTICS_CONFIG = {
  TRACK_PAGE_VIEWS: true,
  TRACK_EVENTS: true,
  TRACK_ERRORS: true,
  SAMPLE_RATE: 0.1 // 10% dos usuários
};

export default {
  API_BASE_URL,
  API_ENDPOINTS,
  STORAGE_KEYS,
  AUTH_STATUS,
  TOAST_TYPES,
  DEFAULT_CATEGORIES,
  REPORT_PERIODS,
  HTTP_STATUS,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES,
  VALIDATION_CONFIG,
  PAGINATION_CONFIG,
  UPLOAD_CONFIG,
  DATE_FORMATS,
  CURRENCY_CONFIG,
  THEMES,
  LANGUAGES,
  PERFORMANCE_CONFIG,
  REGEX_PATTERNS,
  TELEGRAM_CONFIG,
  ANALYTICS_CONFIG
};