import requests
import json
import random
import time
import uuid as _uuid
import os
from datetime import datetime, timedelta

MASSA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'massa_criada.json')
FICHA_HOMOLOG_TYPE_ID = "bcfc80cf-12ea-4cb5-8ac2-195895418db1"
_customer_regra = {}

TOKENS = {
    "CLINICA": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjVlODJhZmI0ZWY2OWI3NjM4MzA2OWFjNmI1N2U3ZTY1MjAzYmZlOTYiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQ2xpbmljYSBQTVYgLSBUT1RBTExJRkUiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vbG9raS1kZXYtNDQ0OGUiLCJhdWQiOiJsb2tpLWRldi00NDQ4ZSIsImF1dGhfdGltZSI6MTc3NTUwNTk5MiwidXNlcl9pZCI6IjNhMjRkMzE3LTBmNzEtNDY1Yi05MzNkLTU0ZjI3MzRkYTlkZiIsInN1YiI6IjNhMjRkMzE3LTBmNzEtNDY1Yi05MzNkLTU0ZjI3MzRkYTlkZiIsImlhdCI6MTc3NTUwNTk5MiwiZXhwIjoxNzc1NTA5NTkyLCJlbWFpbCI6Imdlc3Rvcm1paG1vQG1paG1vLmNvbS5iciIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicGhvbmVfbnVtYmVyIjoiKzU1NDMyMTMyMTMyMTMiLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImdlc3Rvcm1paG1vQG1paG1vLmNvbS5iciJdLCJwaG9uZSI6WyIrNTU0MzIxMzIxMzIxMyJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.ov5SJTIZ2YW04nI2XJGT4I0zWcuUX15WPUzjnq476NkG8Gp-cMClsVqFdNXL3X3VnY2cVzYA99ImZ4tnrH2wLUBlse-BWIC1OBI6K7iRcW050wefIsU_E6B89vAcHYwdv7yO4Vo2N6zlmfQFgqsZZvXB-kmf2ruFgb2kccJRei7tWs3Oy2jzOGexyh9OTrQPGjIbf91h2lcdQ-LrOteWTx2zE4JQ6ZT0KuaGxmdVWx96YQ54UP5we0ehwUxo7Aecm9qyFVEkpXUiqSlMCHWSTFY70-BsIKEyIXh3m8XvMPg61CtLGuv4XgjEI8OgGk-4ME_kyqeBu5XHXhQsYVwPOw",
    "Clínico Geral": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjVlODJhZmI0ZWY2OWI3NjM4MzA2OWFjNmI1N2U3ZTY1MjAzYmZlOTYiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQ2zDrW5pY28gR2VyYWwxIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2xva2ktZGV2LTQ0NDhlIiwiYXVkIjoibG9raS1kZXYtNDQ0OGUiLCJhdXRoX3RpbWUiOjE3NzU1MDU5NTEsInVzZXJfaWQiOiI4YzFjYWFmNS1jOTRlLTRiOGQtYWFjNy03MjI2MGFlYzRlZDciLCJzdWIiOiI4YzFjYWFmNS1jOTRlLTRiOGQtYWFjNy03MjI2MGFlYzRlZDciLCJpYXQiOjE3NzU1MDU5NTEsImV4cCI6MTc3NTUwOTU1MSwiZW1haWwiOiJjbGluaWNvZ2VyYWwxQG1paG1vLmNvbS5iciIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicGhvbmVfbnVtYmVyIjoiKzU1NDg5MDg2MjU0MjQiLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImNsaW5pY29nZXJhbDFAbWlobW8uY29tLmJyIl0sInBob25lIjpbIis1NTQ4OTA4NjI1NDI0Il19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.xiBvaIqLwrvWzQN20Aw2HV-Wbfh7pQv0KAiBrgnwJj9QmP_zt3dGZH5wLvt27bHFLFUTKU1FdRXJD9KeEzycZ8LPouQ-ewKHgnN3AVKH6eRmqC8VbISGnkP9Qw_uFfBkP1APsaIFwocE-46zhcXhm2r8FiPaE9drhzFGlvOwpi7_AeVPF3MM49UC9w1rQC-l-ktc9KpRjCfHUp0NImQU_A3wWPkQzgqWKY6TKwieeJfSyNNt1JHlY0CYHgMAtDtY-aRCdir3Mw60yQTvAkfVDgKSUSfqrocdhpxKMJJufH9XZuIsHz96XLWPc9b7UyXHq_UpqLZCp1MqxfG9GCkXKA",
    "Médico Trabalho": "SEU_TOKEN_MEDICO_TRABALHO",
    "Ortopedista": "SEU_TOKEN_ORTOPEDISTA",
    "Psiquiatra": "SEU_TOKEN_PSIQUIATRA"
}

