*** Settings ***
Library       RequestsLibrary
Resource      ../../../resources/keywords/mihmo_auth.robot
Variables     ../../../resources/variables/homolog.yaml

*** Test Cases ***
Obter Token Com Credenciais Validas
    [Tags]    auth    critico
    ${token}=    Autenticar No Mihmo
    Should Not Be Empty    ${token}
    Log    Token obtido com sucesso
