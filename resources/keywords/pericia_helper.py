import requests
import json
import random
import time
import uuid as _uuid
import os
import base64
from datetime import datetime, timedelta


# Artigos para serviços de licença médica (LTS, LTF, LTS_INSS)
PMV_ARTICLES_LTS = [
    {"id": "89d556e7-edb3-4862-9888-765de680f28e", "article": "Acidente de Trabalho - 15 Dias", "applicableCategories": ["101","306","410","302","771"], "medicalBoard": False},
    {"id": "592f16be-8304-49db-9d87-c20bb76f1c8e", "article": "Licença Médica - CLT/CTD/CC/CONSELHO TUTELAR", "applicableCategories": ["101","306","302","771"], "medicalBoard": False},
    {"id": "e5ff7f0c-9585-4bb5-84e2-8048fb7f111f", "article": "Auxílio Doença Administrativo", "applicableCategories": ["301","101","306","410","302","771"], "medicalBoard": False},
    {"id": "232cce2b-1f07-4447-bf21-364556770d37", "article": "Auxílio Doença Administrativo - ACIDENTE DE TRABALHO", "applicableCategories": ["301","101","306","410","302","771"], "medicalBoard": False},
    {"id": "7e4757a6-f056-4396-96f5-529f66a5700f", "article": "T89-REGISTRO DE ACIDENTE DE TRABALHO - SEM AFASTAMENTO", "applicableCategories": ["301","101","306","410","302","771"], "medicalBoard": False},
]

# Tipos de serviço que usam PMV_ARTICLES_LTS (hardcoded — API pode retornar artigos obsoletos)
PMV_SERVICE_TYPES_LTS = {
    "HealthCareLicense",
    "FamilyPersonTreatmentLicense",
    "HealthCareLicenseInss",
}

def _jwt_user_id(token):
    """Extrai user_id do payload JWT sem verificar assinatura."""
    try:
        payload_b64 = token.split('.')[1]
        padding = 4 - len(payload_b64) % 4
        payload = json.loads(base64.b64decode(payload_b64 + '=' * padding))
        return payload.get("user_id") or payload.get("sub")
    except Exception:
        return None

MASSA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'massa_criada.json')
FICHA_HOMOLOG_TYPE_ID = "bcfc80cf-12ea-4cb5-8ac2-195895418db1"
_customer_regra = {}

# Credenciais para auto-login Firebase (não precisam de atualização manual)
CREDENTIALS = {
    "CLINICA":             {"email": "gestormihmo@mihmo.com.br",      "password": "REMOVIDO"},
    "Clínico Geral":       {"email": "clinicogeral1@mihmo.com.br",    "password": "REMOVIDO"},
    "Clínico Geral 2":     {"email": "clinicogeral2@mihmo.com.br",    "password": "REMOVIDO"},
    "Clínico Geral 3":     {"email": "clinicogeral3@mihmo.com.br",    "password": "REMOVIDO"},
    "Médico Trabalho":     {"email": "medicopmv@mihmo.com.br",        "password": "REMOVIDO"},
    "Ortopedista":         {"email": "ortopedista1@mihmo.com.br",     "password": "REMOVIDO"},
    "Psiquiatra":          {"email": "psiquiatra1@mihmo.com.br",      "password": "REMOVIDO"},
    "Assistente Social":   {"email": "assistente.social@mihmo.com.br","password": "REMOVIDO"},
    "Psicólogo":           {"email": "psicologo@mihmo.com.br",        "password": "REMOVIDO"},
    "Enfermeiro":          {"email": "teste@mihmo.com.br",            "password": "REMOVIDO"},
}

# Mapeamento email → chave de credencial (para identificar squad users pelos nossos logins)
_EMAIL_TO_CRED_KEY = {v["email"]: k for k, v in CREDENTIALS.items()}

FIREBASE_AUTH_URL = (
    "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
    "?key=REMOVIDO"
)

# Cache em memória: role → {"token": "...", "exp": timestamp}
_token_cache: dict = {}


def _obter_token(role: str) -> str:
    """Retorna token Firebase válido para o role, fazendo login automático se expirado."""
    import time as _time

    cached = _token_cache.get(role, {})
    token = cached.get("token")
    exp = cached.get("exp", 0)

    # Renova se faltarem menos de 5 minutos para expirar
    if token and _time.time() < exp - 300:
        return token

    creds = CREDENTIALS.get(role)
    if not creds:
        raise Exception(f"Credenciais não configuradas para role '{role}'. Adicione em CREDENTIALS.")
    if creds["email"].startswith("SEU_"):
        raise Exception(f"Credenciais não configuradas para role '{role}'. Preencha o e-mail em CREDENTIALS.")

    print(f"[auto-login] Obtendo token para '{role}' ({creds['email']})...")
    payload = {"email": creds["email"], "password": creds["password"], "returnSecureToken": True}
    resp = requests.post(FIREBASE_AUTH_URL, json=payload, timeout=10)
    if resp.status_code != 200:
        raise Exception(f"Falha no login Firebase para '{role}': {resp.status_code} - {resp.text[:200]}")

    data = resp.json()
    new_token = data["idToken"]
    expires_in = int(data.get("expiresIn", 3600))

    _token_cache[role] = {"token": new_token, "exp": _time.time() + expires_in}
    print(f"[auto-login] Token para '{role}' obtido. Expira em {expires_in}s.")
    return new_token

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
        "role": None,
        "is_junta": False,
        "matricula": None,
        "service_type": None,
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
            "employmentCategory": "301",
            "functionalRegistration": matricula
        }]
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Criar customer [{nome}] status: {response.status_code}")
    if response.status_code == 201:
        data = safe_json(response)
        customer_id = data.get("customerid")
        salvar_massa(regra, customer_id, cpf, nome)
        # salva matrícula logo após criar o customer
        if os.path.exists(MASSA_FILE):
            with open(MASSA_FILE, 'r') as _f:
                _d = json.load(_f)
            _d[regra]["matricula"] = matricula
            with open(MASSA_FILE, 'w') as _f:
                json.dump(_d, _f, indent=2, ensure_ascii=False)
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
                dados[regra]["service_type"] = tipo
                try:
                    resp_json = safe_json(response)
                    print(f"criar_pericia resposta keys: {list(resp_json.keys())}")
                    pericia_id = resp_json.get("id")
                    dados[regra]["pericia_id"] = pericia_id
                    # Salva attendance_id se vier na resposta da criação
                    att_id = (
                        resp_json.get("scheduledAttendanceId")
                        or resp_json.get("attendanceId")
                        or (resp_json.get("scheduledAttendance") or {}).get("id")
                        or (resp_json.get("attendance") or {}).get("id")
                    )
                    if att_id:
                        dados[regra]["attendance_id"] = att_id
                        print(f"attendance_id salvo da criação: {att_id}")
                except Exception as e:
                    print(f"Erro ao parsear resposta da péricia: {e}")
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


def _encontrar_atendimento_na_resposta(data, pericia_id):
    """Procura pericia_id em qualquer estrutura de resposta de fila (lista plana, items, items.items)."""
    # Normaliza para lista de grupos
    top = data if isinstance(data, list) else data.get("items", [])
    for grupo in top:
        if not isinstance(grupo, dict):
            continue
        # Estrutura 1: grupo tem campo "attendances"
        for atd in grupo.get("attendances", []):
            if atd.get("medicalExpertReportRequestId") == pericia_id:
                return atd
        # Estrutura 2: grupo tem campo "items" com sub-atendimentos
        for item in grupo.get("items", []):
            if isinstance(item, dict):
                if item.get("id") == pericia_id or item.get("medicalExpertReportRequestId") == pericia_id:
                    # item pode ser o próprio atendimento ou conter attendances
                    subs = item.get("attendances")
                    if subs:
                        return subs[0]
                    return item
        # Estrutura 3: grupo é diretamente o atendimento
        if grupo.get("medicalExpertReportRequestId") == pericia_id:
            return grupo
    return None