def gerar_sufixo():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choices(chars, k=4))

def gerar_nome_servidor(regra):
    data = datetime.now().strftime("%Y%m%d")
    sufixo = gerar_sufixo()
    return f"TESTE_{regra}_{data}_{sufixo}"

def gerar_cpf_unico():
    # Gera CPF com dígitos verificadores válidos
    digits = [random.randint(0, 9) for _ in range(9)]
    # Primeiro dígito verificador
    s = sum((10 - i) * digits[i] for i in range(9))
    r = s % 11
    digits.append(0 if r < 2 else 11 - r)
    # Segundo dígito verificador
    s = sum((11 - i) * digits[i] for i in range(10))
    r = s % 11
    digits.append(0 if r < 2 else 11 - r)
    return ''.join(map(str, digits))

def gerar_matricula():
    return str(random.randint(10000, 99999))

def gerar_cnpj():
    nums = [random.randint(0, 9) for _ in range(14)]
    return ''.join(map(str, nums))

def gerar_setor():
    setores = ["Secretaria", "Saude", "Educacao", "Administrativo", "Infraestrutura", "Financeiro"]
    return random.choice(setores)

def gerar_cargo():
    cargos = ["Agente", "Analista", "Assistente", "Tecnico", "Coordenador", "Estagiario"]
    return random.choice(cargos)

def gerar_unidade():
    unidades = ["Unidade Central", "Sede", "Filial Norte", "Filial Sul", "Posto 01"]
    return random.choice(unidades)

def gerar_data_admissao():
    hoje = datetime.now()
    if hoje.month == 1:
        admissao = hoje.replace(year=hoje.year - 1, month=12)
    else:
        admissao = hoje.replace(month=hoje.month - 1)
    return admissao.strftime("%Y-%m-%d")

def gerar_data_hoje():
    return datetime.now().strftime("%Y-%m-%d")

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
        "days": None,
        "start_date": None,
        "attendance_id": None,
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
            "admissionDate": admission_date,
            "department": gerar_setor(),
            "jobTitle": gerar_cargo(),
            "location": gerar_unidade(),
            "cnpjLocation": gerar_cnpj(),
            "employmentCategory": "101",
            "functionalRegistration": matricula
        }]
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Criar customer [{nome}] status: {response.status_code}")
    if response.status_code == 201:
        data = safe_json(response)
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
            with open(MASSA_FILE, 'r') as ff:
                dados = json.load(ff)
            if regra in dados:
                dados[regra]["cid"] = cid
                dados[regra]["days"] = int(days)
                dados[regra]["start_date"] = start_date
                try:
                    pericia_id = safe_json(response).get("id")
                    dados[regra]["pericia_id"] = pericia_id
                except Exception:
                    pass
                with open(MASSA_FILE, 'w') as ff:
                    json.dump(dados, ff, indent=2, ensure_ascii=False)
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

def regra_existe_na_massa(regra):
    if not os.path.exists(MASSA_FILE):
        return False
    with open(MASSA_FILE, 'r') as f:
        dados = json.load(f)
    return regra in dados and dados[regra].get("pericia_id") is not None

def _buscar_detalhes_attendance(base_url, token, attendance_id):
    """Retorna (role, is_junta, board_roles) de um attendance já conhecido pelo ID."""
    url = f"{base_url}/attendance/api/scheduled-attendance/{attendance_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, False, []
    data = safe_json(response)
    # eventType contém o papel do médico (ex: "Clínico Geral")
    # roleName neste endpoint retorna o papel da clínica ("Clinica")
    role = data.get("eventType") or data.get("roleName", "")
    is_junta = data.get("medicalBoard", False)
    board_roles = [r.get("description", "") for r in (data.get("medicalBoardRoles") or [])]
    return role, is_junta, board_roles


