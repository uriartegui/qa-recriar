*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    OperatingSystem
Resource   mihmo_auth.robot

*** Keywords ***
Criar Pericia Via API
    [Arguments]    ${customer_id}    ${cpf}    ${cellphone}    ${email}
    ...            ${start_date}    ${days}    ${tipo}    ${cid}
    ${token}=    Autenticar No Mihmo
    ${headers}=    Create Dictionary
    ...    Authorization=Bearer ${token}
    ${data}=    Create Dictionary
    ...    customerId=${customer_id}
    ...    cpf=${cpf}
    ...    origin=Customer
    ...    cellphone=${cellphone}
    ...    email=${email}
    ...    startDate=${start_date}
    ...    days=${days}
    ...    type=${tipo}
    ...    medicCrm=1515
    ...    medicUf=AC
    ...    cid=${cid}
    ${file_content}=    Get Binary File    ${CURDIR}/../../resources/fixtures/atestado.png
    ${files}=    Create Dictionary    files=('atestado.png', ${file_content}, 'image/png')
    ${response}=    POST    ${API_URL}/medical-expert-report-request/customer-lead/recriar
    ...    data=${data}
    ...    files=${files}
    ...    headers=${headers}
    ...    expected_status=any
    Log    Status: ${response.status_code}
    Log    Response: ${response.text}
    RETURN    ${response}
