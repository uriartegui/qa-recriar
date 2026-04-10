*** Settings ***
Library       ../../../resources/keywords/pericia_helper.py
Resource      ../../../resources/keywords/mihmo_auth.robot
Variables     ../../../resources/variables/homolog.yaml
Suite Setup   Inicializar Data

*** Keywords ***
Inicializar Data
    ${data}=    Gerar Data Hoje
    Set Suite Variable    ${DATA_HOJE}    ${data}

*** Variables ***
${COMPANY_PPV}      80cf1683-3f88-4941-bf57-e36e799f47bc
${FIXTURE}          ${CURDIR}/../../../resources/fixtures/atestado.png
${EMAIL_TESTE}      teste.auto@mihmo.com
${CELL_TESTE}       11999999999

${CID_GERAL}        J00
${CID_ORTOPEDIA}    M54
${CID_PSIQ}         F32

${LTS}              HealthCareLicense
${LTF}              FamilyPersonTreatmentLicense

*** Test Cases ***

# ══════════════════════════════════════════════════════════
# LTS — CID GERAL
# Regras: 1d → Clínico Geral | 15d → Clínico Geral | 30d → Clínico Geral
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_1DIA_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 14 Dias - CID Geral - Limite Antes Faixa 15
    [Tags]    setup    ppv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_14DIAS_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    14    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 15 Dias - CID Geral - Inicio Faixa 15
    [Tags]    setup    ppv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_15DIAS_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    15    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 29 Dias - CID Geral - Limite Antes Faixa 30
    [Tags]    setup    ppv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_29DIAS_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    29    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 30 Dias - CID Geral - Inicio Faixa 30
    [Tags]    setup    ppv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_30DIAS_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    30    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LTS — CID F (Psiquiatria)
# Regras: todas as faixas → Psiquiatra
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID F - Psiquiatra
    [Tags]    setup    ppv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_1DIA_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 14 Dias - CID F - Limite Antes Faixa 15
    [Tags]    setup    ppv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_14DIAS_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    14    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 15 Dias - CID F - Inicio Faixa 15
    [Tags]    setup    ppv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_15DIAS_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    15    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 29 Dias - CID F - Limite Antes Faixa 30
    [Tags]    setup    ppv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_29DIAS_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    29    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 30 Dias - CID F - Inicio Faixa 30
    [Tags]    setup    ppv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_30DIAS_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    30    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LTS — CID M,S (Ortopedia)
# Regras: todas as faixas → Ortopedista
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID M S - Ortopedista
    [Tags]    setup    ppv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_1DIA_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 14 Dias - CID M S - Limite Antes Faixa 15
    [Tags]    setup    ppv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_14DIAS_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    14    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 15 Dias - CID M S - Inicio Faixa 15
    [Tags]    setup    ppv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_15DIAS_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    15    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 29 Dias - CID M S - Limite Antes Faixa 30
    [Tags]    setup    ppv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_29DIAS_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    29    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 30 Dias - CID M S - Inicio Faixa 30
    [Tags]    setup    ppv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_30DIAS_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    30    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LTF — Licença para Tratamento de Pessoa da Família
# Regras: 1-29d → Clínico Geral | 30+d → Clínico Geral + Assistente Social
# ══════════════════════════════════════════════════════════

LTF - 1 Dia - Clinico Geral
    [Tags]    setup    ppv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTF_1DIA    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTF - 29 Dias - Limite Antes Assistente Social
    [Tags]    setup    ppv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTF_29DIAS    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    29    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTF - 30 Dias - Clinico Geral e Assistente Social
    [Tags]    setup    ppv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTF_30DIAS    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    30    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}