def verificar_especialista_api(api_url, token, regra):

    if not os.path.exists(MASSA_FILE):
        raise Exception("massa_criada.json não encontrado.")

    with open(MASSA_FILE, 'r') as f:
        dados = json.load(f)

    if regra not in dados:
        raise Exception(f"SKIP: Regra '{regra}' não encontrada")

    pericia_id = dados[regra].get("pericia_id")
    nome = dados[regra].get("nome", "")
    attendance_id = None

    if not pericia_id:
        raise Exception(f"SKIP: pericia_id não encontrado para '{regra}'. Recrie a massa.")

    base_url = api_url.rsplit('/backend-nest', 1)[0]
    headers  = {"Authorization": f"Bearer {token}"}

    # Se já temos o attendance_id salvo, busca detalhes diretamente
    if attendance_id:
        role, is_junta, board_roles = _buscar_detalhes_attendance(base_url, token, attendance_id)
        if role is not None:
            print(f"Especialista (cache): roleName={role}, medicalBoard={is_junta}, attendance_id={attendance_id}")
            return role, is_junta, board_roles, attendance_id

    # Busca na fila da clínica
    fila_url = f"{base_url}/attendance/api/scheduled-attendance/clinic"
    page = 1
    max_pages = 10
    page = 1

    while page <= max_pages:
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
        data = safe_json(response)

        for grupo in data.get("items", []):
            for atendimento in grupo.get("attendances", []):
                if atendimento.get("medicalExpertReportRequestId") == pericia_id:
                    role         = atendimento.get("roleName", "")
                    is_junta     = atendimento.get("medicalBoard", False)
                    board_roles  = [r.get("description", "") for r in atendimento.get("medicalBoardRoles", [])]
                    attendance_id = atendimento.get("id", "")
                    print(f"Especialista encontrado: roleName={role}, medicalBoard={is_junta}, attendance_id={attendance_id}")
                    dados[regra]["attendance_id"] = attendance_id
                    with open(MASSA_FILE, 'w') as ff:
                        json.dump(dados, ff, indent=2, ensure_ascii=False)
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
    print(f"enviar_para_fila: {response.status_code} | {response.text[:200]}")
    if response.status_code not in (200, 201):
        # Pode já estar na fila do médico — tenta obter detalhes diretamente
        print(f"Aviso: /queue retornou {response.status_code}. Tentando obter detalhes do attendance...")
        details_url = f"{base_url}/attendance/api/scheduled-attendance/{attendance_id}"
        det = requests.get(details_url, headers=headers)
        if det.status_code == 200:
            d = det.json()
            event_type = d.get("eventType") or d.get("roleName", "")
            is_junta = d.get("medicalBoard", False)
            print(f"Attendance já na fila. eventType={event_type}, medicalBoard={is_junta}")
            return event_type, is_junta
        raise Exception(f"Erro ao enviar para fila: {response.status_code} - {response.text[:200]}")
    data = safe_json(response)
    event_type = data.get("eventType", "")
    is_junta = data.get("medicalBoard", False)
    print(f"Enviado para fila. eventType={event_type}, medicalBoard={is_junta}")
    return event_type, is_junta


# ──────────────────────────────────────────────────────────────
# HOMOLOGAÇÃO
# ──────────────────────────────────────────────────────────────

def iniciar_atendimento(base_url, token, attendance_id):
    """Inicia o atendimento (doctor starts/opens the attendance from their queue).
    Tenta POST /start, depois POST /accept, e por último PATCH com status InProgress.
    Não lança exceção — apenas loga o resultado.
    """
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    candidates = [
        ("POST",  f"{base_url}/attendance/api/scheduled-attendance/{attendance_id}/start"),
        ("POST",  f"{base_url}/attendance/api/scheduled-attendance/{attendance_id}/accept"),
        ("PATCH", f"{base_url}/attendance/api/scheduled-attendance/{attendance_id}"),
    ]
    patch_payload = {"status": "InProgress"}

    for method, url in candidates:
        try:
            if method == "POST":
                resp = requests.post(url, headers=headers, timeout=10)
            else:
                resp = requests.patch(url, json=patch_payload, headers=headers, timeout=10)

            print(f"iniciar_atendimento [{method} {url.split('/')[-1]}]: {resp.status_code}")
            if resp.status_code in (200, 201, 204):
                print(f"Atendimento iniciado via {method} {url.split('/')[-2:]}")
                return resp.status_code
        except Exception as exc:
            print(f"iniciar_atendimento erro: {exc}")

    print("iniciar_atendimento: nenhum endpoint respondeu 2xx — continuando mesmo assim.")
    return None


