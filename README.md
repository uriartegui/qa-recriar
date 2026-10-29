# QA Recriar — homologação de regras de perícia

Automação de testes de API, em Robot Framework e Python, que valida as regras de encaminhamento de perícias médicas de uma plataforma de saúde ocupacional.

Para cada regra (tipo de licença, CID e quantidade de dias), a suíte:

1. **Cria a massa de dados** pela API: cadastra o paciente e abre a perícia com o atestado.
2. **Homologa a regra**: confere se a perícia foi encaminhada para o especialista ou a junta médica esperada.

Os cenários cobrem os limites de cada faixa (3/4, 14/15, 59/60 dias), onde as regras mudam de destino.

## Estrutura

```
tests/
  pmv/  setup/criar_massa.robot       # gera a massa das regras PMV
        api/homologacao.robot         # valida o encaminhamento PMV
  ppv/  setup/criar_massa_ppv.robot   # gera a massa das regras PPV
        api/homologacao_ppv.robot     # valida o encaminhamento PPV
resources/
  keywords/pericia_helper.py          # biblioteca Python: chamadas de API e auto-login
  keywords/mihmo_auth.robot           # autenticação Firebase
  variables/homolog.yaml, prod.yaml   # URLs por ambiente (sem credenciais)
executar_regra.py                     # painel desktop (Tkinter) para rodar uma regra por vez
```

## Como rodar

```bash
pip install -r requirements.txt
cp .env.example .env   # preencha com as credenciais do ambiente de homologação
robot tests/pmv/setup/criar_massa.robot
robot tests/pmv/api/homologacao.robot
```

Ou abra o painel e escolha a regra:

```bash
python executar_regra.py
```

As credenciais ficam só no `.env`, que não é versionado.
