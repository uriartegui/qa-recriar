*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${FIREBASE_URL}     https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword
${FIREBASE_KEY}     REMOVIDO

*** Keywords ***
Autenticar No Mihmo
    ${body}=    Create Dictionary
    ...    email=${EMAIL_VALIDO}
    ...    password=${SENHA_VALIDA}
    ...    returnSecureToken=${TRUE}
    ${response}=    POST    ${FIREBASE_URL}
    ...    params=key=${FIREBASE_KEY}
    ...    json=${body}
    ...    expected_status=200
    ${token}=    Get From Dictionary    ${response.json()}    idToken
    RETURN    ${token}

Obter Headers Autenticados
    ${token}=    Autenticar No Mihmo
    ${headers}=    Create Dictionary
    ...    Authorization=Bearer ${token}
    ...    Content-Type=application/json
    RETURN    ${headers}