def criar_ficha_clinica(api_url, token, customer_id, attendance_id):
    """Cria a Ficha de HOMOLOG (registro clínico obrigatório antes de homologar)."""
    url = f"{api_url}/clinical-record"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "typeId": FICHA_HOMOLOG_TYPE_ID,
        "customerId": customer_id,
        "scheduledAttendanceId": attendance_id
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Ficha clínica: {response.status_code} | {response.text[:200]}")
    if response.status_code not in (200, 201):
        print(f"Aviso: Ficha clínica retornou {response.status_code} — pode já existir.")
    return response.status_code


def patch_validate_data(api_url, token, pericia_id, start_date, cid, days):
    """Tenta confirmar/validar dados da perícia antes de homologar.
    Experimenta múltiplos métodos e sufixos de URL; retorna o body JSON se algum
    responder 2xx, ou None se nenhum funcionar (fluxo continuará sem o PATCH).
    """
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"startDate": start_date, "cid": cid, "days": int(days)}

    base = api_url if api_url.endswith('/backend-nest') \
        else api_url.rsplit('/backend-nest', 1)[0] + '/backend-nest'

    # (método, sufixo do caminho)
    candidates = [
        ("PATCH", f"{base}/medical-expert-report-request/{pericia_id}/validate-data-requested"),
        ("PATCH", f"{base}/medical-expert-report-request/{pericia_id}/validate-data"),
        ("POST",  f"{base}/medical-expert-report-request/{pericia_id}/validate-data-requested"),
        ("POST",  f"{base}/medical-expert-report-request/{pericia_id}/validate-data"),
        ("PUT",   f"{base}/medical-expert-report-request/{pericia_id}/validate-data-requested"),
        ("PATCH", f"{base}/medical-expert-report-request/{pericia_id}"),
    ]

    for method, url in candidates:
        print(f"validate-data tentando: {method} {url}")
        print(f"  payload: {payload}")
        try:
            if method == "PATCH":
                resp = requests.patch(url, json=payload, headers=headers, timeout=15)
            elif method == "POST":
                resp = requests.post(url, json=payload, headers=headers, timeout=15)
            else:
                resp = requests.put(url, json=payload, headers=headers, timeout=15)
        except Exception as e:
            print(f"  erro de rede: {e}")
            continue

        print(f"  resposta: {resp.status_code} | {resp.text[:200]}")
        if resp.status_code in (200, 201):
            data = resp.json()
            print(f"validate-data OK via {method} {url.split('/')[-1]}")
            return data[0] if isinstance(data, list) else data

    # Nenhuma variação funcionou — retorna None para tentar continuar sem o PATCH
    print("AVISO: validate-data não encontrado em nenhuma variação — seguindo sem ele.")
    return None


def obter_detalhes_pericia(api_url, token, pericia_id):
    """Retorna detalhes da perícia incluindo registrationId e squadUserId."""
    url = f"{api_url}/medical-expert-report-request/{pericia_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erro ao obter detalhes da perícia: {response.status_code} - {response.text[:200]}")
    return safe_json(response)


def obter_customer(api_url, token, customer_id):
    """Retorna o objeto completo do customer incluindo registrations."""
    url = f"{api_url}/customer/{customer_id}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    print(f"GET customer: {resp.status_code}")
    if resp.status_code != 200:
        return {}
    return resp.json()


def obter_registration_id_do_customer(api_url, token, customer_id):
    """Busca o registrationId do customer diretamente."""
    data = obter_customer(api_url, token, customer_id)
    regs = data.get("registrations") or []
    print(f"  customer registrations: {regs}")
    if regs:
        rid = regs[0].get("registrationid") or regs[0].get("registrationId") or regs[0].get("id")
        print(f"  registration_id encontrado: {rid}")
        return rid
    return None