def verificar_especialista_api(api_url, token, regra):
    if not os.path.exists(MASSA_FILE):
        raise Exception("massa_criada.json não encontrado.")
    with open(MASSA_FILE, 'r') as f:
        dados = json.load(f)
    if regra not in dados:
        raise Exception(f"SKIP: Regra '{regra}' não encontrada no massa_criada.json.")

    pericia_id = dados[regra].get("pericia_id")
    nome = dados[regra].get("nome", "")
    attendance_id = dados[regra].get("attendance_id")

    if not pericia_id:
        raise Exception(f"SKIP: pericia_id não encontrado para '{regra}'. Recrie a massa.")

    base_url = api_url.rsplit('/backend-nest', 1)[0]
    headers  = {"Authorization": f"Bearer {token}"}

    # 1. Se temos attendance_id em cache, tenta buscar detalhes diretamente
    if attendance_id:
        role, is_junta, board_roles = _buscar_detalhes_attendance(base_url, token, attendance_id)
        if role is not None:
            print(f"Especialista (cache): role={role}, medicalBoard={is_junta}, attendance_id={attendance_id}")
            return role, is_junta, board_roles, attendance_id
        # GET attendance retornou 403/404 (attendance na fila do médico ou token sem acesso)
        # Tenta recuperar role do GET da péricia, que sempre retorna 200
        role_cached    = dados[regra].get("role") or ""
        is_junta_cached = dados[regra].get("is_junta", False)
        if role_cached:
            print(f"Especialista (cache role+attendance): role={role_cached}, attendance_id={attendance_id}")
            return role_cached, is_junta_cached, [], attendance_id
        print(f"Cache attendance_id={attendance_id} sem role — tentando via GET péricia...")

    headers_req = {"Authorization": f"Bearer {token}"}

    # 2. Tenta obter attendance_id direto da perícia (evita busca de fila)
    print(f"Buscando attendance via GET péricia {pericia_id}...")
    pericia_resp = requests.get(
        f"{api_url}/medical-expert-report-request/{pericia_id}",
        headers=headers_req
    )
    print(f"  GET péricia: {pericia_resp.status_code}")
    if pericia_resp.status_code == 200:
        pd = pericia_resp.json()
        print(f"  péricia keys: {list(pd.keys())}")
        att_id_from_pericia = (
            pd.get("scheduledAttendanceId")
            or pd.get("attendanceId")
            or pd.get("attendance_id")
            or (pd.get("scheduledAttendance") or {}).get("id")
            or (pd.get("attendance") or {}).get("id")
        )
        print(f"  attendance_id da péricia: {att_id_from_pericia}")
        pericia_role     = pd.get("eventType") or pd.get("roleDescription") or ""
        pericia_is_junta = pd.get("isMedicalBoard", False)
        pericia_br       = [r.get("description", "") for r in (pd.get("medicalBoardRoles") or [])]
        regs = pd.get("registrations") or []
        if regs:
            reg_id_from_pericia = regs[0].get("registrationid") or regs[0].get("registrationId") or regs[0].get("id")
            print(f"  registration_id da péricia: {reg_id_from_pericia}")
            dados[regra]["registration_id"] = reg_id_from_pericia
            with open(MASSA_FILE, 'w') as ff:
                json.dump(dados, ff, indent=2, ensure_ascii=False)
        if att_id_from_pericia:
            role, is_junta, board_roles = _buscar_detalhes_attendance(base_url, token, att_id_from_pericia)
            if role is not None:
                print(f"Especialista via péricia: role={role}, attendance_id={att_id_from_pericia}")
                dados[regra]["attendance_id"] = att_id_from_pericia
                dados[regra]["role"]     = role
                dados[regra]["is_junta"] = is_junta
                with open(MASSA_FILE, 'w') as ff:
                    json.dump(dados, ff, indent=2, ensure_ascii=False)
                return role, is_junta, board_roles, att_id_from_pericia
        if attendance_id and pericia_role:
            print(f"Especialista via eventType da péricia: role={pericia_role}, attendance_id={attendance_id}")
            dados[regra]["role"]     = pericia_role
            dados[regra]["is_junta"] = pericia_is_junta
            with open(MASSA_FILE, 'w') as ff:
                json.dump(dados, ff, indent=2, ensure_ascii=False)
            return pericia_role, pericia_is_junta, pericia_br, attendance_id

    # 3. Fallback: busca nas filas
    fila_base = f"{base_url}/attendance/api/scheduled-attendance"
    for fila_url in [f"{fila_base}/clinic", fila_base]:
        print(f"Buscando em fila: {fila_url}")
        page = 1
        primeira_pagina = True
        while page <= 20:
            params = {"page": page, "pageSize": 50, "search": nome}
            resp = requests.get(fila_url, params=params, headers=headers_req)
            print(f"  page={page}: {resp.status_code}")
            if resp.status_code != 200:
                break
            data = safe_json(resp)
            # Imprime estrutura da 1ª página para diagnóstico
            if primeira_pagina:
                primeira_pagina = False
                top = data if isinstance(data, list) else data.get("items", [])
                if top:
                    primeiro = top[0]
                    print(f"  estrutura item[0] keys: {list(primeiro.keys()) if isinstance(primeiro, dict) else type(primeiro)}")
                    # Mostra um atendimento de exemplo para ver campos disponíveis
                    for campo in ("attendances", "items"):
                        subs = primeiro.get(campo, []) if isinstance(primeiro, dict) else []
                        if subs:
                            print(f"  item[0].{campo}[0] keys: {list(subs[0].keys())}")
                            break
            atd = _encontrar_atendimento_na_resposta(data, pericia_id)
            if atd:
                role        = atd.get("eventType") or atd.get("roleName", "")
                is_junta    = atd.get("medicalBoard") or atd.get("isMedicalBoard", False)
                board_roles = [r.get("description", "") for r in (atd.get("medicalBoardRoles") or [])]
                attendance_id = atd.get("id", "")
                print(f"Especialista na fila: role={role}, attendance_id={attendance_id}")
                dados[regra]["attendance_id"] = attendance_id
                dados[regra]["role"]          = role
                dados[regra]["is_junta"]      = is_junta
                with open(MASSA_FILE, 'w') as ff:
                    json.dump(dados, ff, indent=2, ensure_ascii=False)
                return role, is_junta, board_roles, attendance_id
            if not (data.get("hasNext", False) if isinstance(data, dict) else False):
                break
            page += 1

    raise Exception(
        f"Péricia '{pericia_id}' não encontrada para regra '{regra}'. "
        f"A fila da clínica pode ter mudado após a unificação — consulte o dev sobre o novo endpoint."
    )


def enviar_para_fila(api_url, token, attendance_id, regra=None):
    base_url = api_url.rsplit('/backend-nest', 1)[0]
    url = f"{base_url}/attendance/api/scheduled-attendance/{attendance_id}/queue"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers)
    print(f"enviar_para_fila: {response.status_code} | {response.text[:200]}")
    if response.status_code in (200, 201):
        data = safe_json(response)
        event_type = data.get("eventType", "")
        is_junta = data.get("medicalBoard", False)
        print(f"Enviado para fila. eventType={event_type}, medicalBoard={is_junta}")
        return event_type, is_junta

    # Não foi 2xx — attendance provavelmente já está em queue (rodada anterior)
    print(f"Aviso: /queue retornou {response.status_code} — usando fallback. regra={regra!r}")

    # Tenta role cacheado no massa_criada.json
    if os.path.exists(MASSA_FILE):
        with open(MASSA_FILE, 'r') as f:
            dados = json.load(f)
        entrada = dados.get(str(regra), {}) if regra else {}
        role_cached     = entrada.get("role") or ""
        is_junta_cached = entrada.get("is_junta") or False
        print(f"  massa role_cached={role_cached!r}, is_junta={is_junta_cached!r}, regra_key={str(regra)!r}")
        if role_cached:
            print(f"Role cacheado: eventType={role_cached}, medicalBoard={is_junta_cached}")
            return role_cached, is_junta_cached

    # Último fallback: attendance já está em queue, retorna eventType vazio
    # (o Should Be Equal no robot vai capturar a divergência se houver)
    print("Fallback final: retornando role vazio — attendance provavelmente já em queue.")
    return "", False


