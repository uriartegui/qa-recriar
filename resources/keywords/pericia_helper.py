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
            "admission_date": "2020-01-01",
            "department": "101",
            "job_title": "101",
            "location": "Teste",
            "cnpj_location": "11111111111111",
            "employment_category": "101",
            "functional_registration": "AUTO001"
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
                with open(MASSA_FILE, 'w') as f:
                    json.dump(dados, f, indent=2, ensure_ascii=False)
    print(f"Status: {response.status_code}")
    return response.status_code, response.text
