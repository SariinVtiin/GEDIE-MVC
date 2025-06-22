*** Settings ***
Library    ../../libs/TelegramLibrary.py

*** Keywords ***
# ---------- Sessão ----------
Dado que inicio a sessão com o bot
    Open Connection

Encerro a sessão
    Close Connection

Close All Connections
    Close Connection

# ---------- Ações ----------
E envio o comando
    [Arguments]    ${command}
    Send Command    ${command}

Quando eu clico no botão
    [Arguments]    ${button_text}
    Click Button    ${button_text}

Então o bot deve responder com mensagem contendo
    [Arguments]    ${expected}
    Wait For Reply Containing    ${expected}    ${TIMEOUT}