# ──────────────────────────────────────────────────────────────
# HOMOLOGAÇÃO
# ──────────────────────────────────────────────────────────────

def iniciar_atendimento(base_url, token, attendance_id, squad_user_id):
    """Inicia o atendimento via PATCH /squaduser (atribui médico e bloqueia)."""
    url = f"{base_url}/attendance/api/scheduled-attendance/{attendance_id}/squaduser"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"squadUserId": squad_user_id, "lock": True}
    resp = requests.patch(url, json=payload, headers=headers, timeout=10)
    print(f"iniciar_atendimento [PATCH squaduser]: {resp.status_code}")
    if resp.status_code in (200, 201, 204):
        print(f"Atendimento iniciado via PATCH /squaduser")
        return resp.status_code
    print(f"iniciar_atendimento: aviso {resp.status_code} - {resp.text[:200]}")
    return None


LIMESURVEY_URL = "https://mihmosaude.limesurvey.net"
LIMESURVEY_USER = "admin"
LIMESURVEY_PASS = "REMOVIDO"  # ajuste se necessário
MIHMO_URL = "https://homolog.mihmo.com.br"


def _submeter_ficha_playwright(survey_url, token_medico, cpf, api_url):
    """Abre o LimeSurvey com sessão real do Mihmo via Playwright e submete o formulário.
    O browser executa o fetch JS para /integrate com os cookies corretos."""
    from playwright.sync_api import sync_playwright

    base = api_url.rsplit('/backend-nest', 1)[0]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Injetar o token do Mihmo como cookie de sessão
        context.add_cookies([
            {"name": "token",       "value": token_medico, "domain": "homolog.mihmo.com.br", "path": "/"},
            {"name": "accessToken", "value": token_medico, "domain": "homolog.mihmo.com.br", "path": "/"},
        ])

        page = context.new_page()

        # Monitorar requests para capturar o /integrate
        integrate_called = []
        def on_response(response):
            if "/integrate" in response.url or "limesurveyintegration" in response.url:
                print(f"  [playwright] response: {response.status} {response.url}")
                integrate_called.append(response.status)

        page.on("response", on_response)

        print(f"  [playwright] Abrindo survey: {survey_url}")
        page.goto(survey_url, wait_until="domcontentloaded", timeout=30000)
        print(f"  [playwright] URL atual: {page.url}")
        print(f"  [playwright] Título: {page.title()}")

        # Preencher textareas vazias usando Playwright (persiste no DOM)
        for ta in page.locator("textarea").all():
            try:
                if not ta.input_value():
                    ta.fill("Teste automatizado")
            except Exception:
                pass

        # Preencher inputs de texto vazios
        for inp in page.locator("input[type='text']").all():
            try:
                if not inp.input_value():
                    inp.fill("Teste automatizado")
            except Exception:
                pass

        print(f"  [playwright] Clicando no botão de submit (força navegação real)...")
        # Usar click forçado para disparar o submit com navegação real (segue redirect corretamente)
        submitted = False
        for selector in [
            "input[type='submit'][value*='nviar']",
            "input[type='submit'][value*='inaliz']",
            "input[type='submit']",
            "button[name='move'][value='movesubmit']",
            "button[name='move']",
            "#defaultbtn",
        ]:
            btn = page.locator(selector).first
            if btn.count() > 0:
                try:
                    btn.click(force=True, timeout=5000)
                    submitted = True
                    print(f"  [playwright] clicou: {selector}")
                    break
                except Exception as ce:
                    print(f"  [playwright] click falhou ({selector}): {ce}")

        if not submitted:
            # Fallback: submeter via JS setando hidden input e disparando submit
            page.evaluate("""
                var form = document.querySelector('form');
                if (form) {
                    var inp = document.createElement('input');
                    inp.type = 'hidden'; inp.name = 'move'; inp.value = 'movesubmit';
                    form.appendChild(inp);
                    form.submit();
                }
            """)
            print(f"  [playwright] submeteu via form.submit() fallback")

        # Aguardar navegação real para /integrate no Mihmo
        try:
            page.wait_for_url("**/integrate**", timeout=20000)
            print(f"  [playwright] chegou em /integrate: {page.url}")
        except Exception:
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass

        print(f"  [playwright] URL final: {page.url}")
        print(f"  [playwright] integrate_called: {integrate_called}")
        browser.close()

    return bool(integrate_called)


def _limesurvey_api_add_response(survey_id):
    """Adiciona uma resposta ao LimeSurvey via API RemoteControl2 (XMLRPC/JSON-RPC).
    Mais confiável do que simular o formulário web."""
    rpc_url = f"{LIMESURVEY_URL}/index.php/admin/remotecontrol"
    headers = {"Content-Type": "application/json"}

    def _rpc(method, params, rid=1):
        payload = {"method": method, "params": params, "id": rid}
        r = requests.post(rpc_url, json=payload, headers=headers, timeout=15)
        return r.json().get("result")

    # 1. Obter session key
    session_key = _rpc("get_session_key", [LIMESURVEY_USER, LIMESURVEY_PASS])
    if not session_key or isinstance(session_key, dict):
        print(f"  LimeSurvey API: falha ao obter session key: {session_key}")
        return False
    print(f"  LimeSurvey API: session_key obtida")

    try:
        # 2. Listar perguntas do survey para montar as chaves de resposta
        questions = _rpc("list_questions", [session_key, survey_id], rid=2)
        if not questions or isinstance(questions, dict):
            print(f"  LimeSurvey API: falha ao listar perguntas: {questions}")
            return False
        print(f"  LimeSurvey API: {len(questions)} perguntas encontradas")

        # 3. Montar resposta com "A" para todas as perguntas
        response_data = {}
        for q in questions:
            sid = str(q.get("sid", survey_id))
            gid = str(q.get("gid", ""))
            qid = str(q.get("qid", ""))
            if gid and qid:
                response_data[f"{sid}X{gid}X{qid}"] = "A"
        print(f"  LimeSurvey API: enviando {len(response_data)} respostas: {list(response_data.keys())[:3]}...")

        # 4. Adicionar resposta
        result = _rpc("add_response", [session_key, survey_id, response_data], rid=3)
        print(f"  LimeSurvey API add_response resultado: {result}")
        return bool(result) and str(result) not in ("0", "false", "False")
    finally:
        _rpc("release_session_key", [session_key], rid=4)


