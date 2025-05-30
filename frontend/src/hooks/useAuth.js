// hooks/useAuth.js
import { useContext } from 'react';
import AuthContext from '../contexts/AuthContext';

/**
 * Hook para usar o contexto de autenticação
 * Já exportado no AuthContext, mas mantido aqui para compatibilidade
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  
  return context;
};

export default useAuth;

// hooks/useLocalStorage.js
import { useState, useEffect } from 'react';

/**
 * Hook para gerenciar estado sincronizado com localStorage
 */
export const useLocalStorage = (key, initialValue) => {
  // Estado para armazenar o valor
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Erro ao ler localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Função para definir valor
  const setValue = (value) => {
    try {
      // Permite que value seja uma função (como useState)
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Erro ao definir localStorage key "${key}":`, error);
    }
  };

  return [storedValue, setValue];
};

// hooks/useDebounce.js
import { useState, useEffect } from 'react';

/**
 * Hook para debounce de valores
 */
export const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

// hooks/useOnlineStatus.js
import { useState, useEffect } from 'react';

/**
 * Hook para detectar status online/offline
 */
export const useOnlineStatus = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
};

// hooks/useWindowSize.js
import { useState, useEffect } from 'react';

/**
 * Hook para detectar tamanho da janela
 */
export const useWindowSize = () => {
  const [windowSize, setWindowSize] = useState({
    width: undefined,
    height: undefined,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Chama uma vez para definir o tamanho inicial

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
};

// hooks/useClickOutside.js
import { useEffect, useRef } from 'react';

/**
 * Hook para detectar cliques fora de um elemento
 */
export const useClickOutside = (callback) => {
  const ref = useRef();

  useEffect(() => {
    const handleClick = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        callback();
      }
    };

    document.addEventListener('mousedown', handleClick);
    document.addEventListener('touchstart', handleClick);

    return () => {
      document.removeEventListener('mousedown', handleClick);
      document.removeEventListener('touchstart', handleClick);
    };
  }, [callback]);

  return ref;
};

// hooks/useKeyPress.js
import { useState, useEffect } from 'react';

/**
 * Hook para detectar pressionamento de teclas
 */
export const useKeyPress = (targetKey) => {
  const [keyPressed, setKeyPressed] = useState(false);

  useEffect(() => {
    const downHandler = ({ key }) => {
      if (key === targetKey) {
        setKeyPressed(true);
      }
    };

    const upHandler = ({ key }) => {
      if (key === targetKey) {
        setKeyPressed(false);
      }
    };

    window.addEventListener('keydown', downHandler);
    window.addEventListener('keyup', upHandler);

    return () => {
      window.removeEventListener('keydown', downHandler);
      window.removeEventListener('keyup', upHandler);
    };
  }, [targetKey]);

  return keyPressed;
};

// hooks/useToggle.js
import { useState, useCallback } from 'react';

/**
 * Hook para toggle de valores booleanos
 */
export const useToggle = (initialValue = false) => {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => {
    setValue(v => !v);
  }, []);

  const setTrue = useCallback(() => {
    setValue(true);
  }, []);

  const setFalse = useCallback(() => {
    setValue(false);
  }, []);

  return [value, toggle, setTrue, setFalse];
};

// hooks/useAsync.js
import { useState, useEffect, useCallback } from 'react';

/**
 * Hook para gerenciar operações assíncronas
 */
export const useAsync = (asyncFunction, immediate = true) => {
  const [status, setStatus] = useState('idle');
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const execute = useCallback(async (...args) => {
    setStatus('pending');
    setData(null);
    setError(null);

    try {
      const response = await asyncFunction(...args);
      setData(response);
      setStatus('success');
      return response;
    } catch (error) {
      setError(error);
      setStatus('error');
      throw error;
    }
  }, [asyncFunction]);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  return {
    execute,
    status,
    data,
    error,
    isIdle: status === 'idle',
    isPending: status === 'pending',
    isSuccess: status === 'success',
    isError: status === 'error',
  };
};

// hooks/usePrevious.js
import { useEffect, useRef } from 'react';

/**
 * Hook para obter valor anterior
 */
export const usePrevious = (value) => {
  const ref = useRef();
  
  useEffect(() => {
    ref.current = value;
  });
  
  return ref.current;
};

// hooks/useInterval.js
import { useEffect, useRef } from 'react';

/**
 * Hook para intervalos
 */
export const useInterval = (callback, delay) => {
  const savedCallback = useRef();

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    const tick = () => {
      savedCallback.current();
    };

    if (delay !== null) {
      const id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
};

// hooks/useScrollPosition.js
import { useState, useEffect } from 'react';

/**
 * Hook para detectar posição do scroll
 */
export const useScrollPosition = () => {
  const [scrollPosition, setScrollPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const updatePosition = () => {
      setScrollPosition({ x: window.pageXOffset, y: window.pageYOffset });
    };

    window.addEventListener('scroll', updatePosition);
    updatePosition();

    return () => window.removeEventListener('scroll', updatePosition);
  }, []);

  return scrollPosition;
};

// hooks/useMediaQuery.js
import { useState, useEffect } from 'react';

/**
 * Hook para media queries
 */
export const useMediaQuery = (query) => {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    
    if (media.matches !== matches) {
      setMatches(media.matches);
    }

    const listener = () => setMatches(media.matches);
    
    if (typeof media.addEventListener === 'function') {
      media.addEventListener('change', listener);
    } else {
      // Fallback para navegadores mais antigos
      media.addListener(listener);
    }

    return () => {
      if (typeof media.removeEventListener === 'function') {
        media.removeEventListener('change', listener);
      } else {
        media.removeListener(listener);
      }
    };
  }, [matches, query]);

  return matches;
};

// hooks/useClipboard.js
import { useState } from 'react';
import { copyToClipboard } from '../utils/helpers';

/**
 * Hook para operações de clipboard
 */
export const useClipboard = (text, { successDuration = 1000 } = {}) => {
  const [isCopied, setIsCopied] = useState(false);

  const copy = async (value = text) => {
    const didCopy = await copyToClipboard(value);
    setIsCopied(didCopy);

    if (didCopy) {
      setTimeout(() => {
        setIsCopied(false);
      }, successDuration);
    }

    return didCopy;
  };

  return [isCopied, copy];
};

// hooks/useGeolocation.js
import { useState, useEffect } from 'react';

/**
 * Hook para geolocalização
 */
export const useGeolocation = (options = {}) => {
  const [location, setLocation] = useState({
    loading: true,
    accuracy: null,
    altitude: null,
    altitudeAccuracy: null,
    heading: null,
    latitude: null,
    longitude: null,
    speed: null,
    timestamp: null,
    error: null,
  });

  useEffect(() => {
    if (!navigator.geolocation) {
      setLocation(prev => ({
        ...prev,
        loading: false,
        error: {
          code: 0,
          message: 'Geolocalização não é suportada por este navegador.'
        }
      }));
      return;
    }

    const handleSuccess = (position) => {
      const { coords, timestamp } = position;
      
      setLocation({
        loading: false,
        accuracy: coords.accuracy,
        altitude: coords.altitude,
        altitudeAccuracy: coords.altitudeAccuracy,
        heading: coords.heading,
        latitude: coords.latitude,
        longitude: coords.longitude,
        speed: coords.speed,
        timestamp,
        error: null,
      });
    };

    const handleError = (error) => {
      setLocation(prev => ({
        ...prev,
        loading: false,
        error: {
          code: error.code,
          message: error.message,
        },
      }));
    };

    navigator.geolocation.getCurrentPosition(
      handleSuccess,
      handleError,
      options
    );
  }, [options]);

  return location;
};

// hooks/index.js - Arquivo de índice para exportar todos os hooks
export { useAuth } from './useAuth';
export { useLocalStorage } from './useLocalStorage';
export { useDebounce } from './useDebounce';
export { useOnlineStatus } from './useOnlineStatus';
export { useWindowSize } from './useWindowSize';
export { useClickOutside } from './useClickOutside';
export { useKeyPress } from './useKeyPress';
export { useToggle } from './useToggle';
export { useAsync } from './useAsync';
export { usePrevious } from './usePrevious';
export { useInterval } from './useInterval';
export { useScrollPosition } from './useScrollPosition';
export { useMediaQuery } from './useMediaQuery';
export { useClipboard } from './useClipboard';
export { useGeolocation } from './useGeolocation';