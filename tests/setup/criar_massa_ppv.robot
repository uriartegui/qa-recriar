*** Settings ***
Library       ../../resources/keywords/pericia_helper.py
Resource      ../../resources/keywords/mihmo_auth.robot
Variables     ../../resources/variables/homolog.yaml

*** Variables ***
${COMPANY_PPV}      80cf1683-3f88-4941-bf57-e36e799f47bc
${FIXTURE}          ${CURDIR}/../../resources/fixtures/atestado.png
${EMAIL_TESTE}      teste.auto@mihmo.com
${CELL_TESTE}       11999999999

${CID_GERAL}        J00
${CID_ORTOPEDIA}    M54
${CID_PSIQ}         F32

${LTS}              HealthCareLicense
${LTF}              FamilyPersonTreatmentLicense
${CONSULTA}         MedicalConsultation
${GESTACAO_POS}     PostpartumPregnancyLicense
${GESTACAO_PRE}     PrepartumPregnancyLicense
${READAPTACAO}      FunctionalReadaptation
${APOSENTADORIA}    DisabilityRetirement
${REMOCAO_SERV}     Removal
${REMOCAO_DEP}      RemovalDependent
${REDUCAO_SERV}     ReductionOfWorkloadJourneyEmployee
${REDUCAO_DEP}      ReductionOfWorkloadJourneyDependent
${FERIAS_PECU}      PecuniaVacation
${FERIAS_PECU_DEP}  PecuniaVacationDependent
${PREMIO_PECU}      PecuniaAward
${PREMIO_PECU_DEP}  PecuniaAwardDependent
${PARECER}          MedicalWorkAssessment
${RECURSO}          Appeal
${ABANDONO}         JobAbandonment

*** Test Cases ***