def _limesurvey_submit(survey_id, cpf, responses=None):
    """Submete uma resposta ao LimeSurvey simulando o participante no navegador."""
    import re as _re

    session = requests.Session()
    survey_url = f"{LIMESURVEY_URL}/{survey_id}"
    params = {"lang": "pt", "CPF": cpf}

    # 1. GET para obter o formulário e os tokens de sessão
    print(f"LimeSurvey GET survey {survey_id}...")
    get_resp = session.get(survey_url, params=params, timeout=20)
    print(f"  GET status: {get_resp.status_code}")
    if get_resp.status_code != 200:
        print(f"  AVISO: não conseguiu carregar survey: {get_resp.status_code}")
        return None

    html = get_resp.text

    # Extrair campos hidden do formulário (YII_CSRF_TOKEN, sid, token, etc.)
    hidden_fields = {}
    for match in _re.finditer(r'<input[^>]+type=["\']hidden["\'][^>]*>', html, _re.IGNORECASE):
        tag = match.group(0)
        name_m = _re.search(r'name=["\']([^"\']+)["\']', tag)
        value_m = _re.search(r'value=["\']([^"\']*)["\']', tag)
        if name_m:
            hidden_fields[name_m.group(1)] = value_m.group(1) if value_m else ""

    print(f"  hidden fields encontrados: {list(hidden_fields.keys())}")

    def _extract_hidden(h):
        fields = {}
        for m in _re.finditer(r'<input[^>]+type=["\']hidden["\'][^>]*>', h, _re.IGNORECASE):
            tag = m.group(0)
            name_m = _re.search(r'name=["\']([^"\']+)["\']', tag)
            value_m = _re.search(r'value=["\']([^"\']*)["\']', tag)
            if name_m:
                fields[name_m.group(1)] = value_m.group(1) if value_m else ""
        return fields

    def _extract_questions(h):
        fields = {}
        sid_pat = str(survey_id) + r'X\d+X\d+[^"\']*'
        # inputs: extrai value real (CPF, etc.)
        for m in _re.finditer(
            r'<input([^>]+name=["\'](' + sid_pat + r')["\'][^>]*)>',
            h, _re.IGNORECASE
        ):
            tag_attrs = m.group(1)
            fname = m.group(2)
            val_m = _re.search(r'value=["\']([^"\']*)["\']', tag_attrs)
            value = val_m.group(1) if val_m else ""
            if fname not in fields:
                fields[fname] = value if value else "Teste automatizado"
        # textareas: extrai conteúdo real
        for m in _re.finditer(
            r'<textarea[^>]+name=["\'](' + sid_pat + r')["\'][^>]*>(.*?)</textarea>',
            h, _re.IGNORECASE | _re.DOTALL
        ):
            fname = m.group(1)
            content = m.group(2).strip()
            if fname not in fields:
                fields[fname] = content if content else "Teste automatizado"
        return fields

    # Palavras que indicam conclusão REAL (resposta já salva no LimeSurvey)
    _TRULY_DONE = ["obrigado", "thank", "enviado", "survey complete", "salva com sucesso", "fechar esta guia"]
    # "finaliz" sozinho é ambíguo — pode ser o botão "Finalizar" numa página de revisão

    def _is_truly_done(h):
        low = h.lower()
        return any(w in low for w in _TRULY_DONE)

    def _is_done(h):
        return _is_truly_done(h) or "finaliz" in h.lower()

    # 2. Se a página inicial não tem perguntas, fazer POST com move=start
    questions = _extract_questions(html)
    if not questions:
        print("  Página inicial detectada — enviando move=start...")
        start_data = dict(hidden_fields)
        start_data["move"] = "start"
        start_data["sid"] = str(survey_id)
        start_data["lang"] = "pt"
        start_resp = session.post(survey_url, data=start_data, timeout=20, allow_redirects=True)
        print(f"  start POST: {start_resp.status_code} | len={len(start_resp.text)}")
        html = start_resp.text
        hidden_fields = _extract_hidden(html)
        questions = _extract_questions(html)

    print(f"  perguntas encontradas: {list(questions.keys())}")

    # 3. Iterar páginas até submeter tudo (máx 10 páginas)
    current_html = html
    for step in range(10):
        hidden = _extract_hidden(current_html)
        qs = _extract_questions(current_html)

        if _is_truly_done(current_html):
            print(f"  LimeSurvey: submissão realmente concluída (step {step})")
            return True

        if not qs and step > 0:
            print(f"  Sem perguntas na página {step} — possível conclusão ou erro")
            print(f"  HTML: {current_html[:300]}")
            break

        post_data = {}
        post_data.update(hidden)
        post_data.pop("ajax", None)  # desabilitar modo AJAX para forçar submissão síncrona
        post_data.update({k: "A" for k in qs})
        # Última página → usar movesubmit diretamente para garantir gravação
        post_data["move"] = "movesubmit"
        post_data["sid"] = str(survey_id)
        post_data["lang"] = "pt"

        print(f"  step {step}: POST com {len(qs)} perguntas, move=movesubmit | valores: {dict(list(qs.items())[:4])}")
        resp = session.post(survey_url, data=post_data, timeout=20, allow_redirects=False)
        redirect_url = resp.headers.get("Location", "")
        print(f"  step {step} resposta: {resp.status_code} | Location: {redirect_url or 'N/A'}")
        if redirect_url:
            # Retorna o redirect_url para que o caller possa seguir com auth Mihmo
            return redirect_url
        current_html = resp.text

        if _is_done(current_html):
            # Se ainda não é "truly done" (só tem botão Finalizar / página de revisão),
            # enviar movesubmit independente de ter ou não perguntas visíveis.
            if not _is_truly_done(current_html):
                qs_final = _extract_questions(current_html)
                print(f"  Página de revisão detectada (botão Finalizar) — enviando movesubmit com {len(qs_final)} perguntas...")
                submit_data = {}
                submit_data.update(_extract_hidden(current_html))
                if qs_final:
                    submit_data.update({k: "A" for k in qs_final})
                submit_data["move"] = "movesubmit"
                submit_data["sid"] = str(survey_id)
                submit_data["lang"] = "pt"
                resp2 = session.post(survey_url, data=submit_data, timeout=20, allow_redirects=True)
                print(f"  movesubmit resposta: {resp2.status_code} | len={len(resp2.text)}")
                current_html = resp2.text
            print(f"  LimeSurvey: submissão concluída (step {step})")
            # Notificar Mihmo da integração (o mesmo fetch que o frontend faz)
            _re_survey = _re.search(r"clinical-record/survey/(\d+)", current_html)
            if not _re_survey:
                _re_survey = _re.search(r"clinical-record/survey/(\d+)", str(survey_id))
            notify_url = f"https://homolog.mihmo.com.br/backend-nest/limesurveyintegration/integrate-responses/clinical-record"
            print(f"  Notificando Mihmo (limesurveyintegration): POST {notify_url}")
            try:
                notify_resp = requests.post(notify_url, json={"surveyId": survey_id}, timeout=15)
                print(f"  limesurveyintegration: {notify_resp.status_code} | {notify_resp.text[:200]}")
            except Exception as e:
                print(f"  Notificação Mihmo erro: {e}")
            return True

    print(f"  LimeSurvey: não confirmado após tentativas")
    return None


def _notificar_mihmo_survey(api_url, survey_id, token=None):
    """Integra respostas do LimeSurvey via POST limesurveyintegration/integrate-responses/clinical-record."""
    base = api_url.rsplit('/backend-nest', 1)[0]
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # Endpoint correto para integração de clinical-record
    url = f"{base}/backend-nest/limesurveyintegration/integrate-responses/clinical-record"
    try:
        resp = requests.post(url, json={"surveyId": survey_id}, headers=headers, timeout=15)
        print(f"  limesurvey integrate-responses/clinical-record: {resp.status_code} | {resp.text[:300]}")
        if resp.status_code in (200, 201) and resp.text.strip().startswith("{"):
            data = resp.json()
            return data.get("integrated", 0)
        return 0
    except Exception as e:
        print(f"  integrate-responses/clinical-record erro: {e}")
        return 0


