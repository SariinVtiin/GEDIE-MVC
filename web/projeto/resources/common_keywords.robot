*** Settings ***
Documentation    Keywords comuns reutilizáveis para os testes do GEDIE
Library          SeleniumLibrary
Library          DateTime
Library          String

*** Variables ***
# Reutilizando variáveis do arquivo principal
# Estas devem ser importadas do arquivo principal de testes

*** Keywords ***
Take Screenshot On Failure
    [Documentation]    Captura screenshot quando um teste falha
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${screenshot_name}=    Set Variable    screenshot_${TEST_NAME}_${timestamp}.png
    Capture Page Screenshot    ${screenshot_name}
    Log    Screenshot salvo: ${screenshot_name}    level=WARN

Wait For Ajax
    [Documentation]    Aguarda requisições AJAX serem completadas
    Sleep    0.5s
    Execute Javascript    return jQuery.active == 0
    Sleep    0.5s

Scroll To Element
    [Arguments]    ${locator}
    [Documentation]    Rola a página até o elemento especificado
    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    Scroll Element Into View    ${locator}
    Sleep    0.5s

Format Currency
    [Arguments]    ${value}
    [Documentation]    Formata valor para moeda brasileira
    ${formatted}=    Set Variable    R$ ${value}
    RETURN    ${formatted}

Get Random String
    [Arguments]    ${length}=8
    [Documentation]    Gera string aleatória
    ${chars}=    Set Variable    ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
    ${random_string}=    Generate Random String    ${length}    ${chars}
    RETURN    ${random_string}

Get Today Date
    [Documentation]    Retorna a data de hoje no formato YYYY-MM-DD
    ${today}=    Get Current Date    result_format=%Y-%m-%d
    RETURN    ${today}

Get Yesterday Date
    [Documentation]    Retorna a data de ontem no formato YYYY-MM-DD
    ${yesterday}=    Get Current Date    increment=-1 day    result_format=%Y-%m-%d
    RETURN    ${yesterday}

Verify Element Text
    [Arguments]    ${locator}    ${expected_text}
    [Documentation]    Verifica se o elemento contém o texto esperado
    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    Element Should Contain    ${locator}    ${expected_text}

Click Element With Retry
    [Arguments]    ${locator}    ${retries}=3
    [Documentation]    Clica em um elemento com retry em caso de falha
    FOR    ${i}    IN RANGE    ${retries}
        ${status}=    Run Keyword And Return Status    Click Element    ${locator}
        IF    ${status}
            RETURN
        END
        Sleep    1s
    END
    Fail    Não foi possível clicar no elemento ${locator} após ${retries} tentativas

Input Text With Clear
    [Arguments]    ${locator}    ${text}
    [Documentation]    Limpa o campo antes de inserir texto
    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    Clear Element Text    ${locator}
    Input Text    ${locator}    ${text}

Select Random Option From Dropdown
    [Arguments]    ${locator}
    [Documentation]    Seleciona uma opção aleatória de um dropdown
    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    ${options}=    Get List Items    ${locator}
    ${count}=    Get Length    ${options}
    ${random_index}=    Evaluate    random.randint(1, ${count}-1)    modules=random
    Select From List By Index    ${locator}    ${random_index}

Wait For Modal To Open
    [Arguments]    ${modal_locator}
    [Documentation]    Aguarda um modal abrir completamente
    Wait Until Element Is Visible    ${modal_locator}    timeout=${TIMEOUT}
    Wait Until Element Is Enabled    ${modal_locator}    timeout=${TIMEOUT}
    Sleep    0.5s    # Aguarda animação

Wait For Modal To Close
    [Arguments]    ${modal_locator}
    [Documentation]    Aguarda um modal fechar completamente
    Wait Until Element Is Not Visible    ${modal_locator}    timeout=${TIMEOUT}
    Sleep    0.5s    # Aguarda animação

Check Connection Status
    [Documentation]    Verifica o status de conexão da aplicação
    ${status}=    Get Element Attribute    ${CONNECTION_STATUS}    class
    Should Contain    ${status}    connected

Wait For Page Load Complete
    [Documentation]    Aguarda a página carregar completamente
    Wait For Condition    return document.readyState == "complete"    timeout=${TIMEOUT}
    Sleep    0.5s

Get Table Row Count
    [Arguments]    ${table_locator}
    [Documentation]    Retorna o número de linhas em uma tabela
    Wait Until Element Is Visible    ${table_locator}    timeout=${TIMEOUT}
    ${rows}=    Get Element Count    ${table_locator} tbody tr
    RETURN    ${rows}

Verify Toast Message
    [Arguments]    ${message}    ${type}=success
    [Documentation]    Verifica mensagem toast/popup
    ${toast_locator}=    Set Variable If    
    ...    '${type}' == 'success'    css=.toast-success
    ...    '${type}' == 'error'    css=.toast-error
    ...    css=.toast-info
    Wait Until Element Is Visible    ${toast_locator}    timeout=${TIMEOUT}
    Element Should Contain    ${toast_locator}    ${message}

Execute Javascript Function
    [Arguments]    ${function_name}    @{args}
    [Documentation]    Executa uma função JavaScript com argumentos
    ${js_args}=    Catenate    SEPARATOR=,    @{args}
    ${result}=    Execute Javascript    return ${function_name}(${js_args})
    RETURN    ${result}

Mobile View Setup
    [Documentation]    Configura visualização mobile
    Set Window Size    375    812
    Sleep    1s

Desktop View Setup
    [Documentation]    Configura visualização desktop
    Maximize Browser Window
    Sleep    1s

Verify Responsive Design
    [Arguments]    ${element}
    [Documentation]    Verifica se elemento é responsivo
    Desktop View Setup
    Element Should Be Visible    ${element}
    Mobile View Setup
    Element Should Be Visible    ${element}
    Desktop View Setup

Generate Test Data
    [Arguments]    ${prefix}=Test
    [Documentation]    Gera dados de teste únicos
    ${timestamp}=    Get Current Date    result_format=%Y%m%d%H%M%S
    ${random}=    Get Random String    4
    ${unique_id}=    Set Variable    ${prefix}_${timestamp}_${random}
    RETURN    ${unique_id}

Clean Test Data
    [Arguments]    ${identifier}
    [Documentation]    Limpa dados de teste (placeholder para implementação futura)
    Log    Limpando dados de teste com identificador: ${identifier}
    # Implementar limpeza via API ou banco de dados

Verify API Response
    [Arguments]    ${endpoint}    ${expected_status}=200
    [Documentation]    Verifica resposta de API (placeholder para implementação futura)
    Log    Verificando endpoint: ${endpoint}
    # Implementar verificação de API

Set Test Environment
    [Arguments]    ${env}=test
    [Documentation]    Configura ambiente de teste
    Set Global Variable    ${ENVIRONMENT}    ${env}
    Log    Ambiente de teste configurado para: ${env}

Log Test Info
    [Documentation]    Registra informações do teste
    ${test_info}=    Create Dictionary
    ...    name=${TEST_NAME}
    ...    tags=${TEST_TAGS}
    ...    timestamp=${TEST_START_TIME}
    Log    Informações do teste: ${test_info}    level=INFO