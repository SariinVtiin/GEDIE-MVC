/**
 * Utilitários de validação para formulários do GEDIE
 */

// Expressões regulares
const REGEX = {
    email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/,
    phone: /^\(\d{2}\)\s\d{4,5}-\d{4}$/,
    cpf: /^\d{3}\.\d{3}\.\d{3}-\d{2}$/,
    name: /^[a-zA-ZÀ-ÿ\s]{2,50}$/
  };
  
  // Mensagens de erro padrão
  const ERROR_MESSAGES = {
    required: 'Este campo é obrigatório',
    email: 'Digite um email válido',
    password: 'A senha deve ter pelo menos 8 caracteres, incluindo maiúscula, minúscula e número',
    passwordConfirm: 'As senhas não coincidem',
    minLength: (min) => `Deve ter pelo menos ${min} caracteres`,
    maxLength: (max) => `Deve ter no máximo ${max} caracteres`,
    name: 'Nome deve conter apenas letras e espaços',
    phone: 'Formato: (11) 99999-9999',
    cpf: 'CPF inválido',
    terms: 'Você deve aceitar os termos de uso'
  };
  
  /**
   * Valida se um campo é obrigatório
   */
  export const validateRequired = (value) => {
    if (!value || value.toString().trim() === '') {
      return ERROR_MESSAGES.required;
    }
    return null;
  };
  
  /**
   * Valida formato de email
   */
  export const validateEmail = (email) => {
    if (!email) return ERROR_MESSAGES.required;
    
    if (!REGEX.email.test(email.trim())) {
      return ERROR_MESSAGES.email;
    }
    
    return null;
  };
  
  /**
   * Valida senha forte
   */
  export const validatePassword = (password) => {
    if (!password) return ERROR_MESSAGES.required;
    
    if (password.length < 8) {
      return ERROR_MESSAGES.minLength(8);
    }
    
    if (!REGEX.password.test(password)) {
      return ERROR_MESSAGES.password;
    }
    
    return null;
  };
  
  /**
   * Valida confirmação de senha
   */
  export const validatePasswordConfirm = (password, confirmPassword) => {
    if (!confirmPassword) return ERROR_MESSAGES.required;
    
    if (password !== confirmPassword) {
      return ERROR_MESSAGES.passwordConfirm;
    }
    
    return null;
  };
  
  /**
   * Valida nome completo
   */
  export const validateName = (name) => {
    if (!name) return ERROR_MESSAGES.required;
    
    const trimmedName = name.trim();
    
    if (trimmedName.length < 2) {
      return ERROR_MESSAGES.minLength(2);
    }
    
    if (trimmedName.length > 50) {
      return ERROR_MESSAGES.maxLength(50);
    }
    
    if (!REGEX.name.test(trimmedName)) {
      return ERROR_MESSAGES.name;
    }
    
    return null;
  };
  
  /**
   * Valida telefone brasileiro
   */
  export const validatePhone = (phone) => {
    if (!phone) return null; // Telefone é opcional
    
    if (!REGEX.phone.test(phone)) {
      return ERROR_MESSAGES.phone;
    }
    
    return null;
  };
  
  /**
   * Valida CPF brasileiro
   */
  export const validateCPF = (cpf) => {
    if (!cpf) return null; // CPF é opcional
    
    // Remove formatação
    const cleanCPF = cpf.replace(/\D/g, '');
    
    if (cleanCPF.length !== 11) {
      return ERROR_MESSAGES.cpf;
    }
    
    // Verifica se todos os dígitos são iguais
    if (/^(\d)\1+$/.test(cleanCPF)) {
      return ERROR_MESSAGES.cpf;
    }
    
    // Validação do dígito verificador
    let sum = 0;
    for (let i = 0; i < 9; i++) {
      sum += parseInt(cleanCPF[i]) * (10 - i);
    }
    
    let remainder = sum % 11;
    let digit1 = remainder < 2 ? 0 : 11 - remainder;
    
    if (parseInt(cleanCPF[9]) !== digit1) {
      return ERROR_MESSAGES.cpf;
    }
    
    sum = 0;
    for (let i = 0; i < 10; i++) {
      sum += parseInt(cleanCPF[i]) * (11 - i);
    }
    
    remainder = sum % 11;
    let digit2 = remainder < 2 ? 0 : 11 - remainder;
    
    if (parseInt(cleanCPF[10]) !== digit2) {
      return ERROR_MESSAGES.cpf;
    }
    
    return null;
  };
  
  /**
   * Valida checkbox de termos
   */
  export const validateTerms = (accepted) => {
    if (!accepted) {
      return ERROR_MESSAGES.terms;
    }
    return null;
  };
  
  /**
   * Valida formulário de login
   */
  export const validateLoginForm = (data) => {
    const errors = {};
    
    const emailError = validateEmail(data.email);
    if (emailError) errors.email = emailError;
    
    const passwordError = validateRequired(data.password);
    if (passwordError) errors.password = passwordError;
    
    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  };
  
  /**
   * Valida formulário de cadastro
   */
  export const validateRegisterForm = (data) => {
    const errors = {};
    
    const nameError = validateName(data.name);
    if (nameError) errors.name = nameError;
    
    const emailError = validateEmail(data.email);
    if (emailError) errors.email = emailError;
    
    const passwordError = validatePassword(data.password);
    if (passwordError) errors.password = passwordError;
    
    const confirmPasswordError = validatePasswordConfirm(data.password, data.confirmPassword);
    if (confirmPasswordError) errors.confirmPassword = confirmPasswordError;
    
    const phoneError = validatePhone(data.phone);
    if (phoneError) errors.phone = phoneError;
    
    const termsError = validateTerms(data.acceptTerms);
    if (termsError) errors.acceptTerms = termsError;
    
    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  };
  
  /**
   * Sanitiza string removendo caracteres especiais
   */
  export const sanitizeString = (str) => {
    if (!str) return '';
    return str.toString().trim().replace(/[<>]/g, '');
  };
  
  /**
   * Formata telefone brasileiro
   */
  export const formatPhone = (phone) => {
    if (!phone) return '';
    
    const cleanPhone = phone.replace(/\D/g, '');
    
    if (cleanPhone.length === 10) {
      return `(${cleanPhone.slice(0, 2)}) ${cleanPhone.slice(2, 6)}-${cleanPhone.slice(6)}`;
    } else if (cleanPhone.length === 11) {
      return `(${cleanPhone.slice(0, 2)}) ${cleanPhone.slice(2, 7)}-${cleanPhone.slice(7)}`;
    }
    
    return phone;
  };
  
  /**
   * Formata CPF brasileiro
   */
  export const formatCPF = (cpf) => {
    if (!cpf) return '';
    
    const cleanCPF = cpf.replace(/\D/g, '');
    
    if (cleanCPF.length === 11) {
      return `${cleanCPF.slice(0, 3)}.${cleanCPF.slice(3, 6)}.${cleanCPF.slice(6, 9)}-${cleanCPF.slice(9)}`;
    }
    
    return cpf;
  };
  
  export default {
    validateRequired,
    validateEmail,
    validatePassword,
    validatePasswordConfirm,
    validateName,
    validatePhone,
    validateCPF,
    validateTerms,
    validateLoginForm,
    validateRegisterForm,
    sanitizeString,
    formatPhone,
    formatCPF,
    ERROR_MESSAGES,
    REGEX
  };