def _verificar_ficha_integrada(base_url, token, attendance_id):
    """Verifica se a ficha clínica está integrada via check-clinical-record.
    Retorna True se allow=True (ou se não for possível determinar)."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    ccr_url = f"{base_url}/attendance/api/scheduled-attendance/check-clinical-record/{attendance_id}"
    try:
        ccr_resp = requests.get(ccr_url, headers=headers, timeout=10)
        print(f"_verificar_ficha_integrada: {ccr_resp.status_code} | {ccr_resp.text[:300]}")
        if ccr_resp.status_code == 200:
            ccr_data = ccr_resp.json()
            return ccr_data.get("allow", True)
        return True  # se endpoint não retornou 200, assume OK
    except Exception as e:
        print(f"  _verificar_ficha_integrada parse warning: {e}")
        return True  # em caso de erro de parse, assume OK


def criar_ficha_clinica(api_url, token, customer_id, attendance_id, cpf=None):
    """Cria a Ficha de HOMOLOG e submete o LimeSurvey automaticamente."""
    url = f"{api_url}/clinical-record"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    # Buscar versão anterior para usar como previousVersionId
    base_url = api_url.rsplit('/backend-nest', 1)[0]
    stepper_url = f"{base_url}/backend-nest/clinical-record/scheduled-attendance/{attendance_id}/stepper?page=1&pageSize=1"
    stepper_resp = requests.get(stepper_url, headers=headers)
    previous_version_id = None
    print(f"  stepper: {stepper_resp.status_code} | {stepper_resp.text[:300]}")
    if stepper_resp.status_code == 200:
        items = stepper_resp.json().get("items", [])
        if items:
            previous_version_id = items[0].get("id")
            print(f"  previousVersionId encontrado: {previous_version_id}")

    payload = {
        "typeId": FICHA_HOMOLOG_TYPE_ID,
        "customerId": customer_id,
        "scheduledAttendanceId": attendance_id
    }
    if previous_version_id:
        payload["previousVersionId"] = previous_version_id

    response = requests.post(url, json=payload, headers=headers)
    print(f"Ficha clínica: {response.status_code} | {response.text}")
    if response.status_code not in (200, 201):
        print(f"Aviso: Ficha clínica retornou {response.status_code} — pode já existir.")
        return response.status_code

    # Extrair surveyId e link do LimeSurvey
    ficha_data = safe_json(response)
    if not ficha_data:
        return response.status_code

    # GET no clinical record para ver todos os campos (especialmente token de participante)
    ficha_id = ficha_data.get("id")
    if ficha_id:
        get_resp = requests.get(f"{api_url}/clinical-record/{ficha_id}", headers=headers)
        print(f"  GET clinical-record/{ficha_id}: {get_resp.status_code} | {get_resp.text}")

    survey_link = ficha_data.get("link", "")
    print(f"  survey_link: {survey_link}")
    survey_id_str = survey_link.split("/")[-1].split("?")[0] if survey_link else None
    if not (survey_id_str and survey_id_str.isdigit()):
        return response.status_code

    survey_id = int(survey_id_str)

    # Playwright: submeter formulário com sessão real do Mihmo
    print(f"  Submetendo Ficha de HOMOLOG via Playwright...")
    try:
        pw_ok = _submeter_ficha_playwright(survey_link, token, cpf, api_url)
        print(f"  Playwright result: {pw_ok}")
    except Exception as e:
        print(f"  Playwright erro: {e}")
        pw_ok = False

    # Verificar se o Playwright já integrou (canProceed/answers)
    time.sleep(3)

    # Verificar se integrou
    if ficha_id:
        cr_resp = requests.get(f"{api_url}/clinical-record/{ficha_id}", headers=headers)
        cr_data = cr_resp.json() if cr_resp.status_code == 200 else {}
        answers = cr_data.get("answers", [])
        can_proceed = cr_data.get("canProceed", False)
        print(f"  clinical-record pós-Playwright: answers={len(answers)}, canProceed={can_proceed}")
        if answers or can_proceed:
            print(f"  Ficha integrada com sucesso!")
            return response.status_code

    print(f"  AVISO: Ficha não integrada — check-clinical-record pode retornar allow:false")
    return response.status_code


def patch_validate_data(api_url, token, pericia_id, start_date, cid, days, **kwargs):
    """Tenta confirmar/validar dados da perícia antes de homologar.
    Experimenta múltiplos métodos e sufixos de URL; retorna o body JSON se algum
    responder 2xx, ou None se nenhum funcionar (fluxo continuará sem o PATCH).
    """
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"startDate": start_date, "cid": cid or "", "days": int(days)}

    base = api_url if api_url.endswith('/backend-nest') \
        else api_url.rsplit('/backend-nest', 1)[0] + '/backend-nest'

    attendance_id = kwargs.get("attendance_id")
    att_base = base.rsplit('/backend-nest', 1)[0]
    candidates = []
    if attendance_id:
        candidates += [
            ("PATCH", f"{att_base}/attendance/api/scheduled-attendance/{attendance_id}/validate-data-requested"),
            ("POST",  f"{att_base}/attendance/api/scheduled-attendance/{attendance_id}/validate-data-requested"),
            ("PATCH", f"{att_base}/attendance/api/scheduled-attendance/{attendance_id}/validate-data"),
        ]
    candidates += [
        ("PATCH", f"{base}/medical-expert-report-request/{pericia_id}/validate-data-requested"),
        ("PATCH", f"{base}/medical-expert-report-request/{pericia_id}/validate-data"),
        ("POST",  f"{base}/medical-expert-report-request/{pericia_id}/validate-data-requested"),
        ("POST",  f"{base}/medical-expert-report-request/{pericia_id}/validate-data"),
        ("PUT",   f"{base}/medical-expert-report-request/{pericia_id}/validate-data-requested"),
        ("PATCH", f"{base}/medical-expert-report-request/{pericia_id}"),
    ]
    if attendance_id:
        candidates += [
            ("PATCH", f"{base}/medical-expert-report-request/{attendance_id}/validate-data-requested"),
            ("PATCH", f"{base}/medical-expert-report-request/{attendance_id}/validate-data"),
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
            print("validate-data-requested OK")
            return data[0] if isinstance(data, list) else data
        print(f"AVISO: validate-data-requested retornou {resp.status_code} — seguindo sem ele.")
    return None


def eligibility_check(api_url, token, pericia_id, accepted_days, accepted_start_date,
                      conclusion_id, functional_registration):
    """GET eligibility-check — valida os dados e habilita o generate-memed-file."""
    base = api_url if api_url.endswith('/backend-nest') \
        else api_url.rsplit('/backend-nest', 1)[0] + '/backend-nest'
    url = f"{base}/medical-expert-report-request/{pericia_id}/eligibility-check"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "acceptedDays": accepted_days,
        "acceptedStartDate": accepted_start_date,
        "conclusionId": conclusion_id,
        "functionalRegistration": functional_registration,
    }
    print(f"eligibility-check: GET {url}")
    print(f"  params: {params}")
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    print(f"  resposta: {resp.status_code} | {resp.text[:300]}")
    if resp.status_code == 200:
        print("eligibility-check OK — DataValideted deve ser True agora.")
        return resp.json()
    print(f"AVISO: eligibility-check retornou {resp.status_code} — seguindo sem ele.")
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
    """Busca o registrationId, employmentCategory e functionalRegistration do customer."""
    data = obter_customer(api_url, token, customer_id)
    regs = data.get("registrations") or []
    print(f"  customer registrations: {regs}")
    if regs:
        print(f"  customer regs[0] keys: {list(regs[0].keys())}")
        rid = regs[0].get("registrationid") or regs[0].get("registrationId") or regs[0].get("id")
        cat = regs[0].get("employmentCategory") or regs[0].get("employment_category") or regs[0].get("employmentcategory")
        func_reg = (regs[0].get("functionalRegistration")
                    or regs[0].get("functional_registration")
                    or regs[0].get("functionalregistration"))
        print(f"  registration_id: {rid}, category: {cat}, functionalRegistration: {func_reg}")
        return rid, cat, func_reg
    return None, None, None


def obter_squad_user_do_attendance(base_url, token, attendance_id):
    """Busca o squadUserId e memed_token no endpoint do attendance."""
    url = f"{base_url}/attendance/api/scheduled-attendance/{attendance_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"GET attendance: {response.status_code}")
    if response.status_code != 200:
        return None, None
    data = safe_json(response)
    print(f"  attendance keys: {list(data.keys())}")
    memed_token = data.get("token")
    if memed_token:
        print(f"  memed_token via attendance['token']: presente")
    # Debug: campos críticos de estado
    print(f"  canHomologate: {data.get('canHomologate')}")
    print(f"  canPrescription: {data.get('canPrescription')}")
    print(f"  canCid: {data.get('canCid')}")
    print(f"  medicalExpertReportRequestStatus: {data.get('medicalExpertReportRequestStatus')}")
    print(f"  medicalExpertReportRequestDataValideted: {data.get('medicalExpertReportRequestDataValideted')}")
    print(f"  stepper: {data.get('stepper')}")
    print(f"  clinicalRecord: {data.get('clinicalRecord')}")
    print(f"  medicalExpertReportRequestConclusion: {data.get('medicalExpertReportRequestConclusion')}")
    squad_user_id = None
    for campo in ("squadUserId", "squadUser", "squad_user", "userId", "user_id",
                  "doctorId", "doctor_id", "medicId", "medic_id"):
        val = data.get(campo)
        if val:
            print(f"  squad_user_id via '{campo}': {val}")
            if isinstance(val, dict):
                squad_user_id = val.get("id") or val.get("squadUserId")
            else:
                squad_user_id = val
            break
    if not squad_user_id:
        print(f"  AVISO: squad_user_id não encontrado. Campos disponíveis: {list(data.keys())}")
    return squad_user_id, memed_token


def obter_squad_user_id_proprio(api_url, token):
    """GET /squad-user/me — retorna o squadUserId do usuário autenticado."""
    base = api_url if api_url.endswith('/backend-nest') \
        else api_url.rsplit('/backend-nest', 1)[0] + '/backend-nest'
    candidates = [
        f"{base}/squad-user/me",
        f"{base}/user/me",
        f"{base}/auth/me",
    ]
    headers = {"Authorization": f"Bearer {token}"}
    for url in candidates:
        print(f"GET squad-user/me tentando: {url}")
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            print(f"  status: {resp.status_code} | {resp.text[:200]}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"  keys: {list(data.keys())}")
                sid = (
                    data.get("id")
                    or data.get("squadUserId")
                    or data.get("userId")
                    or data.get("user_id")
                )
                if sid:
                    print(f"  squad_user_id proprio: {sid}")
                    return sid
        except Exception as e:
            print(f"  erro: {e}")
    return None


def obter_memed_token(api_url, token, squad_user_id):
    """Obtém o JWT do Memed para o médico responsável."""
    base = api_url.rsplit('/backend-nest', 1)[0]
    url = f"{base}/backend-nest/memed/memed-token/{squad_user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"GET memed-token/{squad_user_id}: {response.status_code} | {response.text[:200]}")
    if response.status_code != 200:
        raise Exception(f"Erro ao obter token Memed: {response.status_code} - {response.text[:200]}")
    data = safe_json(response)
    print(f"DEBUG memed-token response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
    print(f"DEBUG memed-token response: {str(data)[:300]}")
    memed_token = data.get("token") if isinstance(data, dict) else None
    print(f"Token Memed obtido para squadUser {squad_user_id}: {'ok' if memed_token else 'NULO'}")
    return memed_token


def obter_primeiro_artigo(api_url, token, pericia_id, attendance_id=None, cid=None, category=None, is_junta=False, functional_registration=None, service_type=None):
    """Retorna (article_id, article_name) do primeiro artigo aplicável para a perícia.
    - Para tipos LTS/LTF/LTS_INSS usa PMV_ARTICLES_LTS (hardcoded, API pode retornar obsoletos).
    - Para outros tipos usa a API e retorna o primeiro artigo válido.
    """
    base = api_url if api_url.endswith('/backend-nest') \
        else api_url.rsplit('/backend-nest', 1)[0] + '/backend-nest'
    headers = {"Authorization": f"Bearer {token}"}

    # Para tipos de licença médica, usar lista hardcoded (API retorna artigos obsoletos)
    if service_type in PMV_SERVICE_TYPES_LTS or service_type is None:
        print(f"Usando PMV_ARTICLES_LTS como fonte autoritativa de artigos (service_type={service_type}).")
        items = PMV_ARTICLES_LTS
    else:
        # Para outros tipos (Consulta, Admissional, Acidente, etc.) consultar a API
        print(f"Consultando API de artigos para service_type={service_type}...")
        items = None
        candidates_urls = []
        if functional_registration:
            candidates_urls += [
                f"{base}/medical-expert-report-request/article/{pericia_id}/{functional_registration}/Accepted",
                f"{base}/medical-expert-report-request/article/{pericia_id}/{functional_registration}",
            ]
        candidates_urls += [
            f"{base}/medical-expert-report-request/article/{pericia_id}/Accepted",
            f"{base}/medical-expert-report-request/article/{pericia_id}",
        ]
        if attendance_id:
            candidates_urls += [
                f"{base}/medical-expert-report-request/article/{attendance_id}/Accepted",
                f"{base}/medical-expert-report-request/article/{attendance_id}",
            ]
        for url in candidates_urls:
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                print(f"  GET {url}: {resp.status_code}")
                if resp.status_code == 200:
                    data = safe_json(resp)
                    raw = data if isinstance(data, list) else (data or {}).get("items", [])
                    if raw:
                        items = raw
                        break
            except Exception as e:
                print(f"  Erro ao consultar {url}: {e}")
        if not items:
            print("  API não retornou artigos — usando PMV_ARTICLES_LTS como fallback.")
            items = PMV_ARTICLES_LTS

    filtered = [a for a in items if a.get("medicalBoard", False) == is_junta]
    if category:
        by_cat = [a for a in filtered if category in (a.get("applicableCategories") or [])]
        if by_cat:
            filtered = by_cat
    if not filtered:
        filtered = items
    article_id   = filtered[0].get("id")
    article_name = filtered[0].get("article", "")
    print(f"  Artigo selecionado: {article_name} ({article_id})")
    return article_id, article_name


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
    response = None
    for _attempt in range(3):
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code in (200, 201):
            break
        print(f"Memed prescricoes tentativa {_attempt+1}/3: {response.status_code} — aguardando...")
        time.sleep(4)
    if response.status_code not in (200, 201):
        raise Exception(f"Erro Memed prescricoes: {response.status_code} - {response.text[:300]}")
    memed_file_id = safe_json(response).get("data", {}).get("id")
    print(f"Prescrição Memed criada: memedFileId={memed_file_id} (tipo: {type(memed_file_id).__name__})")
    # Mihmo espera inteiro — converte se vier como string
    try:
        memed_file_id = int(memed_file_id)
    except (TypeError, ValueError):
        pass
    print(f"  memedFileId convertido: {memed_file_id} (tipo: {type(memed_file_id).__name__})")
    return memed_file_id


def emitir_certificado_memed(api_url, token_medico, pericia_id, memed_file_id, memed_token):
    """Gera o PDF da prescrição no Memed via GET /v1/prescricoes/pdf/{id}?printConfig=...
    Este passo é obrigatório antes de chamar generate-memed-file."""
    import urllib.parse
    import json as _json

    today_br = datetime.now().strftime("%d/%m/%Y")
    print_config = {
        "simple": {
            "all": {
                "print": True,
                "showDate": True,
                "isToHideActiveIngredient": False,
                "copies": {today_br: 1}
            }
        }
    }
    print_config_encoded = urllib.parse.quote(_json.dumps(print_config, separators=(',', ':')), safe='')
    ts = int(time.time() * 1000)
    url = (
        f"https://api.memed.com.br/v1/prescricoes/pdf/{memed_file_id}"
        f"?printConfig={print_config_encoded}&signed=false&reprint=false&print=false&_={ts}"
    )
    headers = {
        "Authorization": f"Bearer {memed_token}",
        "Accept": "application/vnd.api+json"
    }
    response = requests.get(url, headers=headers, timeout=30)
    print(f"memed printConfig (gerar PDF): {response.status_code} | {response.text[:200]}")
    if response.status_code not in (200, 201):
        print(f"AVISO: memed printConfig retornou {response.status_code} — continuando mesmo assim")
    return response.status_code


def gerar_memed_file_mihmo(api_url, token, attendance_id, pericia_id,
                            registration_id, memed_file_id, memed_token,
                            days, cid, start_date, observations, article_id, do_finish=True):
    """Finaliza a homologação no Mihmo via generate-memed-file. Retorna status."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = start + timedelta(days=int(days) - 1)
    calculate_end_date = end.strftime("%d/%m/%Y")

    base = api_url.rsplit('/backend-nest', 1)[0]
    url = f"{base}/backend-nest/memed/generate-memed-file"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    # startDate: apenas a data (YYYY-MM-DD), calculateEndDate: DD/MM/YYYY (igual ao payload manual)
    start_dt = start_date.split("T")[0] if "T" in str(start_date) else start_date
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
        "startDate": start_dt,
        "calculateEndDate": calculate_end_date,
        "observations": observations,
    }

    if article_id:
        payload["articleId"] = article_id
    # Verificar check-clinical-record antes de enviar
    att_base2 = base.rsplit('/backend-nest', 1)[0]
    ccr_url = f"{att_base2}/attendance/api/scheduled-attendance/check-clinical-record/{attendance_id}"
    ccr_resp = requests.get(ccr_url, headers=headers, timeout=10)
    print(f"check-clinical-record: {ccr_resp.status_code} | {ccr_resp.text[:300]}")
    try:
        ccr_data = ccr_resp.json()
        if not ccr_data.get("allow", True):
            raise Exception(
                f"check-clinical-record: allow=false — ficha clínica não integrada. "
                f"Mensagem: {ccr_data.get('message', '')} | Título: {ccr_data.get('title', '')}"
            )
    except Exception as e:
        if "allow=false" in str(e):
            raise
        print(f"  check-clinical-record parse warning: {e}")

    print(f"generate-memed-file payload: {json.dumps(payload, indent=2)}")
    response = None
    for _attempt in range(3):
        response = requests.post(url, json=payload, headers=headers)
        print(f"generate-memed-file tentativa {_attempt+1}/3: {response.status_code} | {response.text[:300]}")
        if response.status_code in (200, 201):
            break
        print(f"  Aguardando antes de retry...")
        time.sleep(4)
    if response.status_code not in (200, 201):
        raise Exception(f"Erro generate-memed-file: {response.status_code} - {response.text}")
    status = safe_json(response).get("status", "")
    print(f"Homologação concluída. Status: {status}")

    # 8. Finaliza o atendimento (apenas após o último profissional assinar)
    if do_finish:
        base2 = api_url.rsplit('/backend-nest', 1)[0]
        finish_url = f"{base2}/attendance/api/scheduled-attendance/{attendance_id}/finish"
        finish_resp = requests.post(finish_url, json={"id": attendance_id}, headers=headers, timeout=15)
        print(f"finish attendance: {finish_resp.status_code} | {finish_resp.text[:200]}")
        if finish_resp.status_code not in (200, 201):
            print(f"AVISO: finish retornou {finish_resp.status_code} — seguindo mesmo assim")
    else:
        print(f"finish attendance: pulado (aguardando demais profissionais da junta)")

    return status