def obter_squad_user_do_attendance(base_url, token, attendance_id):
    """Busca o squadUserId no endpoint do attendance."""
    url = f"{base_url}/attendance/api/scheduled-attendance/{attendance_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"GET attendance: {response.status_code}")
    if response.status_code != 200:
        return None
    data = safe_json(response)
    print(f"  attendance keys: {list(data.keys())}")
    # Tenta todas as variações de campo
    for campo in ("squadUserId", "squadUser", "squad_user", "userId", "user_id",
                  "doctorId", "doctor_id", "medicId", "medic_id"):
        val = data.get(campo)
        if val:
            print(f"  squad_user_id via '{campo}': {val}")
            if isinstance(val, dict):
                return val.get("id") or val.get("squadUserId")
            return val
    print(f"  AVISO: squad_user_id não encontrado. Campos disponíveis: {list(data.keys())}")
    return None


def obter_memed_token(api_url, token, squad_user_id):
    """Obtém o JWT do Memed para o médico responsável."""
    base = api_url.rsplit('/backend-nest', 1)[0]
    url = f"{base}/backend-nest/memed/memed-token/{squad_user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erro ao obter token Memed: {response.status_code} - {response.text[:200]}")
    memed_token = safe_json(response).get("token")
    print(f"Token Memed obtido para squadUser {squad_user_id}")
    return memed_token


def obter_primeiro_artigo(api_url, token, pericia_id, cid=None):
    """Retorna (article_id, article_name) do primeiro artigo aplicável.
    Tenta vários endpoints possíveis; retorna (None, '') se nenhum funcionar.
    """
    base = api_url if api_url.endswith('/backend-nest') \
        else api_url.rsplit('/backend-nest', 1)[0] + '/backend-nest'
    headers = {"Authorization": f"Bearer {token}"}

    candidates = [
        f"{base}/medical-expert-report-request/{pericia_id}/Accepted",
        f"{base}/medical-expert-report-request/{pericia_id}/articles",
        f"{base}/medical-expert-report-request/{pericia_id}/article",
        f"{base}/article?medicalExpertReportRequestId={pericia_id}&status=Accepted",
        f"{base}/article?status=Accepted",
        f"{base}/article",
    ]
    if cid:
        candidates.insert(4, f"{base}/article?cid={cid}&status=Accepted")

    for url in candidates:
        print(f"Buscando artigos: GET {url}")
        resp = requests.get(url, headers=headers)
        print(f"  status: {resp.status_code} | {resp.text[:120]}")
        if resp.status_code == 200:
            try:
                data = resp.json()
            except Exception:
                continue
            # Pode vir como lista ou como dict com campo items/data
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = data.get("items") or data.get("data") or data.get("articles") or []
            else:
                items = []
            if items:
                article_id   = items[0].get("id")
                article_name = items[0].get("article") or items[0].get("name") or items[0].get("description") or ""
                print(f"  Artigo encontrado: {article_name} ({article_id})")
                return article_id, article_name

    print("AVISO: nenhum artigo encontrado — prosseguindo com articleId=None.")
    return None, ""


