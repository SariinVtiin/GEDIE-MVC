*** Settings ***
Documentation     Fluxos de envio de comprovante + confirmação e cancelamento
Resource          ../../resources/variables.robot
Resource          ../../resources/keywords/telegram.robot
Test Setup        Dado que inicio a sessão com o bot
Test Teardown     Encerro a sessão

*** Keywords ***
# reutilizamos o helper já existente na Library
Gerar E Enviar Comprovante
    ${img}=    Evaluate    TelegramLibrary.generate_fake_receipt()    modules=TelegramLibrary
    Send Image    ${img}

*** Test Cases ***
Enviar Comprovante — Confirmar
    E envio o comando    /start
    Quando eu clico no botão    Enviar Comprovante
    Gerar E Enviar Comprovante
    # o bot agora mostra botões Confirmar / Cancelar
    Quando eu clico no botão    Confirmar
    Então o bot deve responder com mensagem contendo    Gasto registrado por foto!

Enviar Comprovante — Cancelar
    E envio o comando    /start
    Quando eu clico no botão    Enviar Comprovante
    Gerar E Enviar Comprovante
    Quando eu clico no botão    Cancelar
    Então o bot deve responder com mensagem contendo    Análise cancelada