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
${ABANDONO}                     JobAbandonment
${APOSENT_INVALIDEZ}            DisabilityRetirement
${CONSULTA_PPV}                 MedicalConsultation
${GESTACAO_PRE}                 PrepartumPregnancyLicense
${GESTACAO_POS}                 PostpartumPregnancyLicense
${PECUNIA_FERIAS}               PecuniaVacation
${PECUNIA_FERIAS_DEP}           PecuniaVacationDependent
${PECUNIA_PREMIO}               PecuniaAward
${PECUNIA_PREMIO_DEP}           PecuniaAwardDependent
${PARECER_MED}                  MedicalWorkAssessment
${RF}                           FunctionalReadaptation
${RECURSO}                      Appeal
${RED_JORNADA_DEP}              ReductionOfWorkloadJourneyDependent
${RED_JORNADA_SERV}             ReductionOfWorkloadJourneyEmployee
${REMOCAO}                      Removal
${REMOCAO_DEP}                  RemovalDependent

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

# ══════════════════════════════════════════════════════════
# ABANDONO DE EMPREGO (sem especialista definido na regra)
# ══════════════════════════════════════════════════════════

Abandono de Emprego - 1 Dia - CID Geral
    [Tags]    setup    ppv    abandono
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_ABANDONO    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${ABANDONO}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# APOSENTADORIA POR INVALIDEZ
# Geral → Médico Trabalho | CID F → Psiquiatra | CID M,S → Ortopedista
# ══════════════════════════════════════════════════════════

Aposentadoria por Invalidez - 1 Dia - CID Geral - Medico Trabalho
    [Tags]    setup    ppv    aposent_invalidez
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_APOSENT_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${APOSENT_INVALIDEZ}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Aposentadoria por Invalidez - 1 Dia - CID F - Psiquiatra
    [Tags]    setup    ppv    aposent_invalidez
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_APOSENT_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${APOSENT_INVALIDEZ}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Aposentadoria por Invalidez - 1 Dia - CID MS - Ortopedista
    [Tags]    setup    ppv    aposent_invalidez
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_APOSENT_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${APOSENT_INVALIDEZ}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# CONSULTA MÉDICA → Clínico Geral
# ══════════════════════════════════════════════════════════

Consulta Medica - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    consulta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_CONSULTA    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${CONSULTA_PPV}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LICENÇA GESTAÇÃO pré-parto → Clínico Geral
# LICENÇA GESTAÇÃO pós-parto → Clínico Geral
# ══════════════════════════════════════════════════════════

Licenca Gestacao Pre-parto - 1 Dia - Clinico Geral
    [Tags]    setup    ppv    gestacao
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_GESTACAO_PRE    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${GESTACAO_PRE}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Licenca Gestacao Pos-parto - 1 Dia - Clinico Geral
    [Tags]    setup    ppv    gestacao
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_GESTACAO_POS    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${GESTACAO_POS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LICENÇA FÉRIAS PECÚNIA
# Geral → Clínico Geral | CID F → Psiquiatra | CID M,S → Ortopedista
# ══════════════════════════════════════════════════════════

Ferias Pecunia - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    ferias_pecunia
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FER_PECUNIA_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_FERIAS}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Ferias Pecunia - 1 Dia - CID F - Psiquiatra
    [Tags]    setup    ppv    ferias_pecunia
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FER_PECUNIA_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_FERIAS}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Ferias Pecunia - 1 Dia - CID MS - Ortopedista
    [Tags]    setup    ppv    ferias_pecunia
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FER_PECUNIA_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_FERIAS}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LICENÇA FÉRIAS PECÚNIA - DEPENDENTE
# Geral → Clínico Geral | CID F → Psiquiatra | CID M,S → Ortopedista
# ══════════════════════════════════════════════════════════

Ferias Pecunia Dependente - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    ferias_pecunia_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FER_PECUNIA_DEP_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_FERIAS_DEP}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Ferias Pecunia Dependente - 1 Dia - CID F - Psiquiatra
    [Tags]    setup    ppv    ferias_pecunia_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FER_PECUNIA_DEP_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_FERIAS_DEP}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Ferias Pecunia Dependente - 1 Dia - CID MS - Ortopedista
    [Tags]    setup    ppv    ferias_pecunia_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_FER_PECUNIA_DEP_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_FERIAS_DEP}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LICENÇA PRÊMIO PECÚNIA
# Geral → Clínico Geral | CID F → Psiquiatra | CID M,S → Ortopedista
# ══════════════════════════════════════════════════════════

Premio Pecunia - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    premio_pecunia
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECUNIA_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_PREMIO}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Premio Pecunia - 1 Dia - CID F - Psiquiatra
    [Tags]    setup    ppv    premio_pecunia
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECUNIA_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_PREMIO}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Premio Pecunia - 1 Dia - CID MS - Ortopedista
    [Tags]    setup    ppv    premio_pecunia
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECUNIA_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_PREMIO}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# LICENÇA PRÊMIO PECÚNIA - DEPENDENTE
# Geral → Clínico Geral | CID F → Psiquiatra | CID M,S → Ortopedista
# ══════════════════════════════════════════════════════════

