*** Settings ***
Library    Browser

*** Variables ***
${SELECT_MIHMADO}       p-dropdown >> nth=0
${FILTER_MIHMADO}       input.p-dropdown-filter
${SELECT_TIPO}          p-dropdown >> nth=1
${FILTER_TIPO}          input.p-dropdown-filter
${INPUT_DATA}           po-datepicker input
${INPUT_DIAS}           input[name="quantidadeDias"]
${BTN_SALVAR}           po-button:has-text("Salvar") button

*** Keywords ***
Navegar Para Nova Pericia
    [Arguments]    ${url}
    Go To          ${url}/medical-expertise/create

Selecionar miHmado
    [Arguments]    ${nome}
    Click          ${SELECT_MIHMADO}
    Fill Text      ${FILTER_MIHMADO}    ${nome}
    Click          .p-dropdown-item >> nth=0

Selecionar Tipo de Pericia
    [Arguments]    ${tipo}
    Click          ${SELECT_TIPO}
    Fill Text      ${FILTER_TIPO}    ${tipo}
    Click          .p-dropdown-item >> nth=0

Preencher Data Inicial
    [Arguments]    ${data}
    Fill Text      ${INPUT_DATA}    ${data}

Preencher Quantidade de Dias
    [Arguments]    ${dias}
    Fill Text      ${INPUT_DIAS}    ${dias}

Salvar Pericia
    Click          ${BTN_SALVAR}

Preencher Formulario Pericia
    [Arguments]    ${mihmado}    ${tipo}    ${data}    ${dias}
    Selecionar miHmado            ${mihmado}
    Selecionar Tipo de Pericia    ${tipo}
    Preencher Data Inicial        ${data}
    Preencher Quantidade de Dias  ${dias}
    Salvar Pericia

Login E Navegar Para Pericia
    [Arguments]    ${base_url}    ${email}    ${senha}
    Fazer Login          ${base_url}    ${email}    ${senha}
    Sleep                3s
    Go To                ${base_url}/medical-expertise/create
    Wait For Elements State    ${SELECT_MIHMADO}    visible    timeout=10s

Pericia Cadastrada Com Sucesso
    Wait For Navigation    url=**/medical-expertise/**    timeout=10s
    Get Url                contains    medical-expertise

Verificar Erro Generico
    Get Text    .po-toaster-message >> nth=0    contains    erro
