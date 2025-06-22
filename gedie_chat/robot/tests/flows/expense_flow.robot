*** Settings ***
Documentation     Fluxos de registro de gasto (com e sem descrição)
Resource          ../../resources/variables.robot
Resource          ../../resources/keywords/telegram.robot
Test Setup        Dado que inicio a sessão com o bot
Test Teardown     Encerro a sessão

*** Variables ***
${VALOR_GASTO}       25
${CATEGORIA_BTN}     Alimentação
${DESCRICAO}         almoço

*** Test Cases ***
Registrar Gasto - Sem Descrição
    E envio o comando    /start
    Quando eu clico no botão    Registrar Gasto
    Quando eu clico no botão    ${CATEGORIA_BTN}
    Então o bot deve responder com mensagem contendo    Valor do gasto
    E envio o comando    ${VALOR_GASTO}
    Então o bot deve responder com mensagem contendo    confirmar gasto
    Quando eu clico no botão    Confirmar Sem Descrição
    Então o bot deve responder com mensagem contendo    gasto registrado com sucesso

Registrar Gasto - Com Descrição
    E envio o comando    /start
    Quando eu clico no botão    Registrar Gasto
    Quando eu clico no botão    ${CATEGORIA_BTN}
    Então o bot deve responder com mensagem contendo    valor do gasto
    E envio o comando    ${VALOR_GASTO}
    Então o bot deve responder com mensagem contendo    confirmar gasto
    Quando eu clico no botão    Adicionar Descrição
    Então o bot deve responder com mensagem contendo    descrição do gasto
    E envio o comando    ${DESCRICAO}
    Então o bot deve responder com mensagem contendo    gasto registrado com sucesso
    Então o bot deve responder com mensagem contendo    ${DESCRICAO}
