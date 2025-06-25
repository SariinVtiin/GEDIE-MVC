*** Settings ***
Documentation    Debug detalhado do processo de adicionar despesa
Library          SeleniumLibrary
Library          DateTime
Library          RequestsLibrary
Library          Collections

*** Variables ***
${BASE_URL}              http://localhost:5000
${BROWSER}               Chrome
${VALID_TELEGRAM_ID}     6212796124
${VALID_ACCESS_CODE}     123456

*** Test Cases ***
Test Complete Add Expense Flow
    [Documentation]    Teste completo com verificação de cada etapa
    
    # 1. Setup e Login
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    0.5
    Go To    ${BASE_URL}/login
    
    Log    === ETAPA 1: LOGIN ===
    Input Text    id=telegram_id    ${VALID_TELEGRAM_ID}
    Input Text    id=access_code    ${VALID_ACCESS_CODE}
    Click Button    css=button[type="submit"]
    Wait Until Location Is    ${BASE_URL}/dashboard    timeout=10s
    Log    Login realizado com sucesso
    
    # 2. Verificar Dashboard
    Log    === ETAPA 2: VERIFICAR DASHBOARD ===
    Element Should Be Visible    css=.expenses-table
    ${initial_rows}=    Get Element Count    css=.expenses-table tbody tr
    Log    Número inicial de despesas: ${initial_rows}
    
    # 3. Verificar se há mensagem de "nenhuma despesa"
    ${no_expense_msg}=    Run Keyword And Return Status    Page Should Contain    Nenhuma despesa registrada
    Log    Mensagem 'Nenhuma despesa' visível: ${no_expense_msg}
    
    # 4. Abrir Modal
    Log    === ETAPA 3: ABRIR MODAL ===
    
    # Verificar se botão existe e está visível
    Element Should Be Visible    css=.feature-card:first-child
    ${btn_text}=    Get Text    css=.feature-card:first-child
    Log    Texto do botão: ${btn_text}
    
    # Tentar clicar
    Execute Javascript    window.scrollTo(0, 0);
    Sleep    1s
    Click Element    css=.feature-card:first-child
    
    # Verificar se modal abriu
    ${modal_opened}=    Run Keyword And Return Status    
    ...    Wait Until Element Is Visible    id=expenseModal    timeout=5s
    
    IF    not ${modal_opened}
        Log    Modal não abriu com clique normal, tentando JavaScript
        Execute Javascript    loadCategories(); openModal();
        Sleep    2s
    END
    
    Element Should Be Visible    id=expenseModal
    Log    Modal aberto com sucesso
    
    # 5. Verificar Categorias
    Log    === ETAPA 4: VERIFICAR CATEGORIAS ===
    Wait Until Element Is Visible    id=categorySelect    timeout=5s
    
    ${cat_count}=    Get Element Count    css=#categorySelect option
    Log    Número de categorias no select: ${cat_count}
    
    ${categories}=    Get List Items    id=categorySelect
    Log    Categorias disponíveis: ${categories}
    
    IF    ${cat_count} <= 1
        Log    ERRO: Nenhuma categoria carregada!    level=ERROR
        
        # Tentar debug da API
        ${api_test}=    Execute Javascript    
        ...    return fetch('/api/categories')
        ...        .then(r => r.json())
        ...        .then(d => JSON.stringify(d))
        ...        .catch(e => 'ERRO: ' + e.toString());
        Log    Resposta da API categories: ${api_test}
    END
    
    # 6. Preencher Formulário
    Log    === ETAPA 5: PREENCHER FORMULÁRIO ===
    ${timestamp}=    Get Current Date    result_format=%H%M%S
    ${test_desc}=    Set Variable    Teste Debug ${timestamp}
    ${test_value}=    Set Variable    25.50
    ${today}=    Get Current Date    result_format=%Y-%m-%d
    
    Input Text    name=valor    ${test_value}
    Log    Valor inserido: ${test_value}
    
    Input Text    name=descricao    ${test_desc}
    Log    Descrição inserida: ${test_desc}
    
    Input Text    name=data_gasto    ${today}
    Log    Data inserida: ${today}
    
    # Selecionar categoria se houver
    IF    ${cat_count} > 1
        Select From List By Index    id=categorySelect    1
        ${selected_cat}=    Get Selected List Label    id=categorySelect
        Log    Categoria selecionada: ${selected_cat}
    ELSE
        Log    AVISO: Não foi possível selecionar categoria    level=WARN
    END
    
    # 7. Salvar
    Log    === ETAPA 6: SALVAR DESPESA ===
    
    # Verificar se botão está habilitado
    ${btn_enabled}=    Run Keyword And Return Status    
    ...    Element Should Be Enabled    css=#expenseModal .btn-primary
    Log    Botão salvar habilitado: ${btn_enabled}
    
    # Capturar screenshot antes de salvar
    Capture Page Screenshot    before_save.png
    
    # Tentar salvar
    Click Button    css=#expenseModal .btn-primary
    Log    Botão salvar clicado
    
    # 8. Verificar Resultado
    Log    === ETAPA 7: VERIFICAR RESULTADO ===
    Sleep    5s    # Aguardar processamento
    
    ${modal_closed}=    Run Keyword And Return Status    
    ...    Element Should Not Be Visible    id=expenseModal
    Log    Modal fechou: ${modal_closed}
    
    IF    not ${modal_closed}
        Log    Modal ainda aberto - verificando erros
        
        # Capturar screenshot
        Capture Page Screenshot    modal_still_open.png
        
        # Verificar se há mensagem de erro
        ${error_msg}=    Run Keyword And Return Status    Page Should Contain    erro
        Log    Mensagem de erro visível: ${error_msg}
        
        # Tentar fechar modal
        ${close_btn}=    Run Keyword And Return Status    
        ...    Click Element    css=.btn-cancel
        IF    not ${close_btn}
            Execute Javascript    closeModal();
        END
    END
    
    # 9. Verificar Tabela
    Log    === ETAPA 8: VERIFICAR TABELA ===
    
    # Recarregar página
    Reload Page
    Wait Until Element Is Visible    css=.expenses-table    timeout=10s
    
    ${final_rows}=    Get Element Count    css=.expenses-table tbody tr
    Log    Número final de despesas: ${final_rows}
    
    ${expense_added}=    Evaluate    ${final_rows} > ${initial_rows}
    Log    Despesa foi adicionada: ${expense_added}
    
    # Procurar pela despesa específica
    ${expense_found}=    Run Keyword And Return Status    
    ...    Page Should Contain    ${test_desc}
    Log    Despesa específica encontrada: ${expense_found}
    
    # Se não encontrou, listar todas as despesas
    IF    not ${expense_found}
        Log    === LISTANDO TODAS AS DESPESAS ===
        FOR    ${i}    IN RANGE    1    ${final_rows}+1
            ${row_text}=    Get Text    css=.expenses-table tbody tr:nth-child(${i})
            Log    Linha ${i}: ${row_text}
        END
    END
    
    # 10. Verificar Console JavaScript
    Log    === ETAPA 9: VERIFICAR CONSOLE JAVASCRIPT ===
    ${js_errors}=    Execute Javascript    
    ...    return window.console.logs || 'Sem logs capturados';
    Log    Console logs: ${js_errors}
    
    [Teardown]    Close Browser

