*** Settings ***
Library       ../../../resources/keywords/pericia_helper.py
Resource      ../../../resources/keywords/mihmo_auth.robot
Variables     ../../../resources/variables/homolog.yaml

*** Keywords ***
Homologar Regra API
    [Arguments]    ${regra}    ${especialista_esperado}    ${junta}=${FALSE}
    ${existe}=    Regra Existe Na Massa    ${regra}
    Skip If    not ${existe}    Regra '${regra}' não está no massa_criada.json — rode criar_massa_ppv.robot primeiro
    ${token}=    Autenticar No Mihmo

    Sleep    5s

    # Passo 1: Verificar roteamento na fila da clínica
    ${role}    ${is_junta}    ${board_roles}    ${att_id}=    Verificar Especialista Api
    ...    ${API_URL}    ${token}    ${regra}
    IF    ${junta}
        Should Be True    ${is_junta}
        ...    Esperado Junta Médica mas isMedicalBoard=False para regra '${regra}'
        Should Contain    ${board_roles}    ${especialista_esperado}
        ...    Especialista '${especialista_esperado}' não encontrado na junta. Encontrado: ${board_roles}
    ELSE
        Should Be Equal    ${role}    ${especialista_esperado}
        ...    Especialista errado! Esperado: '${especialista_esperado}' | Recebido: '${role}'
    END
    # Passo 2: Enviar para fila do médico e confirmar eventType
    ${event_type}    ${is_junta_fila}=    Enviar Para Fila
    ...    ${API_URL}    ${token}    ${att_id}    ${regra}
    IF    ${junta}
        Should Be True    ${is_junta_fila}
        ...    Junta não confirmada após envio para fila. regra='${regra}'
    ELSE
        Should Be Equal    ${event_type}    ${especialista_esperado}
        ...    eventType na fila diverge! Esperado: '${especialista_esperado}' | Recebido: '${event_type}'
    END
    # Passo 3: Homologar a perícia
    ${status}=    Homologar Pericia    ${API_URL}    ${token}    ${regra}
    Should Be Equal    ${status}    Accepted
    ...    Status da homologação diverge! Esperado: 'Accepted' | Recebido: '${status}'

*** Test Cases ***

# ══════════════════════════════════════════════════════════
# LTS — CID GERAL → Clínico Geral
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    lts    lts_geral
    Homologar Regra API    PPV_LTS_1DIA_GERAL    Clínico Geral

LTS - 14 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    lts    lts_geral
    Homologar Regra API    PPV_LTS_14DIAS_GERAL    Clínico Geral

LTS - 15 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    lts    lts_geral
    Homologar Regra API    PPV_LTS_15DIAS_GERAL    Clínico Geral

LTS - 29 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    lts    lts_geral
    Homologar Regra API    PPV_LTS_29DIAS_GERAL    Clínico Geral

LTS - 30 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    lts    lts_geral
    Homologar Regra API    PPV_LTS_30DIAS_GERAL    Clínico Geral

# ══════════════════════════════════════════════════════════
# LTS — CID F → Psiquiatra
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    lts    lts_psiquiatria
    Homologar Regra API    PPV_LTS_1DIA_PSIQ    Psiquiatra

LTS - 14 Dias - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    lts    lts_psiquiatria
    Homologar Regra API    PPV_LTS_14DIAS_PSIQ    Psiquiatra

LTS - 15 Dias - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    lts    lts_psiquiatria
    Homologar Regra API    PPV_LTS_15DIAS_PSIQ    Psiquiatra

LTS - 29 Dias - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    lts    lts_psiquiatria
    Homologar Regra API    PPV_LTS_29DIAS_PSIQ    Psiquiatra

LTS - 30 Dias - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    lts    lts_psiquiatria
    Homologar Regra API    PPV_LTS_30DIAS_PSIQ    Psiquiatra

# ══════════════════════════════════════════════════════════
# LTS — CID M,S → Ortopedista
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    lts    lts_ortopedia
    Homologar Regra API    PPV_LTS_1DIA_ORTOP    Ortopedista

LTS - 14 Dias - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    lts    lts_ortopedia
    Homologar Regra API    PPV_LTS_14DIAS_ORTOP    Ortopedista

LTS - 15 Dias - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    lts    lts_ortopedia
    Homologar Regra API    PPV_LTS_15DIAS_ORTOP    Ortopedista

LTS - 29 Dias - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    lts    lts_ortopedia
    Homologar Regra API    PPV_LTS_29DIAS_ORTOP    Ortopedista

LTS - 30 Dias - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    lts    lts_ortopedia
    Homologar Regra API    PPV_LTS_30DIAS_ORTOP    Ortopedista

# ══════════════════════════════════════════════════════════
# LTF
# ══════════════════════════════════════════════════════════

LTF - 1 Dia - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    ltf
    Homologar Regra API    PPV_LTF_1DIA    Clínico Geral

LTF - 29 Dias - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    ltf
    Homologar Regra API    PPV_LTF_29DIAS    Clínico Geral

LTF - 30 Dias - Deve ir para Clinico Geral e Assistente Social
    [Tags]    homolog    api    ppv    ltf
    Homologar Regra API    PPV_LTF_30DIAS    Clínico Geral