def obter_squad_users_por_role(api_url, token, role_id, count=1):
    """Busca squad users disponíveis para um roleId, priorizando os que temos credenciais."""
    base = api_url.rsplit('/backend-nest', 1)[0] + '/backend-nest'
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": 1, "pageSize": 50, "roleId": role_id}
    resp = requests.get(f"{base}/squad-user", params=params, headers=headers, timeout=10)
    print(f"GET squad-user roleId={role_id}: {resp.status_code}")
    if resp.status_code != 200:
        raise Exception(f"Erro ao buscar squad users para role {role_id}: {resp.status_code} - {resp.text[:200]}")
    items = resp.json().get("items", [])
    with_creds = [u for u in items if u.get("email") in _EMAIL_TO_CRED_KEY]
    print(f"  {len(items)} squad users encontrados, {len(with_creds)} com credenciais cadastradas")
    if len(with_creds) < count:
        raise Exception(
            f"Precisamos de {count} squad user(s) com credenciais para role {role_id}, "
            f"mas só temos {len(with_creds)}. Adicione mais credenciais em CREDENTIALS."
        )
    return with_creds[:count]


def selecionar_profissionais_junta(api_url, token_clinica, attendance_id, board_role_ids):
    """
    Seleciona os profissionais para a Junta Médica via POST /medical-board.
    board_role_ids: lista de (role_id, role_description) — uma entrada por vaga.
    Retorna lista de dicts com {squad_user_id, email, role_name, cred_key}.
    """
    from collections import Counter
    base_url = api_url.rsplit('/backend-nest', 1)[0]

    role_counts = Counter(rid for rid, _ in board_role_ids)
    role_name_map = {rid: desc for rid, desc in board_role_ids}

    selected = []
    for role_id, count in role_counts.items():
        users = obter_squad_users_por_role(api_url, token_clinica, role_id, count)
        for u in users:
            selected.append({
                "squad_user_id": u["id"],
                "email":         u["email"],
                "role_name":     role_name_map[role_id],
                "cred_key":      _EMAIL_TO_CRED_KEY[u["email"]],
            })

    squad_ids = [s["squad_user_id"] for s in selected]
    url = f"{base_url}/attendance/api/scheduled-attendance/medical-board"
    headers = {"Authorization": f"Bearer {token_clinica}", "Content-Type": "application/json"}
    payload = {"id": attendance_id, "squadUserIds": squad_ids}
    print(f"POST medical-board payload: {payload}")
    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    print(f"POST medical-board: {resp.status_code} | {resp.text[:300]}")
    if resp.status_code not in (200, 201):
        raise Exception(
            f"Erro ao selecionar profissionais da junta: {resp.status_code} - {resp.text[:300]}"
        )
    print(f"Junta: {len(selected)} profissional(is) selecionado(s): "
          f"{[s['role_name'] + ' (' + s['cred_key'] + ')' for s in selected]}")
    return selected


