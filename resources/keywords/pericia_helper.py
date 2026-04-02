import requests
import json
import random
import time
import os
from datetime import datetime

MASSA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'massa_criada.json')
_customer_regra = {}

def gerar_sufixo():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choices(chars, k=4))

def gerar_nome_servidor(regra):
    data = datetime.now().strftime("%Y%m%d")
    sufixo = gerar_sufixo()
    return f"TESTE_{regra}_{data}_{sufixo}"

def gerar_cpf_unico():
    return str(random.randint(10000000000, 99999999999))

def gerar_matricula():
    numero = random.randint(10000000, 99999999)
    return f"{numero:08d}/01"

def gerar_data_admissao():
    hoje = datetime.now()
    if hoje.month == 1:
        admissao = hoje.replace(year=hoje.year - 1, month=12)
    else:
        admissao = hoje.replace(month=hoje.month - 1)
    return admissao.strftime("%Y-%m-%d")

def limpar_massa():
    if os.path.exists(MASSA_FILE):
        os.remove(MASSA_FILE)
    print("massa_criada.json limpo para nova execução.")

def salvar_massa(regra, customer_id, cpf, nome):
    dados = {}
    if os.path.exists(MASSA_FILE):
        with open(MASSA_FILE, 'r') as f:
            dados = json.load(f)
    dados[regra] = {
        "customer_id": customer_id,
        "cpf": cpf,
        "nome": nome,
        "cid": None,
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    os.makedirs(os.path.dirname(MASSA_FILE), exist_ok=True)
    with open(MASSA_FILE, 'w') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    print(f"Massa salva: {regra} → {nome}")
    _customer_regra[customer_id] = regra

def criar_customer(api_url, token, regra, company_id, tipo="Main"):
    url = f"{api_url}/customer"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    nome = gerar_nome_servidor(regra)
    cpf = gerar_cpf_unico()
    matricula = gerar_matricula()
    admission_date = gerar_data_admissao()
    payload = {
        "email": f"teste.auto.{int(time.time())}@mihmo.com",
        "name": nome,
        "gender": "Male",
        "cpf": cpf,
        "cellphone": "11999999999",
        "companyId": company_id,
        "type": tipo,
        "birthday": "1990-01-01",
        "registrations": [{
            "admission_date": admission_date,
            "department": "Secretaria",
            "job_title": "Agente",
            "location": "Teste",
            "cnpj_location": "11111111111111",
            "employment_category": "101",
            "functional_registration": matricula
        }]
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Criar customer [{nome}] status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        customer_id = data.get("customerid")
        salvar_massa(regra, customer_id, cpf, nome)
        return customer_id, cpf, nome
    raise Exception(f"Erro ao criar customer: {response.status_code} - {response.text[:300]}")

def criar_pericia_api(api_url, token, customer_id, cpf, cellphone, email,
                      start_date, days, tipo, cid, file_path):
    url = f"{api_url}/medical-expert-report-request/customer-lead/recriar"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "customerId": json.dumps(customer_id),
        "cpf": json.dumps(cpf),
        "origin": json.dumps("Customer"),
        "cellphone": json.dumps(cellphone),
        "email": json.dumps(email),
        "startDate": json.dumps(start_date),
        "days": days,
        "type": json.dumps(tipo),
        "medicCrm": json.dumps("1515"),
        "medicUf": json.dumps("AC"),
        "cid": json.dumps(cid),
    }
    with open(file_path, "rb") as f:
        files = {"files": ("atestado.png", f, "image/png")}
        response = requests.post(url, data=data, files=files, headers=headers)
    if response.status_code < 300 and customer_id in _customer_regra:
        regra = _customer_regra[customer_id]
        if os.path.exists(MASSA_FILE):
            with open(MASSA_FILE, 'r') as f:
                dados = json.load(f)
            if regra in dados:
                dados[regra]["cid"] = cid
                try:
                    pericia_id = response.json().get("id")
                    dados[regra]["pericia_id"] = pericia_id
                except Exception:
                    pass
                with open(MASSA_FILE, 'w') as f:
                    json.dump(dados, f, indent=2, ensure_ascii=False)
    print(f"Status: {response.status_code}")
    return response.status_code, response.text

def ler_massa(regra):
    if not os.path.exists(MASSA_FILE):
        raise Exception(f"massa_criada.json não encontrado. Rode criar_massa.robot primeiro.")
    with open(MASSA_FILE, 'r') as f:
        dados = json.load(f)
    if regra not in dados:
        raise Exception(f"Regra '{regra}' não encontrada no massa_criada.json.")
    return dados[regra]["nome"]

def verificar_especialista_api(api_url, token, regra):
    if not os.path.exists(MASSA_FILE):
        raise Exception("massa_criada.json não encontrado.")
    with open(MASSA_FILE, 'r') as f:
        dados = json.load(f)
    if regra not in dados:
        raise Exception(f"Regra '{regra}' não encontrada no massa_criada.json.")
    pericia_id = dados[regra].get("pericia_id")
    nome = dados[regra].get("nome", "")
    if not pericia_id:
        raise Exception(f"pericia_id não encontrado para '{regra}'. Recrie a massa.")

    # A fila da clínica usa um serviço diferente (/attendance/api)
    base_url = api_url.rsplit('/backend-nest', 1)[0]
    fila_url = f"{base_url}/attendance/api/scheduled-attendance/clinic"
    headers = {"Authorization": f"Bearer {token}"}

    page = 1
    while True:
        params = {
            "page": page,
            "pageSize": 50,
            "search": nome,
            "status": "active",
            "type": "faceToFace"
        }
        response = requests.get(fila_url, params=params, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Erro ao buscar fila da clínica: {response.status_code} - {response.text[:200]}")
        data = response.json()

        for grupo in data.get("items", []):
            for atendimento in grupo.get("attendances", []):
                if atendimento.get("medicalExpertReportRequestId") == pericia_id:
                    role = atendimento.get("roleName", "")
                    is_junta = atendimento.get("medicalBoard", False)
                    board_roles = [r.get("description", "") for r in atendimento.get("medicalBoardRoles", [])]
                    attendance_id = atendimento.get("id", "")
                    print(f"Especialista encontrado: roleName={role}, medicalBoard={is_junta}, attendance_id={attendance_id}")
                    return role, is_junta, board_roles, attendance_id

        if not data.get("hasNext", False):
            break
        page += 1

    raise Exception(f"Perícia '{pericia_id}' não encontrada na fila da clínica para regra '{regra}'.")


def enviar_para_fila(api_url, token, attendance_id):
    base_url = api_url.rsplit('/backend-nest', 1)[0]
    url = f"{base_url}/attendance/api/scheduled-attendance/{attendance_id}/queue"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers)
    if response.status_code not in (200, 201):
        raise Exception(f"Erro ao enviar para fila: {response.status_code} - {response.text[:200]}")
    data = response.json()
    event_type = data.get("eventType", "")
    is_junta = data.get("medicalBoard", False)
    print(f"Enviado para fila. eventType={event_type}, medicalBoard={is_junta}")
    return event_type, is_junta
