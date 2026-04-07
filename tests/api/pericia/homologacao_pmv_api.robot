*** Settings ***
Library       ../../../resources/keywords/pericia_helper.py
Resource      ../../../resources/keywords/mihmo_auth.robot
Variables     ../../../resources/variables/homolog.yaml

*** Keywords ***
Homologar Regra API
    [Arguments]    ${regra}    ${especialista_esperado}    ${junta}=${FALSE}
    ${existe}=    Regra Existe Na Massa    ${regra}
    Skip If    not ${existe}    Regra '${regra}' não está no massa_criada.json — rode criar_massa.robot primeiro
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
    # Passo 3: Homologar a perícia (apenas casos não-junta)
    IF    not ${junta}
        ${status}=    Homologar Pericia    ${API_URL}    ${token}    ${regra}
        Should Be Equal    ${status}    Accepted
        ...    Status da homologação diverge! Esperado: 'Accepted' | Recebido: '${status}'
    END

*** Test Cases ***

# ══════════════════════════════════════════════════════════
# LTS — CID GERAL
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID Geral - Deve ir para Medico Trabalho
    [Tags]    homolog    api    pmv    lts    lts_geral
    Homologar Regra API    LTS_1DIA_GERAL    Médico Trabalho

LTS - 3 Dias - CID Geral - Deve ir para Medico Trabalho
    [Tags]    homolog    api    pmv    lts    lts_geral
    Homologar Regra API    LTS_3DIAS_GERAL    Médico Trabalho

LTS - 4 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    lts    lts_geral
    Homologar Regra API    LTS_4DIAS_GERAL    Clínico Geral

LTS - 14 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    lts    lts_geral
    Homologar Regra API    LTS_14DIAS_GERAL    Clínico Geral

LTS - 15 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    lts    lts_geral
    Homologar Regra API    LTS_15DIAS_GERAL    Clínico Geral

LTS - 59 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    lts    lts_geral
    Homologar Regra API    LTS_59DIAS_GERAL    Clínico Geral

LTS - 60 Dias - CID Geral - Deve ir para Junta Medica
    [Tags]    homolog    api    pmv    lts    lts_geral    junta
    Homologar Regra API    LTS_60DIAS_GERAL    Clínico Geral    junta=${TRUE}

# ══════════════════════════════════════════════════════════
# LTS — CID F
# ══════════════════════════════════════════════════════════

LTS - 4 Dias - CID F - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    lts    lts_psiquiatria
    Homologar Regra API    LTS_4DIAS_PSIQ    Clínico Geral

LTS - 29 Dias - CID F - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    lts    lts_psiquiatria
    Homologar Regra API    LTS_29DIAS_PSIQ    Clínico Geral

LTS - 30 Dias - CID F - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    lts    lts_psiquiatria
    Homologar Regra API    LTS_30DIAS_PSIQ    Clínico Geral

LTS - 59 Dias - CID F - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    lts    lts_psiquiatria
    Homologar Regra API    LTS_59DIAS_PSIQ    Clínico Geral

LTS - 60 Dias - CID F - Deve ir para Junta Psiquiatra
    [Tags]    homolog    api    pmv    lts    lts_psiquiatria    junta
    Homologar Regra API    LTS_60DIAS_PSIQ    Psiquiatra    junta=${TRUE}

# ══════════════════════════════════════════════════════════
# LTS — CID M,S
# ══════════════════════════════════════════════════════════

LTS - 4 Dias - CID MS - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    lts    lts_ortopedia
    Homologar Regra API    LTS_4DIAS_ORTOP    Clínico Geral

LTS - 14 Dias - CID MS - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    lts    lts_ortopedia
    Homologar Regra API    LTS_14DIAS_ORTOP    Clínico Geral

LTS - 15 Dias - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    pmv    lts    lts_ortopedia
    Homologar Regra API    LTS_15DIAS_ORTOP    Ortopedista

LTS - 59 Dias - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    pmv    lts    lts_ortopedia
    Homologar Regra API    LTS_59DIAS_ORTOP    Ortopedista

LTS - 60 Dias - CID MS - Deve ir para Junta Ortopedista
    [Tags]    homolog    api    pmv    lts    lts_ortopedia    junta
    Homologar Regra API    LTS_60DIAS_ORTOP    Ortopedista    junta=${TRUE}

# ══════════════════════════════════════════════════════════
# LTS INSS
# ══════════════════════════════════════════════════════════

LTS INSS - 1 Dia - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    lts_inss
    Homologar Regra API    LTS_INSS_1DIA    Clínico Geral

# ══════════════════════════════════════════════════════════
# LTF
# ══════════════════════════════════════════════════════════

LTF - 1 Dia - Deve ir para Medico Trabalho
    [Tags]    homolog    api    pmv    ltf
    Homologar Regra API    LTF_1DIA    Médico Trabalho

LTF - 3 Dias - Deve ir para Medico Trabalho
    [Tags]    homolog    api    pmv    ltf
    Homologar Regra API    LTF_3DIAS    Médico Trabalho

LTF - 4 Dias - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    ltf
    Homologar Regra API    LTF_4DIAS    Clínico Geral

LTF - 59 Dias - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    ltf
    Homologar Regra API    LTF_59DIAS    Clínico Geral

LTF - 60 Dias - Deve ir para Junta Medica
    [Tags]    homolog    api    pmv    ltf    junta
    Homologar Regra API    LTF_60DIAS    Clínico Geral    junta=${TRUE}

# ══════════════════════════════════════════════════════════
# OUTROS
# ══════════════════════════════════════════════════════════

Consulta Medica - Deve ir para Medico Trabalho
    [Tags]    homolog    api    pmv    outros
    Homologar Regra API    CONSULTA_1DIA    Médico Trabalho

Exame Admissional - Deve ir para Clinico Geral
    [Tags]    homolog    api    pmv    outros
    Homologar Regra API    EXAME_ADMISSIONAL    Clínico Geral

Acidente Trabalho - Deve ir para Medico Trabalho
    [Tags]    homolog    api    pmv    outros
    Homologar Regra API    ACIDENTE_1DIA    Médico Trabalho

Processos Administrativos - Deve ir para Medico Trabalho
    [Tags]    homolog    api    pmv    outros
    Homologar Regra API    PROCESSOS_ADM_1DIA    Médico Trabalho
