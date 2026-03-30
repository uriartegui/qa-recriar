import requests
import json

# 1. Pega token Firebase
auth = requests.post(
    "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword",
    params={"key": "REMOVIDO"},
    json={"email": "adm.castela@mihmo.com.br", "password": "REMOVIDO", "returnSecureToken": True}
)
token = auth.json()["idToken"]
print(f"Token OK: {token[:30]}...")

# 2. Cria perícia
url = "https://homolog.mihmo.com.br/backend-nest/medical-expert-report-request/customer-lead/recriar"
headers = {"Authorization": f"Bearer {token}"}
data = {
    "customerId": json.dumps("51f26bc5-8004-4f1d-884e-731e3ddf259d"),
    "cpf": json.dumps("35198958700"),
    "origin": json.dumps("Customer"),
    "cellphone": json.dumps("88598985859"),
    "email": json.dumps("raegvserz@mihmo.com"),
    "startDate": json.dumps("2026-04-01"),
    "days": 16,
    "type": json.dumps("HealthCareLicense"),
    "medicCrm": json.dumps("1515"),
    "medicUf": json.dumps("AC"),
    "cid": json.dumps("J00"),
}
with open("resources/fixtures/atestado.png", "rb") as f:
    files = {"files": ("atestado.png", f, "image/png")}
    response = requests.post(url, data=data, files=files, headers=headers)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:1000]}")
