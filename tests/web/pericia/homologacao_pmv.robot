*** Settings ***
Library       Browser
Library       ../../../resources/keywords/pericia_helper.py
Resource      ../../../resources/pages/login_page.robot
Resource      ../../../resources/pages/pericia_page.robot
Variables     ../../../resources/variables/homolog.yaml
Suite Setup   Login E Aguardar Home

*** Variables ***
${DATA_TESTE}    01/04/2026

*** Keywords ***
Login E Aguardar Home
    Abrir Login        ${BASE_URL}
    Preencher Login    ${EMAIL_VALIDO}    ${SENHA_VALIDA}
    Clicar Entrar
    Wait For Navigation    url=**/home    timeout=10s

Homologar Regra
    [Arguments]    ${regra}    ${tipo_pericia}    ${dias}    ${especialista_esperado}    ${junta}=${FALSE}
    ${servidor}=    Ler Massa    ${regra}
    ${token}=       Autenticar No Mihmo
    Navegar Para Nova Pericia    ${BASE_URL}
    Preencher Formulario Pericia    ${servidor}    ${tipo_pericia}    ${DATA_TESTE}    ${dias}
    Wait For Navigation    url=**/medical-expertise/**    timeout=15s
    ${pericia_id}=    Obter ID Da Pericia Da URL
    ${role}    ${is_junta}    ${board_roles}=    Verificar Especialista Api
    ...    ${API_URL}    ${token}    ${pericia_id}
    IF    ${junta}
        Should Be True    ${is_junta}    Esperado Junta Médica mas isMedicalBoard=False
        Should Contain    ${board_roles}    ${especialista_esperado}
    ELSE
        Should Be Equal    ${role}    ${especialista_esperado}
    END

*** Test Cases ***

# ══════════════════════════════════════════════════════════
# LTS — CID GERAL
# ══════════════════════════════════════════════════════════

LTS - 1 Dia - CID Geral - Deve ir para Medico Trabalho
    [Tags]    homolog    pmv    lts    lts_geral
    Homologar Regra    LTS_1DIA_GERAL
    ...    Licença para Tratamento de Saúde (LTS)
    ...    1    Médico Trabalho

LTS - 3 Dias - CID Geral - Deve ir para Medico Trabalho
    [Tags]    homolog    pmv    lts    lts_geral
    Homologar Regra    LTS_3DIAS_GERAL
    ...    Licença para Tratamento de Saúde (LTS)
    ...    3    Médico Trabalho

LTS - 4 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    lts    lts_geral
    Homologar Regra    LTS_4DIAS_GERAL
    ...    Licença para Tratamento de Saúde (LTS)
    ...    4    Clínico Geral

LTS - 14 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    lts    lts_geral
    Homologar Regra    LTS_14DIAS_GERAL
    ...    Licença para Tratamento de Saúde (LTS)
    ...    14    Clínico Geral

LTS - 15 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    lts    lts_geral
    Homologar Regra    LTS_15DIAS_GERAL
    ...    Licença para Tratamento de Saúde (LTS)
    ...    15    Clínico Geral

LTS - 59 Dias - CID Geral - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    lts    lts_geral
    Homologar Regra    LTS_59DIAS_GERAL
    ...    Licença para Tratamento de Saúde (LTS)
    ...    59    Clínico Geral

LTS - 60 Dias - CID Geral - Deve ir para Junta Medica
    [Tags]    homolog    pmv    lts    lts_geral    junta
    Homologar Regra    LTS_60DIAS_GERAL
    ...    Licença para Tratamento de Saúde (LTS)
    ...    60    Clínico Geral    junta=${TRUE}

# ══════════════════════════════════════════════════════════
# LTS — CID F
# ══════════════════════════════════════════════════════════

LTS - 4 Dias - CID F - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    lts    lts_psiquiatria
    Homologar Regra    LTS_4DIAS_PSIQ
    ...    Licença para Tratamento de Saúde (LTS)
    ...    4    Clínico Geral

LTS - 29 Dias - CID F - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    lts    lts_psiquiatria
    Homologar Regra    LTS_29DIAS_PSIQ
    ...    Licença para Tratamento de Saúde (LTS)
    ...    29    Clínico Geral

LTS - 30 Dias - CID F - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    lts    lts_psiquiatria
    Homologar Regra    LTS_30DIAS_PSIQ
    ...    Licença para Tratamento de Saúde (LTS)
    ...    30    Clínico Geral

LTS - 59 Dias - CID F - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    lts    lts_psiquiatria
    Homologar Regra    LTS_59DIAS_PSIQ
    ...    Licença para Tratamento de Saúde (LTS)
    ...    59    Clínico Geral

LTS - 60 Dias - CID F - Deve ir para Junta Psiquiatra
    [Tags]    homolog    pmv    lts    lts_psiquiatria    junta
    Homologar Regra    LTS_60DIAS_PSIQ
    ...    Licença para Tratamento de Saúde (LTS)
    ...    60    Psiquiatra    junta=${TRUE}

# ══════════════════════════════════════════════════════════
# LTS — CID M,S
# ══════════════════════════════════════════════════════════

LTS - 4 Dias - CID MS - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    lts    lts_ortopedia
    Homologar Regra    LTS_4DIAS_ORTOP
    ...    Licença para Tratamento de Saúde (LTS)
    ...    4    Clínico Geral

LTS - 14 Dias - CID MS - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    lts    lts_ortopedia
    Homologar Regra    LTS_14DIAS_ORTOP
    ...    Licença para Tratamento de Saúde (LTS)
    ...    14    Clínico Geral

LTS - 15 Dias - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    pmv    lts    lts_ortopedia
    Homologar Regra    LTS_15DIAS_ORTOP
    ...    Licença para Tratamento de Saúde (LTS)
    ...    15    Ortopedista

LTS - 59 Dias - CID MS - Deve ir para Ortopedista
    [Tags]    homolog    pmv    lts    lts_ortopedia
    Homologar Regra    LTS_59DIAS_ORTOP
    ...    Licença para Tratamento de Saúde (LTS)
    ...    59    Ortopedista

LTS - 60 Dias - CID MS - Deve ir para Junta Ortopedista
    [Tags]    homolog    pmv    lts    lts_ortopedia    junta
    Homologar Regra    LTS_60DIAS_ORTOP
    ...    Licença para Tratamento de Saúde (LTS)
    ...    60    Ortopedista    junta=${TRUE}

# ══════════════════════════════════════════════════════════
# LTS INSS
# ══════════════════════════════════════════════════════════

LTS INSS - 1 Dia - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    lts_inss
    Homologar Regra    LTS_INSS_1DIA
    ...    Licença para Tratamento de Saúde (LTS) - INSS
    ...    1    Clínico Geral

# ══════════════════════════════════════════════════════════
# LTF
# ══════════════════════════════════════════════════════════

LTF - 1 Dia - Deve ir para Medico Trabalho
    [Tags]    homolog    pmv    ltf
    Homologar Regra    LTF_1DIA
    ...    Licença para Tratamento de Pessoa da Família (LTF)
    ...    1    Médico Trabalho

LTF - 3 Dias - Deve ir para Medico Trabalho
    [Tags]    homolog    pmv    ltf
    Homologar Regra    LTF_3DIAS
    ...    Licença para Tratamento de Pessoa da Família (LTF)
    ...    3    Médico Trabalho

LTF - 4 Dias - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    ltf
    Homologar Regra    LTF_4DIAS
    ...    Licença para Tratamento de Pessoa da Família (LTF)
    ...    4    Clínico Geral

LTF - 59 Dias - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    ltf
    Homologar Regra    LTF_59DIAS
    ...    Licença para Tratamento de Pessoa da Família (LTF)
    ...    59    Clínico Geral

LTF - 60 Dias - Deve ir para Junta Medica
    [Tags]    homolog    pmv    ltf    junta
    Homologar Regra    LTF_60DIAS
    ...    Licença para Tratamento de Pessoa da Família (LTF)
    ...    60    Clínico Geral    junta=${TRUE}

# ══════════════════════════════════════════════════════════
# OUTROS
# ══════════════════════════════════════════════════════════

Consulta Medica - Deve ir para Medico Trabalho
    [Tags]    homolog    pmv    outros
    Homologar Regra    CONSULTA_1DIA
    ...    Consulta Médica
    ...    1    Médico Trabalho

Exame Admissional - Deve ir para Clinico Geral
    [Tags]    homolog    pmv    outros
    Homologar Regra    EXAME_ADMISSIONAL
    ...    Exame Clínico Admissional
    ...    1    Clínico Geral

Acidente Trabalho - Deve ir para Medico Trabalho
    [Tags]    homolog    pmv    outros
    Homologar Regra    ACIDENTE_1DIA
    ...    Primeiro Atendimento - Acidente de Trabalho
    ...    1    Médico Trabalho

Processos Administrativos - Deve ir para Medico Trabalho
    [Tags]    homolog    pmv    outros
    Homologar Regra    PROCESSOS_ADM_1DIA
    ...    Processos Administrativos
    ...    1    Médico Trabalho
