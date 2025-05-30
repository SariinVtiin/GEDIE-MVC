/**
 * GEDIE - Login Page JavaScript
 * Funcionalidades da página de login
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const form = document.querySelector('.login-form');
    const telegramIdInput = document.getElementById('telegram_id');
    const accessCodeInput = document.getElementById('access_code');
    const submitButton = form.querySelector('button[type="submit"]');
    const connectionStatus = document.getElementById('connectionStatus');
    
    // Inicializar
    initializeLogin();
    
    function initializeLogin() {
        setupFormValidation();
        setupInputFormatting();
        checkServerConnection();
        setupHelpLinks();
    }
    
    /**
     * Configurar validação do formulário
     */
    function setupFormValidation() {
        // Validação em tempo real com debounce
        let telegramIdTimeout;
        let accessCodeTimeout;
        
        telegramIdInput.addEventListener('input', function() {
            clearTimeout(telegramIdTimeout);
            telegramIdTimeout = setTimeout(() => {
                validateTelegramId();
            }, 300); // Aguarda 300ms após parar de digitar
        });
        
        accessCodeInput.addEventListener('input', function() {
            clearTimeout(accessCodeTimeout);
            accessCodeTimeout = setTimeout(() => {
                validateAccessCode();
            }, 300);
        });
        
        // Validação no submit
        form.addEventListener('submit', function(e) {
            // Limpar mensagens de erro anteriores
            clearAllErrors();
            
            if (!validateForm()) {
                e.preventDefault();
                showAlert('Por favor, corrija os erros no formulário', 'error');
            } else {
                showLoadingState();
            }
        });
    }
    
    /**
     * Configurar formatação dos inputs
     */
    function setupInputFormatting() {
        // Formatar Telegram ID (apenas números)
        telegramIdInput.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
        
        // Formatar código de acesso (apenas números, máximo 6 dígitos)
        accessCodeInput.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '').substring(0, 6);
        });
        
        // Auto-avançar para próximo campo
        accessCodeInput.addEventListener('input', function(e) {
            if (this.value.length === 6) {
                this.blur(); // Remove foco quando completo
            }
        });
    }
    
    /**
     * Validar ID do Telegram
     */
    function validateTelegramId() {
        const value = telegramIdInput.value.trim();
        
        // Se vazio, não mostrar erro
        if (value === '') {
            updateFieldValidation(telegramIdInput, true, '');
            return false;
        }
        
        const isValid = value.length >= 5 && /^\d+$/.test(value);
        
        if (!isValid) {
            updateFieldValidation(telegramIdInput, false, 
                'ID do Telegram deve conter apenas números (mínimo 5 dígitos)');
        } else {
            updateFieldValidation(telegramIdInput, true, '');
        }
        
        return isValid;
    }
    
    /**
     * Validar código de acesso
     */
    function validateAccessCode() {
        const value = accessCodeInput.value.trim();
        
        // Se vazio, não mostrar erro
        if (value === '') {
            updateFieldValidation(accessCodeInput, true, '');
            return false;
        }
        
        const isValid = value.length === 6 && /^\d{6}$/.test(value);
        
        if (!isValid) {
            updateFieldValidation(accessCodeInput, false, 
                'Código deve conter exatamente 6 dígitos');
        } else {
            updateFieldValidation(accessCodeInput, true, '');
        }
        
        return isValid;
    }
    
    /**
     * Validar formulário completo
     */
    function validateForm() {
        // Para validação final, campos vazios são inválidos
        const telegramValue = telegramIdInput.value.trim();
        const codeValue = accessCodeInput.value.trim();
        
        const telegramValid = telegramValue.length >= 5 && /^\d+$/.test(telegramValue);
        const codeValid = codeValue.length === 6 && /^\d{6}$/.test(codeValue);
        
        // Mostrar erros se campos estão preenchidos mas inválidos
        if (telegramValue && !telegramValid) {
            updateFieldValidation(telegramIdInput, false, 
                'ID do Telegram deve conter apenas números (mínimo 5 dígitos)');
        }
        
        if (codeValue && !codeValid) {
            updateFieldValidation(accessCodeInput, false, 
                'Código deve conter exatamente 6 dígitos');
        }
        
        return telegramValid && codeValid;
    }
    
    /**
     * Atualizar indicador visual de validação
     */
    function updateFieldValidation(field, isValid, errorMessage) {
        const formGroup = field.closest('.form-group');
        
        // Limpar erros anteriores PRIMEIRO
        clearFieldErrors(formGroup);
        
        // Remover classes de validação anteriores
        field.classList.remove('field-valid', 'field-error');
        
        // Se o campo não está vazio, aplicar validação
        if (field.value.trim() !== '') {
            if (isValid) {
                field.classList.add('field-valid');
            } else {
                field.classList.add('field-error');
                
                // Adicionar mensagem de erro apenas se não existe
                if (!formGroup.querySelector('.field-error-message')) {
                    const errorElement = document.createElement('small');
                    errorElement.className = 'field-error-message form-help';
                    errorElement.style.color = 'var(--error-color)';
                    errorElement.textContent = errorMessage;
                    formGroup.appendChild(errorElement);
                }
            }
        }
    }
    
    /**
     * Limpar erros de um campo específico
     */
    function clearFieldErrors(formGroup) {
        const existingErrors = formGroup.querySelectorAll('.field-error-message');
        existingErrors.forEach(error => error.remove());
    }
    
    /**
     * Limpar todos os erros do formulário
     */
    function clearAllErrors() {
        const allErrors = document.querySelectorAll('.field-error-message');
        allErrors.forEach(error => error.remove());
        
        // Remover classes de validação
        [telegramIdInput, accessCodeInput].forEach(input => {
            input.classList.remove('field-valid', 'field-error');
        });
    }
    
    /**
     * Verificar conexão com o servidor
     */
    function checkServerConnection() {
        updateConnectionStatus('checking', 'Verificando conexão...');
        
        fetch('/api/test-db')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateConnectionStatus('connected', 'Conectado');
                } else {
                    updateConnectionStatus('disconnected', 'Erro na conexão');
                }
            })
            .catch(error => {
                console.error('Erro ao verificar conexão:', error);
                updateConnectionStatus('disconnected', 'Sem conexão');
            });
    }
    
    /**
     * Atualizar status de conexão
     */
    function updateConnectionStatus(status, message) {
        connectionStatus.className = `connection-status ${status}`;
        connectionStatus.querySelector('span').textContent = message;
    }
    
    /**
     * Mostrar estado de carregamento
     */
    function showLoadingState() {
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Entrando...';
        
        // Reabilitar após timeout (segurança)
        setTimeout(() => {
            submitButton.disabled = false;
            submitButton.innerHTML = '<i class="fas fa-sign-in-alt"></i> Entrar';
        }, 10000);
    }
    
    /**
     * Configurar links de ajuda
     */
    function setupHelpLinks() {
        const helpLinks = document.querySelectorAll('.help-link');
        
        helpLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const text = this.textContent.trim();
                
                if (text.includes('Como obter meu ID')) {
                    showHelpModal('como-obter-id');
                } else if (text.includes('Não recebi o código')) {
                    showHelpModal('nao-recebi-codigo');
                }
            });
        });
    }
    
    /**
     * Mostrar modal de ajuda
     */
    function showHelpModal(type) {
        let title, content;
        
        switch (type) {
            case 'como-obter-id':
                title = 'Como obter meu ID do Telegram?';
                content = `
                    <ol>
                        <li>Abra o Telegram</li>
                        <li>Procure pelo bot <strong>@userinfobot</strong></li>
                        <li>Envie qualquer mensagem para o bot</li>
                        <li>O bot retornará seu ID numérico</li>
                        <li>Use esse número para fazer login</li>
                    </ol>
                `;
                break;
                
            case 'nao-recebi-codigo':
                title = 'Não recebi o código de acesso';
                content = `
                    <ol>
                        <li>Certifique-se de ter iniciado conversa com <strong>@gedie_bot</strong></li>
                        <li>Digite <code>/start</code> no chat do bot</li>
                        <li>Solicite um novo código digitando <code>/codigo</code></li>
                        <li>Aguarde alguns minutos</li>
                        <li>Se persistir, entre em contato com o suporte</li>
                    </ol>
                `;
                break;
        }
        
        showAlert(content, 'info', title);
    }
    
    /**
     * Mostrar alerta personalizado
     */
    function showAlert(message, type = 'info', title = null) {
        // Remover alertas anteriores
        const existingAlerts = document.querySelectorAll('.alert-custom');
        existingAlerts.forEach(alert => alert.remove());
        
        // Criar novo alerta
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-custom`;
        
        const icon = getAlertIcon(type);
        
        alert.innerHTML = `
            <i class="fas fa-${icon}"></i>
            <div>
                ${title ? `<strong>${title}</strong><br>` : ''}
                ${message}
            </div>
            <button class="alert-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Inserir antes do formulário
        const flashContainer = document.querySelector('.flash-messages') || 
                              document.createElement('div');
        
        if (!document.querySelector('.flash-messages')) {
            flashContainer.className = 'flash-messages';
            form.parentElement.insertBefore(flashContainer, form);
        }
        
        flashContainer.appendChild(alert);
        
        // Auto-remover após 8 segundos
        setTimeout(() => {
            if (alert.parentElement) {
                alert.remove();
            }
        }, 8000);
    }
    
    /**
     * Obter ícone para tipo de alerta
     */
    function getAlertIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    /**
     * Adicionar funcionalidade de teclado
     */
    document.addEventListener('keydown', function(e) {
        // Enter no campo Telegram ID avança para código
        if (e.key === 'Enter' && document.activeElement === telegramIdInput) {
            e.preventDefault();
            accessCodeInput.focus();
        }
        
        // Escape limpa formulário
        if (e.key === 'Escape') {
            if (confirm('Limpar formulário?')) {
                form.reset();
                document.querySelectorAll('.field-error, .field-valid').forEach(el => {
                    el.classList.remove('field-error', 'field-valid');
                });
                document.querySelectorAll('.field-error.form-help').forEach(el => {
                    el.remove();
                });
            }
        }
    });
    
    // Debug mode (apenas em desenvolvimento)
    if (window.location.hostname === 'localhost') {
        console.log('🔧 GEDIE Login - Debug Mode Ativo');
        
        // Atalho para preencher formulário de teste
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.shiftKey && e.key === 'T') {
                telegramIdInput.value = '6212796124';
                accessCodeInput.value = '123456';
                
                // Trigger validação
                setTimeout(() => {
                    validateTelegramId();
                    validateAccessCode();
                }, 100);
                
                console.log('📝 Formulário preenchido com dados de teste');
            }
        });
    }
});