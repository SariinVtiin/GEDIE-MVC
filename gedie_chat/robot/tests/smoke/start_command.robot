*** Settings ***
Documentation     Smoke: Valida mensagem de boas‑vindas do comando /start
Resource          ../../resources/variables.robot
Resource          ../../resources/keywords/telegram.robot
Test Setup        Dado que inicio a sessão com o bot
Test Teardown     Encerro a sessão
Suite Teardown    Close All Connections

*** Test Cases ***
CT01 - Boas‑Vindas
    E envio o comando    /start
    Então o bot deve responder com mensagem contendo    Bem-vindo ao GEDIE
