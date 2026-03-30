*** Settings ***
Library           Browser
Resource          ../../../resources/pages/login_page.robot
Variables         ../../../resources/variables/homolog.yaml

*** Variables ***
${EMAIL_VALIDO}     adm.castela@mihmo.com.br
${SENHA_VALIDA}     REMOVIDO
${MSG_ERRO}         Usuário não encontrado. Verifique o email ou cadastre-se.

*** Test Cases ***
Login Com Credenciais Validas
    Fazer Login    ${BASE_URL}    ${EMAIL_VALIDO}    ${SENHA_VALIDA}
    Wait For Navigation    url=**/home    timeout=10s
    Get Url         ==    ${BASE_URL}/home

Login Com Email Invalido
    Abrir Login     ${BASE_URL}
    Preencher Login    invalido@teste.com    ${SENHA_VALIDA}
    Clicar Entrar
    Get Text        .po-toaster-message    ==    ${MSG_ERRO}

Login Com Campos Em Branco
    Abrir Login     ${BASE_URL}
    Clicar Entrar
    Get Text        css=.po-toaster-message >> nth=0    contains    Verifique os campos requeridos
