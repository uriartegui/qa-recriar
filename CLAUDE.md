# CLAUDE.md

Suíte de testes de API (Robot Framework + Python) que cria massa de dados e homologa as regras de encaminhamento de perícias médicas (PMV e PPV). Visão geral e comandos no [README.md](README.md).

## Pontos importantes

- Credenciais e chaves vêm **só** do `.env` (modelo em `.env.example`). `pericia_helper.py` carrega o arquivo ao ser importado, e `mihmo_auth.robot` lê os valores com `%{VAR}`. Nunca coloque senha, token ou chave em `.py`, `.robot` ou `.yaml`.
- `resources/variables/*.yaml` têm apenas URLs e opções por ambiente.
- Cada regra tem um teste de setup (`tests/*/setup/`) e um de homologação (`tests/*/api/`) com nomes casados; `executar_regra.py` mapeia os dois na lista `REGRAS`. Ao criar uma regra, atualize os três.
- A massa criada é salva em `results/massa_criada_*.json` e lida pela homologação.
