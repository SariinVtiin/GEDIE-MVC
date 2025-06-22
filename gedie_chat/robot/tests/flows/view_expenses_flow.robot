*** Settings ***
Documentation     Fluxos de visualização de gastos (Hoje e Este Mês)
Resource          ../../resources/variables.robot
Resource          ../../resources/keywords/telegram.robot
Test Setup        Dado que inicio a sessão com o bot
Test Teardown     Encerro a sessão

*** Test Cases ***
Ver Gastos de Hoje
    E envio o comando    /start
    Quando eu clico no botão    Ver Gastos
    Então o bot deve responder com mensagem contendo    escolha o período
    Quando eu clico no botão    Hoje
    Então o bot deve responder com mensagem contendo    Gastos de Hoje
    Então o bot deve responder com mensagem contendo    Total: R$

Ver Gastos deste Mês
    E envio o comando    /start
    Quando eu clico no botão    Ver Gastos
    Então o bot deve responder com mensagem contendo    escolha o período
    Quando eu clico no botão    Este Mês
    Então o bot deve responder com mensagem contendo    Gastos deste Mês
    Então o bot deve responder com mensagem contendo    Total: R$
