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
    IF    ${junta}
        Should Be True    '${status}' in ['Accepted', 'SignaturePending']
        ...    Status junta diverge! Esperado: 'Accepted' ou 'SignaturePending' | Recebido: '${status}'
    ELSE
        Should Be Equal    ${status}    Accepted
        ...    Status da homologação diverge! Esperado: 'Accepted' | Recebido: '${status}'
    END

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

# ══════════════════════════════════════════════════════════
# APOSENTADORIA POR INVALIDEZ
# ══════════════════════════════════════════════════════════

Aposentadoria por Invalidez - CID Geral - Deve ir para Medico Trabalho
    [Tags]    homolog    api    ppv    aposent_invalidez
    Homologar Regra API    PPV_APOSENT_GERAL    Médico Trabalho

Aposentadoria por Invalidez - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    aposent_invalidez
    Homologar Regra API    PPV_APOSENT_PSIQ    Psiquiatra

Aposentadoria por Invalidez - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    aposent_invalidez
    Homologar Regra API    PPV_APOSENT_ORTOP    Ortopedista

# ══════════════════════════════════════════════════════════
# CONSULTA MÉDICA → Clínico Geral
# ══════════════════════════════════════════════════════════

Consulta Medica - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    consulta
    Homologar Regra API    PPV_CONSULTA    Clínico Geral

# ══════════════════════════════════════════════════════════
# LICENÇA GESTAÇÃO pré/pós-parto → Clínico Geral
# ══════════════════════════════════════════════════════════

Gestacao Pre-parto - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    gestacao
    Homologar Regra API    PPV_GESTACAO_PRE    Clínico Geral

Gestacao Pos-parto - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    gestacao
    Homologar Regra API    PPV_GESTACAO_POS    Clínico Geral

# ══════════════════════════════════════════════════════════
# LICENÇA FÉRIAS PECÚNIA
# ══════════════════════════════════════════════════════════

Ferias Pecunia - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    ferias_pecunia
    Homologar Regra API    PPV_FER_PECUNIA_GERAL    Clínico Geral

Ferias Pecunia - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    ferias_pecunia
    Homologar Regra API    PPV_FER_PECUNIA_PSIQ    Psiquiatra

Ferias Pecunia - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    ferias_pecunia
    Homologar Regra API    PPV_FER_PECUNIA_ORTOP    Ortopedista

# ══════════════════════════════════════════════════════════
# LICENÇA FÉRIAS PECÚNIA - DEPENDENTE
# ══════════════════════════════════════════════════════════

Ferias Pecunia Dependente - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    ferias_pecunia_dep
    Homologar Regra API    PPV_FER_PECUNIA_DEP_GERAL    Clínico Geral

Ferias Pecunia Dependente - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    ferias_pecunia_dep
    Homologar Regra API    PPV_FER_PECUNIA_DEP_PSIQ    Psiquiatra

Ferias Pecunia Dependente - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    ferias_pecunia_dep
    Homologar Regra API    PPV_FER_PECUNIA_DEP_ORTOP    Ortopedista

# ══════════════════════════════════════════════════════════
# LICENÇA PRÊMIO PECÚNIA
# ══════════════════════════════════════════════════════════

Premio Pecunia - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    premio_pecunia
    Homologar Regra API    PPV_PREMIO_PECUNIA_GERAL    Clínico Geral

Premio Pecunia - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    premio_pecunia
    Homologar Regra API    PPV_PREMIO_PECUNIA_PSIQ    Psiquiatra

Premio Pecunia - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    premio_pecunia
    Homologar Regra API    PPV_PREMIO_PECUNIA_ORTOP    Ortopedista

# ══════════════════════════════════════════════════════════
# LICENÇA PRÊMIO PECÚNIA - DEPENDENTE
# ══════════════════════════════════════════════════════════

Premio Pecunia Dependente - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    premio_pecunia_dep
    Homologar Regra API    PPV_PREMIO_PECUNIA_DEP_GERAL    Clínico Geral

Premio Pecunia Dependente - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    premio_pecunia_dep
    Homologar Regra API    PPV_PREMIO_PECUNIA_DEP_PSIQ    Psiquiatra

Premio Pecunia Dependente - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    premio_pecunia_dep
    Homologar Regra API    PPV_PREMIO_PECUNIA_DEP_ORTOP    Ortopedista

