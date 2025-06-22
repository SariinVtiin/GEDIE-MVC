*** Settings ***
Documentation     Geração e visualização de código de acesso
Resource          ../../resources/variables.robot
Resource          ../../resources/keywords/telegram.robot
Test Setup        Dado que inicio a sessão com o bot
Test Teardown     Encerro a sessão

*** Test Cases ***
Gerar Código de Acesso
    E envio o comando    /start
    Quando eu clico no botão    Configurações
    Quando eu clico no botão    Ver Código Atual
    Então o bot deve responder com mensagem contendo    Seu Código de Acesso Atual
