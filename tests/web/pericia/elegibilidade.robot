*** Settings ***
Library           Browser
Resource          ../../../resources/pages/login_page.robot
Resource          ../../../resources/pages/pericia_page.robot
Variables         ../../../resources/variables/homolog.yaml

*** Variables ***
${MIHMADO_COM_INSS}     Victória Teste miHrmo
${MIHMADO_SEM_INSS}     Teste Porto Velho
${DATA_TESTE}           01/04/2026

*** Test Cases ***

# ─── COM INSS ───────────────────────────────────────────

LTS INSS - 1 dia - Deve ser Elegivel
    [Tags]    com_inss    lts    critico
    Fazer Login              ${BASE_URL}    ${EMAIL_VALIDO}    ${SENHA_VALIDA}
    Wait For Navigation      url=**/home    timeout=10s
    Navegar Para Nova Pericia    ${BASE_URL}
    Preencher Formulario Pericia
    ...    ${MIHMADO_COM_INSS}
    ...    Licença para Tratamento de Saúde (LTS) - INSS
    ...    ${DATA_TESTE}
    ...    1
    Pericia Cadastrada Com Sucesso

LTS - 1 a 3 dias - Medico do Trabalho
    [Tags]    com_inss    lts    critico
    Fazer Login              ${BASE_URL}    ${EMAIL_VALIDO}    ${SENHA_VALIDA}
    Wait For Navigation      url=**/home    timeout=10s
    Navegar Para Nova Pericia    ${BASE_URL}
    Preencher Formulario Pericia
    ...    ${MIHMADO_COM_INSS}
    ...    Licença para Tratamento de Saúde (LTS)
    ...    ${DATA_TESTE}
    ...    2
    Pericia Cadastrada Com Sucesso

LTS - 4 a 14 dias - Clinico Geral
    [Tags]    com_inss    lts
    Fazer Login              ${BASE_URL}    ${EMAIL_VALIDO}    ${SENHA_VALIDA}
    Wait For Navigation      url=**/home    timeout=10s
    Navegar Para Nova Pericia    ${BASE_URL}
    Preencher Formulario Pericia
    ...    ${MIHMADO_COM_INSS}
    ...    Licença para Tratamento de Saúde (LTS)
    ...    ${DATA_TESTE}
    ...    10
    Pericia Cadastrada Com Sucesso

LTS - 60 dias ou mais - Junta Medica
    [Tags]    com_inss    lts    junta
    Fazer Login              ${BASE_URL}    ${EMAIL_VALIDO}    ${SENHA_VALIDA}
    Wait For Navigation      url=**/home    timeout=10s
    Navegar Para Nova Pericia    ${BASE_URL}
    Preencher Formulario Pericia
    ...    ${MIHMADO_COM_INSS}
    ...    Licença para Tratamento de Saúde (LTS)
    ...    ${DATA_TESTE}
    ...    60
    Pericia Cadastrada Com Sucesso

# ─── SEM INSS ───────────────────────────────────────────

LTS - 1 dia - Sem INSS - Deve ser Elegivel
    [Tags]    sem_inss    lts    critico
    Fazer Login              ${BASE_URL}    ${EMAIL_VALIDO}    ${SENHA_VALIDA}
    Wait For Navigation      url=**/home    timeout=10s
    Navegar Para Nova Pericia    ${BASE_URL}
    Preencher Formulario Pericia
    ...    ${MIHMADO_SEM_INSS}
    ...    Licença para Tratamento de Saúde (LTS)
    ...    ${DATA_TESTE}
    ...    1
    Pericia Cadastrada Com Sucesso

LTS - 15 dias - Sem INSS - Deve ser Elegivel
    [Tags]    sem_inss    lts
    Fazer Login              ${BASE_URL}    ${EMAIL_VALIDO}    ${SENHA_VALIDA}
    Wait For Navigation      url=**/home    timeout=10s
    Navegar Para Nova Pericia    ${BASE_URL}
    Preencher Formulario Pericia
    ...    ${MIHMADO_SEM_INSS}
    ...    Licença para Tratamento de Saúde (LTS)
    ...    ${DATA_TESTE}
    ...    15
    Pericia Cadastrada Com Sucesso

# ─── VALIDAÇÕES ─────────────────────────────────────────

Salvar Sem Preencher Campos - Deve Dar Erro
    [Tags]    validacao
    Fazer Login              ${BASE_URL}    ${EMAIL_VALIDO}    ${SENHA_VALIDA}
    Wait For Navigation      url=**/home    timeout=10s
    Navegar Para Nova Pericia    ${BASE_URL}
    Salvar Pericia
    Get Text    css=.po-toaster-message >> nth=0    contains    requeridos