def criar_prescricao_memed(memed_token, customer_id, customer_name, cpf,
                           cid, days, start_date, observations):
    """Cria a prescrição no Memed e retorna o memedFileId."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = start + timedelta(days=int(days) - 1)
    start_br = start.strftime("%d/%m/%Y")
    end_br = end.strftime("%d/%m/%Y")
    prescription_uuid = str(_uuid.uuid4())

    posologia = (
        f"<strong>PARECER MEDICO</strong><br><br>"
        f"- Parecer: Aceito<br>"
        f"- CID: {cid}<br>"
        f"- Data de início: {start_br}<br>"
        f"- Número de dias: {days}<br>"
        f"- Data Fim: {end_br}<br><br>"
        f"<p><strong>Observações:</strong></p><br>{observations}"
    )

    payload = {
    "data": {
        "type": "prescricoes",
        "attributes": {
            "paciente": {
                "nome_atualizado": customer_name,
                "idExterno": customer_id,
                "nome": customer_name,
                "cpf": cpf,
                "data_nascimento": "01/01/1990",
                "telefone": "",
                "external_id": customer_id
            },
            "screening": {
                "total": 0,
                "status": "success"
            },
            "workplace": "",
            "prescriptionDate": start_br,
            "prescriptionUuid": prescription_uuid,
            "medicamentos": [
                {
                    "nome": f"Atestado CID {cid}",
                    "posologia": posologia,
                    "isFromCommand": True,
                    "tipo": "custom",
                    "descontinuado": False,
                    "status": "",
                    "categoria_posologia": "",
                    "quantidade": "",
                    "composicao": "",
                    "fabricante": "",
                    "titularidade": "",
                    "preco": 0,
                    "anamnese": "",
                    "cid_id": "",
                    "data_solicitacao": "",
                    "descricao_tratamento": "",
                    "quantidade_mes_1": "",
                    "quantidade_mes_2": "",
                    "quantidade_mes_3": "",
                    "quantidade_mes_4": ""
                }
            ]
        }
    }
}

    headers = {
    "Authorization": f"Bearer {memed_token}",
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/json"
}
    url = f"https://api.memed.com.br/v1/prescricoes?_={int(time.time() * 1000)}"
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code not in (200, 201):
        raise Exception(f"Erro Memed prescricoes: {response.status_code} - {response.text[:300]}")
    memed_file_id = safe_json(response).get("data", {}).get("id")
    print(f"Prescrição Memed criada: memedFileId={memed_file_id}")
    return memed_file_id

def gerar_memed_file_mihmo(api_url, token, attendance_id, pericia_id,
                            registration_id, memed_file_id, memed_token,
                            days, cid, start_date, observations, article_id):
    """Finaliza a homologação no Mihmo via generate-memed-file. Retorna status."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = start + timedelta(days=int(days) - 1)
    calculate_end_date = end.strftime("%d/%m/%Y")

    base = api_url.rsplit('/backend-nest', 1)[0]
    url = f"{base}/backend-nest/memed/generate-memed-file"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "scheduledAttendanceId": attendance_id,
        "medicalExpertReportRequestId": pericia_id,
        "type": "MedicalExpertReportRequest",
        "registrationId": registration_id,
        "memedFileId": memed_file_id,
        "token": memed_token,
        "status": "Accepted",
        "days": int(days),
        "cid": cid,
        "startDate": start_date,
        "calculateEndDate": calculate_end_date,
        "observations": observations,
    }
    if article_id:
        payload["articleId"] = article_id
    print(f"generate-memed-file payload: {json.dumps(payload, indent=2)}")
    response = requests.post(url, json=payload, headers=headers)
    print(f"generate-memed-file: {response.status_code} | {response.text[:300]}")
    if response.status_code not in (200, 201):
        raise Exception(f"Erro generate-memed-file: {response.status_code} - {response.text[:300]}")
    status = safe_json(response).get("status", "")
    print(f"Homologação concluída. Status: {status}")
    return status


