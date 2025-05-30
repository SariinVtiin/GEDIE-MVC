/**
 * Cliente HTTP para comunicação com a API do backend
 */

import axios from 'axios';
import { toast } from 'react-hot-toast';
import { API_BASE_URL, HTTP_STATUS, ERROR_MESSAGES } from '../utils/constants';
import storage from '../utils/storage';

// Configuração da instância do axios
const httpClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 segundos
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Contador de requisições em andamento
let requestCount = 0;

// Interceptor de requisições
httpClient.interceptors.request.use(
  (config) => {
    // Incrementa contador de requisições
    requestCount++;
    
    // Adiciona token de autenticação se disponível
    const token = storage.auth.getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Log da requisição (apenas em desenvolvimento)
    if (process.env.NODE_ENV === 'development') {
      console.log(`🚀 [${config.method?.toUpperCase()}] ${config.url}`, config.data);
    }

    return config;
  },
  (error) => {
    requestCount--;
    console.error('Erro na configuração da requisição:', error);
    return Promise.reject(error);
  }
);

// Interceptor de respostas
httpClient.interceptors.response.use(
  (response) => {
    // Decrementa contador de requisições
    requestCount--;

    // Log da resposta (apenas em desenvolvimento)
    if (process.env.NODE_ENV === 'development') {
      console.log(`✅ [${response.status}] ${response.config.url}`, response.data);
    }

    return response;
  },
  async (error) => {
    // Decrementa contador de requisições
    requestCount--;

    const originalRequest = error.config;

    // Log do erro (apenas em desenvolvimento)
    if (process.env.NODE_ENV === 'development') {
      console.error(`❌ [${error.response?.status}] ${originalRequest.url}`, error.response?.data);
    }

    // Trata erro de token expirado
    if (error.response?.status === HTTP_STATUS.UNAUTHORIZED && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = storage.auth.getRefreshToken();
        
        if (refreshToken) {
          // Tenta renovar o token
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refreshToken
          });

          const { accessToken, refreshToken: newRefreshToken } = response.data;
          
          // Atualiza tokens no storage
          storage.auth.setTokens(accessToken, newRefreshToken, storage.auth.getRememberMe());
          
          // Refaz a requisição original com o novo token
          originalRequest.headers.Authorization = `Bearer ${accessToken}`;
          return httpClient(originalRequest);
        }
      } catch (refreshError) {
        // Se falhar ao renovar token, limpa autenticação
        storage.auth.clearTokens();
        storage.user.clearData();
        
        // Redireciona para login (pode ser feito via evento)
        window.dispatchEvent(new CustomEvent('auth:logout'));
        
        toast.error(ERROR_MESSAGES.UNAUTHORIZED);
        return Promise.reject(refreshError);
      }
    }

    // Trata outros erros HTTP
    const errorMessage = getErrorMessage(error);
    
    // Só mostra toast de erro se não for uma requisição silenciosa
    if (!originalRequest.silent) {
      toast.error(errorMessage);
    }

    return Promise.reject(error);
  }
);

/**
 * Extrai mensagem de erro apropriada
 */
const getErrorMessage = (error) => {
  if (!error.response) {
    return ERROR_MESSAGES.NETWORK_ERROR;
  }

  const { status, data } = error.response;

  // Mensagens específicas baseadas no status
  switch (status) {
    case HTTP_STATUS.UNAUTHORIZED:
      return ERROR_MESSAGES.UNAUTHORIZED;
    case HTTP_STATUS.FORBIDDEN:
      return ERROR_MESSAGES.FORBIDDEN;
    case HTTP_STATUS.NOT_FOUND:
      return ERROR_MESSAGES.NOT_FOUND;
    case HTTP_STATUS.CONFLICT:
      return data?.message || ERROR_MESSAGES.EMAIL_ALREADY_EXISTS;
    case HTTP_STATUS.UNPROCESSABLE_ENTITY:
      return data?.message || ERROR_MESSAGES.VALIDATION_ERROR;
    case HTTP_STATUS.INTERNAL_SERVER_ERROR:
      return ERROR_MESSAGES.SERVER_ERROR;
    case HTTP_STATUS.SERVICE_UNAVAILABLE:
      return 'Serviço temporariamente indisponível. Tente novamente em alguns minutos.';
    default:
      return data?.message || ERROR_MESSAGES.GENERIC_ERROR;
  }
};