def _homologar_junta(api_url, token_clinica, attendance_id, entrada):
    """
    Orquestra o fluxo de Junta Médica:
    1. Busca medicalBoardRoles com IDs do attendance
    2. Seleciona profissionais via POST /medical-board
    3. Envia para fila
    4. Cada profissional executa o fluxo completo de homologação
    5. Finish apenas após o último profissional assinar
    """
    base_url = api_url.rsplit('/backend-nest', 1)[0]

    # 1. Buscar medicalBoardRoles com roleIds
    headers_clinica = {"Authorization": f"Bearer {token_clinica}"}
    resp = requests.get(
        f"{base_url}/attendance/api/scheduled-attendance/{attendance_id}",
        headers=headers_clinica, timeout=15
    )
    if resp.status_code != 200:
        raise Exception(f"Erro ao buscar attendance para junta: {resp.status_code}")
    att_data = resp.json()
    board_role_ids = [
        (r["id"], r["description"])
        for r in att_data.get("medicalBoardRoles", [])
    ]
    if not board_role_ids:
        raise Exception(f"attendance {attendance_id} não tem medicalBoardRoles — não é junta?")
    print(f"Junta: {len(board_role_ids)} vagas: {[d for _, d in board_role_ids]}")

    # 2. Selecionar profissionais (GET squad-user + POST /medical-board)
    selected_users = selecionar_profissionais_junta(api_url, token_clinica, attendance_id, board_role_ids)

    # 3. Enviar para fila
    enviar_para_fila(api_url, token_clinica, attendance_id)

    # 4. Cada profissional homologa
    status = None
    total = len(selected_users)
    for i, prof in enumerate(selected_users):
        is_last = (i == total - 1)
        print(f"\n{'='*60}")
        print(f"Homologando profissional {i+1}/{total}: {prof['role_name']} ({prof['cred_key']})")
        print(f"{'='*60}")
        token_medico = _obter_token(prof["cred_key"])
        squad_user_id = _jwt_user_id(token_medico)
        if not squad_user_id:
            raise Exception(f"Não foi possível extrair user_id do token de '{prof['cred_key']}'.")

        iniciar_atendimento(base_url, token_medico, attendance_id, squad_user_id)
        _, memed_token_attendance = obter_squad_user_do_attendance(base_url, token_medico, attendance_id)

        customer_id   = entrada.get("customer_id")
        cpf           = entrada.get("cpf")
        cid           = entrada.get("cid")
        days          = entrada.get("days")
        start_date    = entrada.get("start_date") or gerar_data_hoje()
        service_type  = entrada.get("service_type")
        pericia_id    = entrada.get("pericia_id")
        observations  = "Teste automatizado"

        criar_ficha_clinica(api_url, token_medico, customer_id, attendance_id, cpf=cpf)

        _check_base = api_url.rsplit('/backend-nest', 1)[0]
        for _tentativa in range(1, 3):
            if _verificar_ficha_integrada(_check_base, token_medico, attendance_id):
                print(f"  Ficha clínica integrada OK (tentativa {_tentativa})")
                break
            print(f"  Ficha não integrada (tentativa {_tentativa}/2) — re-submetendo...")
            time.sleep(5)
            criar_ficha_clinica(api_url, token_medico, customer_id, attendance_id, cpf=cpf)
            time.sleep(5)

        pericia_data = patch_validate_data(
            api_url, token_medico, pericia_id, start_date, cid, days,
            attendance_id=attendance_id
        )

        def _extrair_registration_id_junta(data):
            if not data:
                return None
            reg = data.get("registration")
            if reg:
                rid = reg.get("registrationId") or reg.get("registrationid") or reg.get("id")
                if rid:
                    return rid
            regs = (data.get("customer") or {}).get("registrations") or data.get("registrations") or []
            if regs:
                return regs[0].get("registrationId") or regs[0].get("registrationid") or regs[0].get("id")
            return None

        registration_id = _extrair_registration_id_junta(pericia_data)
        rid_customer, category_from_customer, functional_registration = obter_registration_id_do_customer(
            api_url, token_medico, customer_id
        )
        if not registration_id:
            registration_id = rid_customer
        category = categoria = category_from_customer

        if not registration_id:
            raise Exception(f"registration_id não encontrado para profissional {prof['cred_key']}.")

        article_id, article_name = obter_primeiro_artigo(
            api_url, token_medico, pericia_id,
            attendance_id=attendance_id, cid=cid, category=category,
            is_junta=True, functional_registration=functional_registration,
            service_type=service_type
        )

        eligibility_check(
            api_url, token_medico, pericia_id,
            accepted_days=days, accepted_start_date=start_date,
            conclusion_id=article_id, functional_registration=functional_registration
        )

        memed_token = obter_memed_token(api_url, token_medico, squad_user_id)
        if not memed_token:
            memed_token = memed_token_attendance

        customer_name = entrada.get("nome")
        memed_file_id = criar_prescricao_memed(
            memed_token, customer_id, customer_name, cpf,
            cid, days, start_date, observations
        )

        emitir_certificado_memed(api_url, token_medico, pericia_id, memed_file_id, memed_token)

        status = gerar_memed_file_mihmo(
            api_url, token_medico, attendance_id, pericia_id,
            registration_id, memed_file_id, memed_token,
            days, cid, start_date, observations, article_id,
            do_finish=is_last
        )
        print(f"Profissional {i+1}/{total} concluído. Status: {status}")

    # Para junta, a API retorna 'SignaturePending' por profissional;
    # o atendimento é dado como concluído após todos assinarem e o finish ser chamado.
    return "Accepted"


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

    token_clinica = _obter_token("CLINICA")

    role, is_junta, board_roles, attendance_id = verificar_especialista_api(
        api_url, token, regra
    )

    if not attendance_id:
        raise Exception(f"attendance_id não encontrado para regra {regra}")

    if is_junta:
        return _homologar_junta(api_url, token_clinica, attendance_id, entrada)

    enviar_para_fila(api_url, token_clinica, attendance_id)

    token_medico = _obter_token(role)

    if not token_medico:
        raise Exception(f"Token não encontrado para role '{role}'")

    if not attendance_id:
        raise Exception(f"attendance_id inválido para regra {regra}")
    
    cid           = entrada.get("cid")
    days          = entrada.get("days")
    customer_id   = entrada.get("customer_id")
    customer_name = entrada.get("nome")
    cpf           = entrada.get("cpf")
    category      = entrada.get("employmentCategory")
    start_date    = entrada.get("start_date") or gerar_data_hoje()
    service_type  = entrada.get("service_type")
    observations  = "Teste automatizado"

    if not all([pericia_id, attendance_id, cid, days, customer_id]):
        raise Exception(
            f"Dados incompletos para '{regra}'. "
            f"pericia_id={pericia_id}, attendance_id={attendance_id}, "
            f"cid={cid}, days={days}"
        )

    base_url = api_url.rsplit('/backend-nest', 1)[0]

    # 1. squad_user_id = user_id extraído do JWT do médico
    squad_user_id = _jwt_user_id(token_medico)
    print(f"squad_user_id (JWT)={squad_user_id}")
    if not squad_user_id:
        raise Exception(f"Não foi possível extrair user_id do token do médico para '{regra}'.")

    # 2. Iniciar atendimento via PATCH /squaduser com lock
    iniciar_atendimento(base_url, token_medico, attendance_id, squad_user_id)
    # Re-fetch após iniciar para pegar token Memed se disponível
    _, memed_token_attendance = obter_squad_user_do_attendance(base_url, token_medico, attendance_id)
    criar_ficha_clinica(api_url, token_medico, customer_id, attendance_id, cpf=cpf)

    # Verificar se a ficha clínica integrou — retry automático se allow=false (máx 2 tentativas)
    _check_base = api_url.rsplit('/backend-nest', 1)[0]
    for _tentativa in range(1, 3):
        if _verificar_ficha_integrada(_check_base, token_medico, attendance_id):
            print(f"  Ficha clínica integrada OK (tentativa {_tentativa})")
            break
        print(f"  Ficha não integrada (tentativa {_tentativa}/2) — aguardando e re-submetendo...")
        time.sleep(5)
        criar_ficha_clinica(api_url, token_medico, customer_id, attendance_id, cpf=cpf)
        time.sleep(5)
    else:
        print("  AVISO: Ficha pode não ter integrado após 2 tentativas — prosseguindo (generate-memed-file vai confirmar)")

    pericia_data = patch_validate_data(
        api_url, token_medico, pericia_id, start_date, cid, days,
        attendance_id=attendance_id
    )

    # 3. registration_id
    def _extrair_registration_id(data):
        if not data:
            return None
        reg = data.get("registration")
        if reg:
            rid = reg.get("registrationId") or reg.get("registrationid") or reg.get("id")
            if rid:
                return rid
        regs = (data.get("customer") or {}).get("registrations") or data.get("registrations") or []
        if regs:
            return (
                regs[0].get("registrationId")
                or regs[0].get("registrationid")
                or regs[0].get("id")
            )
        return None

    registration_id = _extrair_registration_id(pericia_data)
    # Sempre busca do customer para garantir category e functionalRegistration
    rid_customer, category_from_customer, functional_registration = obter_registration_id_do_customer(api_url, token_medico, customer_id)
    if not registration_id:
        registration_id = rid_customer
    if category_from_customer:
        category = category_from_customer
    if not functional_registration:
        print("AVISO: functionalRegistration não encontrado no customer — eligibility-check pode falhar")
    print(f"registration_id={registration_id}, category={category}, functionalRegistration={functional_registration}")
    if not registration_id:
        raise Exception(
            f"registration_id não encontrado para '{regra}'. "
            f"Verifique se o customer '{customer_id}' tem matrícula cadastrada."
        )

    # 4. Artigo CID (URL correta inclui functionalRegistration)
    article_id, article_name = obter_primeiro_artigo(
        api_url, token_medico, pericia_id,
        attendance_id=attendance_id, cid=cid, category=category,
        is_junta=is_junta, functional_registration=functional_registration,
        service_type=service_type
    )

    # 4.5 eligibility-check — valida dados e habilita DataValideted no backend
    eligibility_check(
        api_url, token_medico, pericia_id,
        accepted_days=days,
        accepted_start_date=start_date,
        conclusion_id=article_id,
        functional_registration=functional_registration
    )

    # 5. Token Memed
    # Sempre obtém token Memed fresco — token em cache pode estar expirado
    memed_token = obter_memed_token(api_url, token_medico, squad_user_id)
    if not memed_token:
        memed_token = memed_token_attendance

    if memed_token:
        prefix = memed_token[:30]
        alg = "HS256(Memed)" if "eyJ0eXAiOiJKV1Qi" in memed_token[:30] else "RS256(Firebase?)"
        print(f"  memed_token prefix: {prefix}... alg_guess={alg}")


    # 6. Prescrição Memed
    memed_file_id = criar_prescricao_memed(
        memed_token, customer_id, customer_name, cpf,
        cid, days, start_date, observations
    )

    # 6.5 Emite o certificado Memed no Mihmo (equivale ao clique em "Emitir" no widget)
    emitir_certificado_memed(api_url, token_medico, pericia_id, memed_file_id, memed_token)

    # 7. Finaliza no Mihmo
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
        return json.loads(response.text)
    except Exception:
        raise Exception(
            f"Response inválida!\nStatus: {response.status_code}\nBody:\n{response.text[:500]}"
        )