def homologar_pericia(api_url, token, regra):
    """
    Orquestra o fluxo completo de homologação:
    1. Cria Ficha de HOMOLOG
    2. PATCH validate-data-requested (desbloqueia artigos e popula registration)
    3. Busca registrationId e squadUserId
    4. Busca artigo CID aplicável (GET /Accepted)
    5. Obtém token Memed
    6. Cria prescrição no Memed
    7. Salva homologação no Mihmo (generate-memed-file)
    Retorna o status final ("Accepted").
    """
    if not os.path.exists(MASSA_FILE):
        raise Exception("massa_criada.json não encontrado.")
    with open(MASSA_FILE, 'r') as f:
        dados = json.load(f)
    if regra not in dados:
        raise Exception(f"Regra '{regra}' não encontrada no massa_criada.json.")

    entrada = dados[regra]
    pericia_id    = entrada.get("pericia_id")

    token_clinica = TOKENS["CLINICA"]

    role, is_junta, board_roles, attendance_id = verificar_especialista_api(
        api_url, token_clinica, regra
    )

    if not attendance_id:
        raise Exception(f"attendance_id não encontrado para regra {regra}")

    enviar_para_fila(api_url, token_clinica, attendance_id)

    token_medico = TOKENS.get(role)

    if not token_medico:
        raise Exception(f"Token não encontrado para role '{role}'")

    if not attendance_id:
        _, _, _, attendance_id = verificar_especialista_api(api_url, token_clinica, regra)

    if not attendance_id:
        raise Exception(f"attendance_id inválido para regra {regra}")
    
    cid           = entrada.get("cid")
    days          = entrada.get("days")
    customer_id   = entrada.get("customer_id")
    customer_name = entrada.get("nome")
    cpf           = entrada.get("cpf")
    start_date    = entrada.get("start_date") or gerar_data_hoje()
    observations  = "Teste automatizado"

    if not all([pericia_id, attendance_id, cid, days, customer_id]):
        raise Exception(
            f"Dados incompletos para '{regra}'. "
            f"pericia_id={pericia_id}, attendance_id={attendance_id}, "
            f"cid={cid}, days={days}"
        )

    base_url = api_url.rsplit('/backend-nest', 1)[0]

    iniciar_atendimento(base_url, token_medico, attendance_id)
    criar_ficha_clinica(api_url, token_medico, customer_id, attendance_id)
    pericia_data = patch_validate_data(
        api_url, token_medico, pericia_id, start_date, cid, days
    )

    def _extrair_registration_id(data):
        if not data:
            return None
        reg = data.get("registration")
        if reg:
            rid = reg.get("registrationid") or reg.get("id")
            if rid:
                return rid
        regs = (data.get("customer") or {}).get("registrations") or data.get("registrations") or []
        if regs:
            return regs[0].get("registrationid") or regs[0].get("id")
        return None

    # 3a. registration_id — tenta em cascata: PATCH response → GET péricia → GET customer
    registration_id = _extrair_registration_id(pericia_data)
    if not registration_id:
        details = obter_detalhes_pericia(api_url, token_medico, pericia_id)
        registration_id = obter_registration_id_do_customer(api_url, token_medico, customer_id)
    if not registration_id:
        print("registration_id não veio do GET péricia — buscando via GET customer...")
        registration_id = obter_registration_id_do_customer(api_url, token_medico, customer_id)
    print(f"registration_id={registration_id}")
    if not registration_id:
        raise Exception(
            f"registration_id não encontrado para '{regra}'. "
            f"Verifique se o customer '{customer_id}' tem matrícula cadastrada."
        )

    # 3b. squad_user_id — attendance endpoint (com debug completo)
    squad_user_id = obter_squad_user_do_attendance(base_url, token_medico, attendance_id)
    if not squad_user_id and pericia_data:
        for campo in ("squad_user", "squadUser", "userId"):
            sq = pericia_data.get(campo)
            if sq:
                squad_user_id = sq.get("id") if isinstance(sq, dict) else sq
                break
    if not squad_user_id:
        try:
            det2 = obter_detalhes_pericia(api_url, token_medico, pericia_id)
            print(f"  GET péricia (2ª vez) keys: {list(det2.keys())}")
            for campo in ("squad_user", "squadUser", "userId", "squadUserId"):
                sq2 = det2.get(campo)
                if sq2:
                    squad_user_id = sq2.get("id") if isinstance(sq2, dict) else sq2
                    print(f"  squad_user_id via péricia['{campo}']: {squad_user_id}")
                    break
        except Exception:
            pass
    print(f"squad_user_id={squad_user_id}")
    if not squad_user_id:
        raise Exception(
            f"squad_user_id não encontrado para '{regra}'. "
            f"Verifique se o attendance '{attendance_id}' tem médico atribuído."
        )

    # 4. Artigo CID
    article_id, article_name = obter_primeiro_artigo(api_url, token_medico, pericia_id, cid=cid)

    # 4. Token Memed
    memed_token = obter_memed_token(api_url, token_medico, squad_user_id)

    # 5. Prescrição Memed
    memed_file_id = criar_prescricao_memed(
        memed_token, customer_id, customer_name, cpf,
        cid, days, start_date, observations
    )

    # 6. Finaliza no Mihmo
    status = gerar_memed_file_mihmo(
        api_url, token_medico, attendance_id, pericia_id,
        registration_id, memed_file_id, memed_token,
        days, cid, start_date, observations, article_id
    )
    return status

def safe_json(response):
    if response.status_code == 204:
        return None

    if not response.text:
        raise Exception(f"Response vazia! Status: {response.status_code}")

    try:
        return json.loads(response.text)  # 🔥 NÃO usa response.json()
    except Exception:
        raise Exception(
            f"Response inválida!\nStatus: {response.status_code}\nBody:\n{response.text[:500]}"
        )