# ══════════════════════════════════════════════════════════
# LTS — CID GERAL (Clínico Geral)
# Bordas: 1, 14, 15, 29, 30 dias
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_1DIA_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 14 Dias - CID Geral - Limite Antes 15
    [Tags]    setup    ppv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_14DIAS_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    14    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 15 Dias - CID Geral - Inicio Segunda Faixa
    [Tags]    setup    ppv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_15DIAS_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    15    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 29 Dias - CID Geral - Limite Antes 30
    [Tags]    setup    ppv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_29DIAS_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    29    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 30 Dias - CID Geral - Inicio Terceira Faixa
    [Tags]    setup    ppv    lts    lts_geral    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_30DIAS_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    30    ${LTS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LTS — CID M e S (Ortopedista)
# Bordas: 1, 14, 15, 29, 30 dias
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID M S - Ortopedista
    [Tags]    setup    ppv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_1DIA_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 14 Dias - CID M S - Limite Antes 15
    [Tags]    setup    ppv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_14DIAS_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    14    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 15 Dias - CID M S - Inicio Segunda Faixa
    [Tags]    setup    ppv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_15DIAS_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    15    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 29 Dias - CID M S - Limite Antes 30
    [Tags]    setup    ppv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_29DIAS_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    29    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 30 Dias - CID M S - Inicio Terceira Faixa
    [Tags]    setup    ppv    lts    lts_ortopedia    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_30DIAS_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    30    ${LTS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LTS — CID F (Psiquiatra)
# Bordas: 1, 14, 15, 29, 30 dias
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID F - Psiquiatra
    [Tags]    setup    ppv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_1DIA_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 14 Dias - CID F - Limite Antes 15
    [Tags]    setup    ppv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_14DIAS_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    14    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 15 Dias - CID F - Inicio Segunda Faixa
    [Tags]    setup    ppv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_15DIAS_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    15    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 29 Dias - CID F - Limite Antes 30
    [Tags]    setup    ppv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_29DIAS_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    29    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTS - 30 Dias - CID F - Inicio Terceira Faixa
    [Tags]    setup    ppv    lts    lts_psiquiatria    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTS_30DIAS_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    30    ${LTS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LTF — Licença para Tratamento de Pessoa da Família
# Regra: 1–29 dias → Clínico Geral
#        30+ dias → Clínico Geral + Assistente Social
# ══════════════════════════════════════════════════════════

LTF - 1 Dia - Clinico Geral
    [Tags]    setup    ppv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTF_1DIA    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTF - 29 Dias - Limite Antes Assistente Social
    [Tags]    setup    ppv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTF_29DIAS    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    29    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

LTF - 30 Dias - Clinico Geral e Assistente Social
    [Tags]    setup    ppv    ltf    borda
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_LTF_30DIAS    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    30    ${LTF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LICENÇA GESTAÇÃO
# pré-parto e pós-parto → Clínico Geral
# ══════════════════════════════════════════════════════════

Licenca Gestacao Pre Parto - Clinico Geral
    [Tags]    setup    ppv    outros    gestacao
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_GESTACAO_PRE    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    30    ${GESTACAO_PRE}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Licenca Gestacao Pos Parto - 120 Dias - Clinico Geral
    [Tags]    setup    ppv    outros    gestacao
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_GESTACAO_POS    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    120    ${GESTACAO_POS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# CONSULTA MÉDICA → Clínico Geral
# ══════════════════════════════════════════════════════════

Consulta Medica - 1 Dia - Clinico Geral
    [Tags]    setup    ppv    outros    consulta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_CONSULTA_1DIA    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${CONSULTA}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# READAPTAÇÃO FUNCIONAL — sempre Junta Médica (3 profissionais)
# CID Todos → Clínico Geral + Médico Trabalho
# CID F     → Psiquiatra + Clínico Geral + Médico Trabalho
# CID M,S   → Ortopedista + Clínico Geral + Médico Trabalho
# ══════════════════════════════════════════════════════════

Readaptacao Funcional - CID Geral - Junta Medica
    [Tags]    setup    ppv    outros    readaptacao    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RF_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${READAPTACAO}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Readaptacao Funcional - CID F - Junta Medica Psiquiatra
    [Tags]    setup    ppv    outros    readaptacao    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RF_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${READAPTACAO}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Readaptacao Funcional - CID M S - Junta Medica Ortopedista
    [Tags]    setup    ppv    outros    readaptacao    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RF_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${READAPTACAO}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# APOSENTADORIA POR INVALIDEZ
# CID F     → Psiquiatra
# CID M,S   → Ortopedista
# CID Todos → Médico Trabalho
# ══════════════════════════════════════════════════════════

Aposentadoria Invalidez - CID Geral - Medico Trabalho
    [Tags]    setup    ppv    outros    aposentadoria
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_APOSENT_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${APOSENTADORIA}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Aposentadoria Invalidez - CID F - Psiquiatra
    [Tags]    setup    ppv    outros    aposentadoria
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_APOSENT_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${APOSENTADORIA}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Aposentadoria Invalidez - CID M S - Ortopedista
    [Tags]    setup    ppv    outros    aposentadoria
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_APOSENT_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${APOSENTADORIA}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# REMOÇÃO POR MOTIVO DE DOENÇA — SERVIDOR
# CID Todos → Clínico Geral
# CID F     → Psiquiatra
# CID M,S   → Ortopedista
# ══════════════════════════════════════════════════════════

Remocao Servidor - CID Geral - Clinico Geral
    [Tags]    setup    ppv    outros    remocao
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_SERV_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REMOCAO_SERV}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Remocao Servidor - CID F - Psiquiatra
    [Tags]    setup    ppv    outros    remocao
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_SERV_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REMOCAO_SERV}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Remocao Servidor - CID M S - Ortopedista
    [Tags]    setup    ppv    outros    remocao
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_SERV_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REMOCAO_SERV}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# REMOÇÃO POR MOTIVO DE DOENÇA — DEPENDENTE
# CID Todos → Assistente Social + Clínico Geral
# CID F     → Psicólogo + Psiquiatra
# CID M,S   → Assistente Social + Ortopedista
# ══════════════════════════════════════════════════════════

Remocao Dependente - CID Geral - Assistente Social e Clinico Geral
    [Tags]    setup    ppv    outros    remocao_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_DEP_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REMOCAO_DEP}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Remocao Dependente - CID F - Psicologo e Psiquiatra
    [Tags]    setup    ppv    outros    remocao_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_DEP_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REMOCAO_DEP}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Remocao Dependente - CID M S - Assistente Social e Ortopedista
    [Tags]    setup    ppv    outros    remocao_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_DEP_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REMOCAO_DEP}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# REDUÇÃO DE CARGA HORÁRIA — SERVIDOR
# CID Todos → Clínico Geral
# CID F     → Psiquiatra
# CID M,S   → Ortopedista
# ══════════════════════════════════════════════════════════

Reducao Jornada Servidor - CID Geral - Clinico Geral
    [Tags]    setup    ppv    outros    reducao_serv
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REDUCAO_SERV_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REDUCAO_SERV}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Reducao Jornada Servidor - CID F - Psiquiatra
    [Tags]    setup    ppv    outros    reducao_serv
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REDUCAO_SERV_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REDUCAO_SERV}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Reducao Jornada Servidor - CID M S - Ortopedista
    [Tags]    setup    ppv    outros    reducao_serv
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REDUCAO_SERV_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REDUCAO_SERV}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# REDUÇÃO DE CARGA HORÁRIA — DEPENDENTE
# CID Todos → Assistente Social + Clínico Geral
# CID F     → Psicólogo + Psiquiatra
# CID M,S   → Assistente Social + Ortopedista
# ══════════════════════════════════════════════════════════