Premio Pecunia Dependente - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    premio_pecunia_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECUNIA_DEP_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_PREMIO_DEP}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Premio Pecunia Dependente - 1 Dia - CID F - Psiquiatra
    [Tags]    setup    ppv    premio_pecunia_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECUNIA_DEP_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_PREMIO_DEP}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Premio Pecunia Dependente - 1 Dia - CID MS - Ortopedista
    [Tags]    setup    ppv    premio_pecunia_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PREMIO_PECUNIA_DEP_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PECUNIA_PREMIO_DEP}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# PARECER MÉDICO DO TRABALHO → Médico Trabalho
# ══════════════════════════════════════════════════════════

Parecer Medico do Trabalho - 1 Dia - CID Geral - Medico Trabalho
    [Tags]    setup    ppv    parecer_med
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_PARECER_MED    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${PARECER_MED}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# READAPTAÇÃO FUNCIONAL (RF) — Junta Médica
# Geral: Clínico Geral + Médico Trabalho
# CID F: Psiquiatra + Clínico Geral + Médico Trabalho
# CID M,S: Ortopedista + Clínico Geral + Médico Trabalho
# ══════════════════════════════════════════════════════════

Readaptacao Funcional - 1 Dia - CID Geral - Junta Clinico Geral
    [Tags]    setup    ppv    rf    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RF_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${RF}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Readaptacao Funcional - 1 Dia - CID F - Junta Psiquiatra
    [Tags]    setup    ppv    rf    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RF_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${RF}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Readaptacao Funcional - 1 Dia - CID MS - Junta Ortopedista
    [Tags]    setup    ppv    rf    junta
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RF_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${RF}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# RECURSO → Clínico Geral
# ══════════════════════════════════════════════════════════

Recurso - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    recurso
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RECURSO    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${RECURSO}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# REDUÇÃO DE CARGA HORÁRIA / JORNADA - SERVIDOR
# Geral → Clínico Geral | CID F → Psiquiatra | CID M,S → Ortopedista
# ══════════════════════════════════════════════════════════

Reducao Jornada Servidor - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    red_jornada_serv
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RED_JORNADA_SERV_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${RED_JORNADA_SERV}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Reducao Jornada Servidor - 1 Dia - CID F - Psiquiatra
    [Tags]    setup    ppv    red_jornada_serv
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RED_JORNADA_SERV_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${RED_JORNADA_SERV}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Reducao Jornada Servidor - 1 Dia - CID MS - Ortopedista
    [Tags]    setup    ppv    red_jornada_serv
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RED_JORNADA_SERV_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${RED_JORNADA_SERV}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# REDUÇÃO DE CARGA HORÁRIA / JORNADA - DEPENDENTE
# Geral: Assistente Social + Clínico Geral
# CID F: Psicólogo + Psiquiatra
# CID M,S: Assistente Social + Ortopedista
# ══════════════════════════════════════════════════════════

Reducao Jornada Dependente - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    red_jornada_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RED_JORNADA_DEP_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${RED_JORNADA_DEP}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Reducao Jornada Dependente - 1 Dia - CID F - Psicologo e Psiquiatra
    [Tags]    setup    ppv    red_jornada_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RED_JORNADA_DEP_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${RED_JORNADA_DEP}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Reducao Jornada Dependente - 1 Dia - CID MS - Assist Social e Ortopedista
    [Tags]    setup    ppv    red_jornada_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_RED_JORNADA_DEP_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${RED_JORNADA_DEP}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# REMOÇÃO POR MOTIVO DE DOENÇA - SERVIDOR
# Geral → Clínico Geral | CID F → Psiquiatra | CID M,S → Ortopedista
# ══════════════════════════════════════════════════════════

Remocao Servidor - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    remocao_serv
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${REMOCAO}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Remocao Servidor - 1 Dia - CID F - Psiquiatra
    [Tags]    setup    ppv    remocao_serv
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${REMOCAO}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Remocao Servidor - 1 Dia - CID MS - Ortopedista
    [Tags]    setup    ppv    remocao_serv
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${REMOCAO}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

# ══════════════════════════════════════════════════════════
# REMOÇÃO POR MOTIVO DE DOENÇA - DEPENDENTE
# Geral: Assistente Social + Clínico Geral
# CID F: Psicólogo + Psiquiatra
# CID M,S: Assistente Social + Ortopedista
# ══════════════════════════════════════════════════════════

Remocao Dependente - 1 Dia - CID Geral - Clinico Geral
    [Tags]    setup    ppv    remocao_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_DEP_GERAL    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${REMOCAO_DEP}    ${CID_GERAL}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Remocao Dependente - 1 Dia - CID F - Psicologo e Psiquiatra
    [Tags]    setup    ppv    remocao_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_DEP_PSIQ    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${REMOCAO_DEP}    ${CID_PSIQ}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}

Remocao Dependente - 1 Dia - CID MS - Assist Social e Ortopedista
    [Tags]    setup    ppv    remocao_dep
    ${token}=    Autenticar No Mihmo
    ${id}    ${cpf}    ${nome}=    Criar Customer
    ...    ${API_URL}    ${token}    PPV_REMOCAO_DEP_ORTOP    ${COMPANY_PPV}
    ${status}    ${body}=    Criar Pericia Api
    ...    ${API_URL}    ${token}    ${id}    ${cpf}
    ...    ${CELL_TESTE}    ${EMAIL_TESTE}
    ...    ${DATA_HOJE}    1    ${REMOCAO_DEP}    ${CID_ORTOPEDIA}    ${FIXTURE}
    Should Be True    ${status} < 300    API retornou ${status}: ${body}
