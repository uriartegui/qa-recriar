*** Settings ***
Library    Browser

*** Variables ***
${INPUT_EMAIL}      input[name="username"]
${INPUT_SENHA}      input[name="password"]
${BTN_ENTRAR}       po-button button

*** Keywords ***
Abrir Login
    [Arguments]    ${url}
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page       ${url}

Preencher Login
    [Arguments]    ${email}    ${senha}
    Fill Text    ${INPUT_EMAIL}    ${email}
    Fill Text    ${INPUT_SENHA}    ${senha}

Clicar Entrar
    Click    ${BTN_ENTRAR}

Fazer Login
    [Arguments]    ${url}    ${email}    ${senha}
    Abrir Login       ${url}
    Preencher Login   ${email}    ${senha}
    Clicar Entrar
