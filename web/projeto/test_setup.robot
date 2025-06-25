*** Settings ***
Documentation    Script de setup e debug para testes do GEDIE
Library          SeleniumLibrary
Library          RequestsLibrary
Library          Collections

*** Variables ***
${BASE_URL}          http://localhost:5000
${API_URL}           ${BASE_URL}/api
${BROWSER}           Chrome
${HEADLESS}          False

*** Test Cases ***
Verificar Servidor Rodando
    [Documentation]    Verifica se o servidor Flask está rodando
    Create Session    gedie    ${BASE_URL}
    ${response}=    GET On Session    gedie    /login    expected_status=200
    Log    Servidor respondendo corretamente
    
Verificar Conexão Com Banco
    [Documentation]    Verifica se a aplicação conecta ao banco
    Create Session    gedie    ${API_URL}
    ${response}=    GET On Session    gedie    /test-db    expected_status=200
    ${json}=    Set Variable    ${response.json()}
    Should Be Equal    ${json['status']}    success
    Log    Conexão com banco OK: ${json['message']}

Verificar Usuário de Teste
    [Documentation]    Verifica se usuário de teste existe no banco
    Open Browser    ${BASE_URL}/login    ${BROWSER}
    Maximize Browser Window
    
    # Tentar fazer login
    Input Text    id=telegram_id    6212796124
    Input Text    id=access_code    123456
    Click Button    css=button[type="submit"]
    
    # Verificar resultado
    ${login_success}=    Run Keyword And Return Status    
    ...    Wait Until Location Is    ${BASE_URL}/dashboard    timeout=5s
    
    IF    ${login_success}
        Log    Usuário de teste existe e está ativo
        # Verificar categorias
        Click Element    css=.feature-card:first-child
        Wait Until Element Is Visible    id=expenseModal    timeout=5s
        Sleep    2s
        ${options}=    Get Element Count    css=#categorySelect option
        Log    Número de categorias disponíveis: ${options}
        
        IF    ${options} <= 1
            Log    AVISO: Usuário não tem categorias cadastradas    level=WARN
        END
        
        Click Element    css=.btn-cancel
    ELSE
        Log    ERRO: Usuário de teste não existe ou credenciais incorretas    level=ERROR
        ${error_msg}=    Get Text    css=.alert-error
        Log    Mensagem de erro: ${error_msg}
    END
    
    Close Browser

Debug JavaScript Console
    [Documentation]    Captura erros do console JavaScript
    Open Browser    ${BASE_URL}/login    ${BROWSER}
    
    # Habilitar captura de logs do console
    ${logs}=    Get Browser Logs    browser
    Log    Console logs: ${logs}
    
    # Fazer login para verificar erros no dashboard
    Input Text    id=telegram_id    6212796124
    Input Text    id=access_code    123456
    Click Button    css=button[type="submit"]
    
    ${on_dashboard}=    Run Keyword And Return Status    
    ...    Wait Until Location Is    ${BASE_URL}/dashboard    timeout=5s
    
    IF    ${on_dashboard}
        Sleep    3s
        ${dashboard_logs}=    Get Browser Logs    browser
        Log    Dashboard console logs: ${dashboard_logs}
        
        # Testar abertura do modal
        Click Element    css=.feature-card:first-child
        Sleep    2s
        ${modal_logs}=    Get Browser Logs    browser
        Log    Modal console logs: ${modal_logs}
    END
    
    Close Browser

Criar Dados de Teste Via API
    [Documentation]    Tenta criar dados de teste diretamente via API
    [Tags]    setup
    
    # Esta keyword precisaria de um endpoint API específico
    # ou acesso direto ao banco de dados
    Log    Para criar dados de teste, execute o script SQL fornecido

*** Keywords ***
Get Browser Logs
    [Arguments]    ${log_type}=browser
    [Documentation]    Captura logs do navegador (Chrome only)
    ${logs}=    Execute Javascript    
    ...    return window.performance.getEntriesByType("resource").map(e => ({name: e.name, duration: e.duration}))
    RETURN    ${logs}