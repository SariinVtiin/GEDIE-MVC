 // utils/helpers.js
  /**
   * Funções utilitárias auxiliares para a aplicação GEDIE
   */
  
  import { CURRENCY_CONFIG, DATE_FORMATS } from './constants';
  
  /**
   * Formata valores monetários
   */
  export const formatCurrency = (value, options = {}) => {
    const {
      locale = CURRENCY_CONFIG.LOCALE,
      currency = CURRENCY_CONFIG.CURRENCY,
      minimumFractionDigits = CURRENCY_CONFIG.DECIMAL_PLACES,
      maximumFractionDigits = CURRENCY_CONFIG.DECIMAL_PLACES
    } = options;
  
    if (value === null || value === undefined || isNaN(value)) {
      return 'R$ 0,00';
    }
  
    try {
      return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency,
        minimumFractionDigits,
        maximumFractionDigits
      }).format(Number(value));
    } catch (error) {
      console.warn('Erro ao formatar moeda:', error);
      return `R$ ${Number(value).toFixed(2).replace('.', ',')}`;
    }
  };
  
  /**
   * Formata datas
   */
  export const formatDate = (date, format = DATE_FORMATS.DISPLAY) => {
    if (!date) return '';
  
    try {
      const dateObj = date instanceof Date ? date : new Date(date);
      
      if (isNaN(dateObj.getTime())) {
        return '';
      }
  
      // Formatação personalizada brasileira
      if (format === DATE_FORMATS.DISPLAY) {
        return dateObj.toLocaleDateString('pt-BR');
      }
      
      if (format === DATE_FORMATS.DATETIME) {
        return dateObj.toLocaleString('pt-BR');
      }
      
      if (format === DATE_FORMATS.TIME) {
        return dateObj.toLocaleTimeString('pt-BR', { 
          hour: '2-digit', 
          minute: '2-digit' 
        });
      }
  
      // Formato ISO para API
      if (format === DATE_FORMATS.API) {
        return dateObj.toISOString().split('T')[0];
      }
  
      return dateObj.toLocaleDateString('pt-BR');
    } catch (error) {
      console.warn('Erro ao formatar data:', error);
      return '';
    }
  };
  
  /**
   * Formata data relativa (há X dias, etc.)
   */
  export const formatRelativeDate = (date) => {
    if (!date) return '';
  
    try {
      const dateObj = date instanceof Date ? date : new Date(date);
      const now = new Date();
      const diffInSeconds = Math.floor((now - dateObj) / 1000);
  
      if (diffInSeconds < 60) {
        return 'agora há pouco';
      }
  
      const diffInMinutes = Math.floor(diffInSeconds / 60);
      if (diffInMinutes < 60) {
        return `há ${diffInMinutes} minuto${diffInMinutes !== 1 ? 's' : ''}`;
      }
  
      const diffInHours = Math.floor(diffInMinutes / 60);
      if (diffInHours < 24) {
        return `há ${diffInHours} hora${diffInHours !== 1 ? 's' : ''}`;
      }
  
      const diffInDays = Math.floor(diffInHours / 24);
      if (diffInDays < 7) {
        return `há ${diffInDays} dia${diffInDays !== 1 ? 's' : ''}`;
      }
  
      const diffInWeeks = Math.floor(diffInDays / 7);
      if (diffInWeeks < 4) {
        return `há ${diffInWeeks} semana${diffInWeeks !== 1 ? 's' : ''}`;
      }
  
      const diffInMonths = Math.floor(diffInDays / 30);
      if (diffInMonths < 12) {
        return `há ${diffInMonths} ${diffInMonths === 1 ? 'mês' : 'meses'}`;
      }
  
      const diffInYears = Math.floor(diffInDays / 365);
      return `há ${diffInYears} ano${diffInYears !== 1 ? 's' : ''}`;
    } catch (error) {
      console.warn('Erro ao formatar data relativa:', error);
      return formatDate(date);
    }
  };
  
  /**
   * Debounce function - atrasa a execução de uma função
   */
  export const debounce = (func, wait, immediate = false) => {
    let timeout;
    
    return function executedFunction(...args) {
      const later = () => {
        timeout = null;
        if (!immediate) func(...args);
      };
      
      const callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      
      if (callNow) func(...args);
    };
  };
  
  /**
   * Throttle function - limita a frequência de execução
   */
  export const throttle = (func, limit) => {
    let inThrottle;
    
    return function executedFunction(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  };
  
  /**
   * Gera um ID único
   */
  export const generateId = (prefix = '') => {
    const timestamp = Date.now().toString(36);
    const randomStr = Math.random().toString(36).substr(2, 5);
    return `${prefix}${timestamp}${randomStr}`;
  };
  
  /**
   * Capitaliza primeira letra
   */
  export const capitalize = (str) => {
    if (!str || typeof str !== 'string') return '';
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
  };
  
  /**
   * Capitaliza cada palavra
   */
  export const capitalizeWords = (str) => {
    if (!str || typeof str !== 'string') return '';
    return str.split(' ').map(capitalize).join(' ');
  };
  
  /**
   * Trunca texto com reticências
   */
  export const truncate = (str, length = 100, suffix = '...') => {
    if (!str || typeof str !== 'string') return '';
    if (str.length <= length) return str;
    return str.substring(0, length).trim() + suffix;
  };
  
  /**
   * Remove acentos de strings
   */
  export const removeAccents = (str) => {
    if (!str || typeof str !== 'string') return '';
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  };
  
  /**
   * Converte string para slug (URL amigável)
   */
  export const slugify = (str) => {
    if (!str || typeof str !== 'string') return '';
    return removeAccents(str)
      .toLowerCase()
      .trim()
      .replace(/[^\w\s-]/g, '')
      .replace(/[\s_-]+/g, '-')
      .replace(/^-+|-+$/g, '');
  };
  
  /**
   * Valida se é um email válido
   */
  export const isValidEmail = (email) => {
    if (!email || typeof email !== 'string') return false;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email.trim().toLowerCase());
  };
  
  /**
   * Valida se é um número válido
   */
  export const isValidNumber = (value) => {
    return !isNaN(value) && isFinite(value);
  };
  
  /**
   * Deep clone de objetos
   */
  export const deepClone = (obj) => {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj.getTime());
    if (obj instanceof Array) return obj.map(item => deepClone(item));
    if (typeof obj === 'object') {
      const clonedObj = {};
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          clonedObj[key] = deepClone(obj[key]);
        }
      }
      return clonedObj;
    }
  };
  
  /**
   * Compara se dois objetos são iguais (shallow)
   */
  export const isEqual = (obj1, obj2) => {
    const keys1 = Object.keys(obj1);
    const keys2 = Object.keys(obj2);
    
    if (keys1.length !== keys2.length) {
      return false;
    }
    
    for (let key of keys1) {
      if (obj1[key] !== obj2[key]) {
        return false;
      }
    }
    
    return true;
  };
  
  /**
   * Agrupa array por propriedade
   */
  export const groupBy = (array, key) => {
    return array.reduce((result, item) => {
      const group = item[key];
      if (!result[group]) {
        result[group] = [];
      }
      result[group].push(item);
      return result;
    }, {});
  };
  
  /**
   * Ordena array de objetos por propriedade
   */
  export const sortBy = (array, key, direction = 'asc') => {
    return [...array].sort((a, b) => {
      const aVal = a[key];
      const bVal = b[key];
      
      if (aVal < bVal) return direction === 'asc' ? -1 : 1;
      if (aVal > bVal) return direction === 'asc' ? 1 : -1;
      return 0;
    });
  };
  
  /**
   * Calcula soma de valores em array
   */
  export const sumBy = (array, key) => {
    return array.reduce((sum, item) => {
      const value = typeof key === 'function' ? key(item) : item[key];
      return sum + (Number(value) || 0);
    }, 0);
  };
  
  /**
   * Filtra valores únicos de array
   */
  export const unique = (array, key = null) => {
    if (!key) {
      return [...new Set(array)];
    }
    
    const seen = new Set();
    return array.filter(item => {
      const value = item[key];
      if (seen.has(value)) {
        return false;
      }
      seen.add(value);
      return true;
    });
  };
  
  /**
   * Converte bytes para formato legível
   */
  export const formatBytes = (bytes, decimals = 2) => {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  };
  
  /**
   * Copia texto para clipboard
   */
  export const copyToClipboard = async (text) => {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        return true;
      } else {
        // Fallback para navegadores mais antigos
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);
        
        return successful;
      }
    } catch (error) {
      console.error('Erro ao copiar para clipboard:', error);
      return false;
    }
  };
  
  /**
   * Detecta se é dispositivo móvel
   */
  export const isMobile = () => {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent
    );
  };
  
  /**
   * Detecta se é iOS
   */
  export const isIOS = () => {
    return /iPad|iPhone|iPod/.test(navigator.userAgent);
  };
  
  /**
   * Detecta se está online
   */
  export const isOnline = () => {
    return navigator.onLine;
  };
  
  /**
   * Scroll suave para elemento
   */
  export const scrollToElement = (elementId, options = {}) => {
    const element = document.getElementById(elementId);
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
        ...options
      });
    }
  };
  
  /**
   * Formata número de telefone brasileiro
   */
  export const formatPhoneNumber = (phone) => {
    if (!phone) return '';
    
    const cleaned = phone.replace(/\D/g, '');
    
    if (cleaned.length === 10) {
      return `(${cleaned.slice(0, 2)}) ${cleaned.slice(2, 6)}-${cleaned.slice(6)}`;
    } else if (cleaned.length === 11) {
      return `(${cleaned.slice(0, 2)}) ${cleaned.slice(2, 7)}-${cleaned.slice(7)}`;
    }
    
    return phone;
  };
  
  /**
   * Extrai iniciais do nome
   */
  export const getInitials = (name) => {
    if (!name || typeof name !== 'string') return '';
    
    return name
      .split(' ')
      .filter(word => word.length > 0)
      .slice(0, 2)
      .map(word => word[0].toUpperCase())
      .join('');
  };
  
  /**
   * Gera cor aleatória
   */
  export const generateRandomColor = () => {
    const colors = [
      '#ef4444', '#f97316', '#f59e0b', '#eab308', '#84cc16',
      '#22c55e', '#10b981', '#14b8a6', '#06b6d4', '#0ea5e9',
      '#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#c084fc',
      '#d946ef', '#ec4899', '#f43f5e'
    ];
    
    return colors[Math.floor(Math.random() * colors.length)];
  };
  
  export default {
    formatCurrency,
    formatDate,
    formatRelativeDate,
    debounce,
    throttle,
    generateId,
    capitalize,
    capitalizeWords,
    truncate,
    removeAccents,
    slugify,
    isValidEmail,
    isValidNumber,
    deepClone,
    isEqual,
    groupBy,
    sortBy,
    sumBy,
    unique,
    formatBytes,
    copyToClipboard,
    isMobile,
    isIOS,
    isOnline,
    scrollToElement,
    formatPhoneNumber,
    getInitials,
    generateRandomColor
  };