/**
 * Wrapper para requisições GET
 */
export const get = async (url, config = {}) => {
  try {
    const response = await httpClient.get(url, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Wrapper para requisições POST
 */
export const post = async (url, data = {}, config = {}) => {
  try {
    const response = await httpClient.post(url, data, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Wrapper para requisições PUT
 */
export const put = async (url, data = {}, config = {}) => {
  try {
    const response = await httpClient.put(url, data, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Wrapper para requisições PATCH
 */
export const patch = async (url, data = {}, config = {}) => {
  try {
    const response = await httpClient.patch(url, data, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Wrapper para requisições DELETE
 */
export const del = async (url, config = {}) => {
  try {
    const response = await httpClient.delete(url, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Upload de arquivos
 */
export const upload = async (url, file, onProgress = null, config = {}) => {
  const formData = new FormData();
  formData.append('file', file);

  const uploadConfig = {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress) {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onProgress(progress);
      }
    },
    ...config
  };

  try {
    const response = await httpClient.post(url, formData, uploadConfig);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Download de arquivos
 */
export const download = async (url, filename = null, config = {}) => {
  const downloadConfig = {
    responseType: 'blob',
    ...config
  };

  try {
    const response = await httpClient.get(url, downloadConfig);
    
    // Cria um link temporário para download
    const blob = new Blob([response.data]);
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    link.href = downloadUrl;
    link.download = filename || 'download';
    document.body.appendChild(link);
    link.click();
    
    // Limpa o link temporário
    document.body.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Requisição silenciosa (sem toast de erro)
 */
export const silent = (requestFn) => {
  return (...args) => {
    const config = args[args.length - 1] || {};
    config.silent = true;
    args[args.length - 1] = config;
    return requestFn(...args);
  };
};

/**
 * Verifica se há requisições em andamento
 */
export const isLoading = () => {
  return requestCount > 0;
};

/**
 * Cancela todas as requisições pendentes
 */
export const cancelAll = () => {
  const cancelTokenSource = axios.CancelToken.source();
  cancelTokenSource.cancel('Operação cancelada pelo usuário');
};

/**
 * Configura baseURL dinamicamente
 */
export const setBaseURL = (baseURL) => {
  httpClient.defaults.baseURL = baseURL;
};

/**
 * Adiciona header customizado
 */
export const setHeader = (key, value) => {
  httpClient.defaults.headers.common[key] = value;
};

/**
 * Remove header customizado
 */
export const removeHeader = (key) => {
  delete httpClient.defaults.headers.common[key];
};

/**
 * Configurações para requisições específicas
 */
export const withConfig = (config) => ({
  get: (url, extraConfig = {}) => get(url, { ...config, ...extraConfig }),
  post: (url, data, extraConfig = {}) => post(url, data, { ...config, ...extraConfig }),
  put: (url, data, extraConfig = {}) => put(url, data, { ...config, ...extraConfig }),
  patch: (url, data, extraConfig = {}) => patch(url, data, { ...config, ...extraConfig }),
  del: (url, extraConfig = {}) => del(url, { ...config, ...extraConfig })
});

// Funções silenciosas
export const silentGet = silent(get);
export const silentPost = silent(post);
export const silentPut = silent(put);
export const silentPatch = silent(patch);
export const silentDel = silent(del);

export default {
  get,
  post,
  put,
  patch,
  del,
  upload,
  download,
  silent,
  silentGet,
  silentPost,
  silentPut,
  silentPatch,
  silentDel,
  isLoading,
  cancelAll,
  setBaseURL,
  setHeader,
  removeHeader,
  withConfig,
  httpClient
};