# ══════════════════════════════════════════════════════════
# PARECER MÉDICO DO TRABALHO → Médico Trabalho
# ══════════════════════════════════════════════════════════

Parecer Medico do Trabalho - Deve ir para Medico Trabalho
    [Tags]    homolog    api    ppv    parecer_med
    Homologar Regra API    PPV_PARECER_MED    Médico Trabalho

# ══════════════════════════════════════════════════════════
# READAPTAÇÃO FUNCIONAL (RF) — Junta Médica
# ══════════════════════════════════════════════════════════

Readaptacao Funcional - CID Geral - Deve ir para Junta Clinico Geral
    [Tags]    homolog    api    ppv    rf    junta
    Homologar Regra API    PPV_RF_GERAL    Clínico Geral    junta=${TRUE}

Readaptacao Funcional - CID F - Deve ir para Junta Psiquiatra
    [Tags]    homolog    api    ppv    rf    junta
    Homologar Regra API    PPV_RF_PSIQ    Psiquiatra    junta=${TRUE}

Readaptacao Funcional - CID MS - Deve ir para Junta Ortopedista
    [Tags]    homolog    api    ppv    rf    junta
    Homologar Regra API    PPV_RF_ORTOP    Ortopedista    junta=${TRUE}

# ══════════════════════════════════════════════════════════
# RECURSO → Clínico Geral
# ══════════════════════════════════════════════════════════

Recurso - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    recurso
    Homologar Regra API    PPV_RECURSO    Clínico Geral

# ══════════════════════════════════════════════════════════
# REDUÇÃO DE CARGA HORÁRIA / JORNADA - SERVIDOR
# ══════════════════════════════════════════════════════════

Reducao Jornada Servidor - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    red_jornada_serv
    Homologar Regra API    PPV_RED_JORNADA_SERV_GERAL    Clínico Geral

Reducao Jornada Servidor - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    red_jornada_serv
    Homologar Regra API    PPV_RED_JORNADA_SERV_PSIQ    Psiquiatra

Reducao Jornada Servidor - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    red_jornada_serv
    Homologar Regra API    PPV_RED_JORNADA_SERV_ORTOP    Ortopedista

# ══════════════════════════════════════════════════════════
# REDUÇÃO DE CARGA HORÁRIA / JORNADA - DEPENDENTE
# Geral: Clínico Geral (primário) | CID F: Psiquiatra (primário) | CID M,S: Ortopedista (primário)
# ══════════════════════════════════════════════════════════

Reducao Jornada Dependente - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    red_jornada_dep
    Homologar Regra API    PPV_RED_JORNADA_DEP_GERAL    Clínico Geral

Reducao Jornada Dependente - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    red_jornada_dep
    Homologar Regra API    PPV_RED_JORNADA_DEP_PSIQ    Psiquiatra

Reducao Jornada Dependente - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    red_jornada_dep
    Homologar Regra API    PPV_RED_JORNADA_DEP_ORTOP    Ortopedista

# ══════════════════════════════════════════════════════════
# REMOÇÃO POR MOTIVO DE DOENÇA - SERVIDOR
# ══════════════════════════════════════════════════════════

Remocao Servidor - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    remocao_serv
    Homologar Regra API    PPV_REMOCAO_GERAL    Clínico Geral

Remocao Servidor - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    remocao_serv
    Homologar Regra API    PPV_REMOCAO_PSIQ    Psiquiatra

Remocao Servidor - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    remocao_serv
    Homologar Regra API    PPV_REMOCAO_ORTOP    Ortopedista

# ══════════════════════════════════════════════════════════
# REMOÇÃO POR MOTIVO DE DOENÇA - DEPENDENTE
# Geral: Clínico Geral (primário) | CID F: Psiquiatra (primário) | CID M,S: Ortopedista (primário)
# ══════════════════════════════════════════════════════════

Remocao Dependente - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    api    ppv    remocao_dep
    Homologar Regra API    PPV_REMOCAO_DEP_GERAL    Clínico Geral

Remocao Dependente - CID F - Deve ir para Psiquiatra
    [Tags]    homolog    api    ppv    remocao_dep
    Homologar Regra API    PPV_REMOCAO_DEP_PSIQ    Psiquiatra

Remocao Dependente - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    api    ppv    remocao_dep
    Homologar Regra API    PPV_REMOCAO_DEP_ORTOP    Ortopedista