Test API Directly
    [Documentation]    Testa a API de adicionar despesa diretamente
    
    # Criar sessão
    Create Session    gedie    ${BASE_URL}
    
    # 1. Fazer login para obter cookie de sessão
    ${login_data}=    Create Dictionary    
    ...    telegram_id=${VALID_TELEGRAM_ID}    
    ...    access_code=${VALID_ACCESS_CODE}
    
    ${login_resp}=    POST On Session    gedie    /login    
    ...    data=${login_data}    
    ...    expected_status=ANY
    
    Log    Login status: ${login_resp.status_code}
    
    # 2. Extrair cookies
    ${cookies}=    Set Variable    ${login_resp.cookies}
    
    # 3. Testar API de categorias
    ${cat_resp}=    GET On Session    gedie    /api/categories    
    ...    cookies=${cookies}    
    ...    expected_status=ANY
    
    Log    Categories API status: ${cat_resp.status_code}
    Log    Categories API response: ${cat_resp.text}
    
    # 4. Testar adicionar despesa via POST
    ${timestamp}=    Get Current Date    result_format=%H%M%S
    ${today}=    Get Current Date    result_format=%Y-%m-%d
    
    ${expense_data}=    Create Dictionary    
    ...    valor=30.00
    ...    descricao=Teste API ${timestamp}
    ...    data_gasto=${today}
    ...    category_id=1
    
    ${add_resp}=    POST On Session    gedie    /add-expense    
    ...    data=${expense_data}    
    ...    cookies=${cookies}    
    ...    expected_status=ANY
    
    Log    Add expense status: ${add_resp.status_code}
    Log    Add expense response: ${add_resp.text}

Verify Server Logs
    [Documentation]    Instruções para verificar logs do servidor
    
    Log    === VERIFICAR LOGS DO SERVIDOR ===
    Log    1. No terminal onde o Flask está rodando, verifique se há erros
    Log    2. Procure por mensagens como:
    Log    - 500 Internal Server Error
    Log    - KeyError ou AttributeError
    Log    - Problemas de conexão com banco
    Log    3. Se houver erros, eles indicarão o problema real