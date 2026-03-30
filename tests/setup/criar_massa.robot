*** Settings ***
Library       ../../resources/keywords/pericia_helper.py
Resource      ../../resources/keywords/mihmo_auth.robot
Variables     ../../resources/variables/homolog.yaml

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
# LTS — CID GERAL
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID Geral - Medico Trabalho
    [Tags]    setup    pmv    lts    lts_geral    1dia
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_1DIA_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 3 Dias - CID Geral - Limite Medico Trabalho
    [Tags]    setup    pmv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_3DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    3    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 4 Dias - CID Geral - Inicio Clinico Geral
    [Tags]    setup    pmv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_4DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    4    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 14 Dias - CID Geral - Limite Clinico Geral
    [Tags]    setup    pmv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_14DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    14    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 15 Dias - CID Geral - Limite Clinica Homologa
    [Tags]    setup    pmv    lts    lts_geral    borda    inss_borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_15DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    15    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 16 Dias - CID Geral - Inicio INSS
    [Tags]    setup    pmv    lts    lts_geral    borda    inss_borda    inss
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_16DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    16    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 59 Dias - CID Geral - Limite Antes Junta
    [Tags]    setup    pmv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_59DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    59    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 60 Dias - CID Geral - Junta Medica
    [Tags]    setup    pmv    lts    lts_geral    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_60DIAS_GERAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    60    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

# ══════════════════════════════════════════════════════════
# LTS — CID M e S (ORTOPEDIA)
# ══════════════════════════════════════════════════════════

LTS - 4 a 14 Dias - CID M S - Clinico Geral Ortopedista
    [Tags]    setup    pmv    lts    lts_ortopedia
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_4DIAS_ORTOP    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    10    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 15 Dias - CID M S - Limite Clinica Ortopedista
    [Tags]    setup    pmv    lts    lts_ortopedia    borda    inss_borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_15DIAS_ORTOP    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    15    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 16 Dias - CID M S - Inicio INSS Ortopedista
    [Tags]    setup    pmv    lts    lts_ortopedia    borda    inss
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_16DIAS_ORTOP    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    16    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 59 Dias - CID M S - Limite Antes Junta Ortopedista
    [Tags]    setup    pmv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_59DIAS_ORTOP    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    59    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 60 Dias - CID M S - Junta Medica Ortopedista
    [Tags]    setup    pmv    lts    lts_ortopedia    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_60DIAS_ORTOP    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    60    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300

# ══════════════════════════════════════════════════════════
# LTS — CID F (PSIQUIATRIA)
# ══════════════════════════════════════════════════════════

LTS - 4 Dias - CID F - Clinico Geral
    [Tags]    setup    pmv    lts    lts_psiquiatria
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_4DIAS_PSIQ    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    15    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 30 Dias - CID F - Clinico Geral
    [Tags]    setup    pmv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_30DIAS_PSIQ    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    30    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 59 Dias - CID F - Limite Antes Junta
    [Tags]    setup    pmv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_59DIAS_PSIQ    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    59    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300

LTS - 60 Dias - CID F - Junta Medica Psiquiatra
    [Tags]    setup    pmv    lts    lts_psiquiatria    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_60DIAS_PSIQ    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    60    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300

# ══════════════════════════════════════════════════════════
# LTS - INSS
# ══════════════════════════════════════════════════════════

LTS INSS - 1 Dia - Clinico Geral
    [Tags]    setup    pmv    lts_inss    inss
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTS_INSS_1DIA    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${LTS_INSS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

# ══════════════════════════════════════════════════════════
# LTF
# ══════════════════════════════════════════════════════════

LTF - 1 Dia - Medico Trabalho
    [Tags]    setup    pmv    ltf
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTF_1DIA    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    2    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

LTF - 3 Dias - Limite Medico Trabalho
    [Tags]    setup    pmv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTF_3DIAS    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    3    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

LTF - 4 Dias - Inicio Clinico Geral
    [Tags]    setup    pmv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTF_4DIAS    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    4    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

LTF - 59 Dias - Limite Antes Junta
    [Tags]    setup    pmv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTF_59DIAS    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    59    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

LTF - 60 Dias - Junta Medica
    [Tags]    setup    pmv    ltf    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    LTF_60DIAS    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    60    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

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
    ...    2026-04-01    1    ${CONSULTA}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

Exame Admissional - 1 Dia - Clinico Geral
    [Tags]    setup    pmv    outros    admissional
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    EXAME_ADMISSIONAL    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${ADMISSIONAL}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

Licenca Gestacao - 120 Dias - Clinico Geral
    [Tags]    setup    pmv    outros    gestacao
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    GESTACAO_120DIAS    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    120    ${GESTACAO}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

Atividade Com Restricao - 1 Dia - Junta Medica
    [Tags]    setup    pmv    outros    restricao
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    RESTRICAO_1DIA    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${RESTRICAO}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

Acidente de Trabalho - 1 Dia - Medico Trabalho
    [Tags]    setup    pmv    outros    acidente
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    ACIDENTE_1DIA    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${ACIDENTE}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300

Processos Administrativos - 1 Dia - Medico Trabalho
    [Tags]    setup    pmv    outros    adm
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PROCESSOS_ADM_1DIA    ${COMPANY_PMV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${PROCESSOS_ADM}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300
