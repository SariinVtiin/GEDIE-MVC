*** Settings ***
Documentation     Smoke: Exibe o ID de Telegram do usuário
Resource          ../../resources/variables.robot
Resource          ../../resources/keywords/telegram.robot
Test Setup        Dado que inicio a sessão com o bot
Test Teardown     Encerro a sessão

*** Test Cases ***
Ver Meu ID
    E envio o comando    /start
    Quando eu clico no botão    Meu ID
    Então o bot deve responder com mensagem contendo    Seu ID do Telegram