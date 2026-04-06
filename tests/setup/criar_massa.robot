*** Settings ***
Library       ../../resources/keywords/pericia_helper.py
Resource      ../../resources/keywords/mihmo_auth.robot
Variables     ../../resources/variables/homolog.yaml
Suite Setup   Inicializar Data

*** Keywords ***
Inicializar Data
    ${data}=    Gerar Data Hoje
    Set Suite Variable    ${DATA_HOJE}    ${data}

*** Variables ***
${COMPANY_PMV}      32e94042-51d1-4270-a5ea-88b9915f22d4
${FIXTURE}          ${CURDIR}/../../resources/fixtures/atestado.png
${EMAIL_TESTE}      teste.auto@mihmo.com
${CELL_TESTE}       11999999999

${CID_GERAL}        J00
${CID_ORTOPEDIA}    M54
${CID_PSIQ}         F32

${LTS}              HealthCareLicense
${LTS_INSS}         HealthCareLicenseInss
${LTF}              FamilyPersonTreatmentLicense
${CONSULTA}         MedicalConsultation
${GESTACAO}         PregnancyLicense
${RESTRICAO}        RestrictedActivity
${ADMISSIONAL}      Admission
${ACIDENTE}         FirstWorkAccidentAttendance
${PROCESSOS_ADM}    AdministrativeProcesses

*** Test Cases ***

# ══════════════════════════════════════════════════════════
# LTS — CID GERAL (vazio)
# Regras: 1-3d → Médico Trabalho | 4-14d → Clínico Geral
#         15-59d → Clínico Geral  | 60+d → Junta/Clínico Geral
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID Geral - Medico Trabalho
    [Tags]    setup    pmv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_1DIA_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 3 Dias - CID Geral - Limite Medico Trabalho
    [Tags]    setup    pmv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_3DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    3    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 4 Dias - CID Geral - Inicio Clinico Geral
    [Tags]    setup    pmv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_4DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    4    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 14 Dias - CID Geral - Limite Faixa 4-14
    [Tags]    setup    pmv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_14DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    14    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 15 Dias - CID Geral - Inicio Faixa 15-59
    [Tags]    setup    pmv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_15DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    15    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 59 Dias - CID Geral - Limite Antes Junta
    [Tags]    setup    pmv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_59DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    59    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 61 Dias - CID Geral - Junta Medica Clinico Geral
    [Tags]    setup    pmv    lts    lts_geral    borda    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_60DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    61    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LTS — CID F (Psiquiatria)
# Regras: 4-29d → Clínico Geral | 30-59d → Clínico Geral
#         60+d → Junta/Psiquiatra+Clínico Geral
# ══════════════════════════════════════════════════════════

LTS - 4 Dias - CID F - Inicio Clinico Geral
    [Tags]    setup    pmv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_4DIAS_PSIQ    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    4    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 29 Dias - CID F - Limite Faixa 4-30
    [Tags]    setup    pmv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_29DIAS_PSIQ    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    29    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 30 Dias - CID F - Inicio Faixa 30-59
    [Tags]    setup    pmv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_30DIAS_PSIQ    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    30    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 59 Dias - CID F - Limite Antes Junta
    [Tags]    setup    pmv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_59DIAS_PSIQ    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    59    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 61 Dias - CID F - Junta Medica Psiquiatra e Clinico Geral
    [Tags]    setup    pmv    lts    lts_psiquiatria    borda    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_60DIAS_PSIQ    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    61    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LTS — CID M e S (Ortopedia)
# Regras: 4-14d → Clínico Geral | 15-59d → Ortopedista
#         60+d → Junta/Ortopedista+Clínico Geral
# ══════════════════════════════════════════════════════════

LTS - 4 Dias - CID M S - Inicio Clinico Geral
    [Tags]    setup    pmv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_4DIAS_ORTOP    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    4    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 14 Dias - CID M S - Limite Faixa 4-14 Clinico Geral
    [Tags]    setup    pmv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_14DIAS_ORTOP    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    14    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 15 Dias - CID M S - Inicio Ortopedista
    [Tags]    setup    pmv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_15DIAS_ORTOP    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    15    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 59 Dias - CID M S - Limite Antes Junta Ortopedista
    [Tags]    setup    pmv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_59DIAS_ORTOP    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    59    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 61 Dias - CID M S - Junta Medica Ortopedista e Clinico Geral
    [Tags]    setup    pmv    lts    lts_ortopedia    borda    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_60DIAS_ORTOP    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    61    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LTS INSS (tipo separado) → Clínico Geral
# ══════════════════════════════════════════════════════════

LTS INSS - 1 Dia - Clinico Geral
    [Tags]    setup    pmv    lts_inss
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_INSS_1DIA    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${LTS_INSS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LTF — Licença para Tratamento de Pessoa da Família
# Regras: 1-3d → Médico Trabalho | 4-59d → Clínico Geral
#         60+d → Junta/Clínico Geral
# ══════════════════════════════════════════════════════════

LTF - 1 Dia - Medico Trabalho
    [Tags]    setup    pmv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTF_1DIA    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTF - 3 Dias - Limite Medico Trabalho
    [Tags]    setup    pmv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTF_3DIAS    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    3    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTF - 4 Dias - Inicio Clinico Geral
    [Tags]    setup    pmv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTF_4DIAS    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    4    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTF - 59 Dias - Limite Antes Junta
    [Tags]    setup    pmv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTF_59DIAS    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    59    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTF - 61 Dias - Junta Medica Clinico Geral
    [Tags]    setup    pmv    ltf    borda    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTF_60DIAS    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    61    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# OUTROS TIPOS
# ══════════════════════════════════════════════════════════

Consulta Medica - 1 Dia - Medico Trabalho
    [Tags]    setup    pmv    outros    consulta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    CONSULTA_1DIA    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${CONSULTA}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Exame Admissional - 1 Dia - Clinico Geral
    [Tags]    setup    pmv    outros    admissional
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    EXAME_ADMISSIONAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${ADMISSIONAL}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Licenca Gestacao - 120 Dias - Clinico Geral
    [Tags]    setup    pmv    outros    gestacao
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    GESTACAO_120DIAS    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    120    ${GESTACAO}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Atividade Com Restricao - 1 Dia - Junta Medica Clinico Geral
    [Tags]    setup    pmv    outros    restricao    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    RESTRICAO_1DIA    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${RESTRICAO}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Acidente de Trabalho - 1 Dia - Medico Trabalho
    [Tags]    setup    pmv    outros    acidente
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    ACIDENTE_1DIA    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${ACIDENTE}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Processos Administrativos - 1 Dia - Medico Trabalho
    [Tags]    setup    pmv    outros    adm
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PROCESSOS_ADM_1DIA    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PROCESSOS_ADM}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}