Reducao Jornada Dependente - CID Geral - Assistente Social e Clinico Geral
    [Tags]    setup    ppv    outros    reducao_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REDUCAO_DEP_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REDUCAO_DEP}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Reducao Jornada Dependente - CID F - Psicologo e Psiquiatra
    [Tags]    setup    ppv    outros    reducao_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REDUCAO_DEP_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REDUCAO_DEP}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Reducao Jornada Dependente - CID M S - Assistente Social e Ortopedista
    [Tags]    setup    ppv    outros    reducao_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REDUCAO_DEP_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${REDUCAO_DEP}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LICENÇA FÉRIAS PECÚNIA POR MOTIVO DE DOENÇA
# CID Todos → Clínico Geral
# CID F     → Psiquiatra
# CID M,S   → Ortopedista
# ══════════════════════════════════════════════════════════

Ferias Pecunia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    outros    ferias_pecu
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FERIAS_PECU_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${FERIAS_PECU}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Ferias Pecunia - CID F - Psiquiatra
    [Tags]    setup    ppv    outros    ferias_pecu
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FERIAS_PECU_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${FERIAS_PECU}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Ferias Pecunia - CID M S - Ortopedista
    [Tags]    setup    ppv    outros    ferias_pecu
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FERIAS_PECU_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${FERIAS_PECU}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LICENÇA FÉRIAS PECÚNIA — DEPENDENTE
# ══════════════════════════════════════════════════════════

Ferias Pecunia Dependente - CID Geral - Clinico Geral
    [Tags]    setup    ppv    outros    ferias_pecu_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FERIAS_PECU_DEP_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${FERIAS_PECU_DEP}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Ferias Pecunia Dependente - CID F - Psiquiatra
    [Tags]    setup    ppv    outros    ferias_pecu_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FERIAS_PECU_DEP_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${FERIAS_PECU_DEP}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Ferias Pecunia Dependente - CID M S - Ortopedista
    [Tags]    setup    ppv    outros    ferias_pecu_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FERIAS_PECU_DEP_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${FERIAS_PECU_DEP}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LICENÇA PRÊMIO PECÚNIA POR MOTIVO DE DOENÇA
# CID Todos → Clínico Geral
# CID F     → Psiquiatra
# CID M,S   → Ortopedista
# ══════════════════════════════════════════════════════════

Premio Pecunia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    outros    premio_pecu
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECU_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${PREMIO_PECU}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Premio Pecunia - CID F - Psiquiatra
    [Tags]    setup    ppv    outros    premio_pecu
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECU_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${PREMIO_PECU}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Premio Pecunia - CID M S - Ortopedista
    [Tags]    setup    ppv    outros    premio_pecu
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECU_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${PREMIO_PECU}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LICENÇA PRÊMIO PECÚNIA — DEPENDENTE
# ══════════════════════════════════════════════════════════

Premio Pecunia Dependente - CID Geral - Clinico Geral
    [Tags]    setup    ppv    outros    premio_pecu_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECU_DEP_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${PREMIO_PECU_DEP}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Premio Pecunia Dependente - CID F - Psiquiatra
    [Tags]    setup    ppv    outros    premio_pecu_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECU_DEP_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${PREMIO_PECU_DEP}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Premio Pecunia Dependente - CID M S - Ortopedista
    [Tags]    setup    ppv    outros    premio_pecu_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECU_DEP_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${PREMIO_PECU_DEP}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# PARECER MÉDICO DO TRABALHO → Médico Trabalho
# ══════════════════════════════════════════════════════════

Parecer Medico do Trabalho - 1 Dia - Medico Trabalho
    [Tags]    setup    ppv    outros    parecer
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PARECER_1DIA    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${PARECER}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# RECURSO → Clínico Geral
# ══════════════════════════════════════════════════════════

Recurso - 1 Dia - Clinico Geral
    [Tags]    setup    ppv    outros    recurso
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RECURSO_1DIA    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${RECURSO}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# ABANDONO DE EMPREGO → múltiplos especialistas
# ══════════════════════════════════════════════════════════

Abandono de Emprego - 1 Dia - Multi Especialistas
    [Tags]    setup    ppv    outros    abandono
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_ABANDONO_1DIA    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    2026-04-01    1    ${ABANDONO}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}
