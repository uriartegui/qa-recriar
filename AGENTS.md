# qa-recriar — Contexto para Hermes Agent

## O que é esse projeto

Suite de testes de homologação da plataforma **Mihmo** — sistema de gestão de perícias médicas para o setor público.
Testa o roteamento automático de perícias para especialistas médicos.

## Stack

- **Robot Framework** — testes `.robot`
- **Python** — keywords customizadas em `resources/keywords/pericia_helper.py`
- **Tkinter** — GUI `executar_regra.py` para rodar testes individualmente
- **API Mihmo** — endpoints REST de criação de clientes, perícias e homologação

## Estrutura

```
tests/
  pmv/
    setup/criar_massa.robot       → cria customers + perícias (PMV)
    api/homologacao.robot         → verifica roteamento + homologa (PMV)
  ppv/
    setup/criar_massa_ppv.robot   → cria customers + perícias (PPV)
    api/homologacao_ppv.robot     → verifica roteamento + homologa (PPV)
resources/
  keywords/
    pericia_helper.py             → keywords Python principais
    mihmo_auth.robot              → autenticação
  variables/
    homolog.yaml                  → variáveis de ambiente (API_URL, credenciais)
results/
  massa_criada.json               → dados criados pelo setup, lidos pela homologação
executar_regra.py                 → GUI Tkinter
```

## Fluxo de Teste

1. **Criar massa** (`criar_massa.robot`) → cria customer + pericia com CID e tipo definidos → salva IDs em `massa_criada.json`
2. **Homologar** (`homologacao.robot`) → lê `massa_criada.json` → verifica especialista → envia para fila → homologa

## Clientes Testados

| Suite | Cliente | Company ID |
|-------|---------|------------|
| PMV | Produto Mínimo Viável | — |
| PPV | Porto Velho | `80cf1683-3f88-4941-bf57-e36e799f47bc` |

## Convenções de Chaves (massa_criada.json)

- PMV: prefixo `PMV_` → ex: `PMV_LTS_1DIA_GERAL`
- PPV: prefixo `PPV_` → ex: `PPV_LTS_1DIA_GERAL`

## Tipos de Perícia

| Variável Robot | API type string |
|---------------|-----------------|
| `${LTS}` | `HealthCareLicense` |
| `${LTF}` | `FamilyPersonTreatmentLicense` |
| `${RF}` | `FunctionalReadaptation` |
| `${ABANDONO}` | `JobAbandonment` |
| `${APOSENT_INVALIDEZ}` | `DisabilityRetirement` |
| `${PARECER_MED}` | `MedicalWorkAssessment` |
| `${RECURSO}` | `Appeal` |
| `${RED_JORNADA_DEP}` | `ReductionOfWorkloadJourneyDependent` |
| `${RED_JORNADA_SERV}` | `ReductionOfWorkloadJourneyEmployee` |
| `${REMOCAO}` | `Removal` |
| `${REMOCAO_DEP}` | `RemovalDependent` |

## CIDs Usados

| Grupo | CID | Especialista roteado |
|-------|-----|---------------------|
| Geral | J00 | Clínico Geral ou Médico do Trabalho |
| Psiquiatria | F32 | Psiquiatra |
| Ortopedia | M54 | Ortopedista |

## Regras Especiais

- **Junta Médica**: RF usa `junta=${TRUE}` → verifica `is_junta=True` + `board_roles` contém o especialista
- **Abandono**: sem homologação (não tem especialista associado)
- **Redução/Remoção Dep CID F**: multi-especialista (Psicólogo + Psiquiatra) → valida Psiquiatra
- **Redução/Remoção Dep CID MS**: multi-especialista (Assist. Social + Ortopedista) → valida Ortopedista

## Problemas Conhecidos

- `sign/initialize` retorna 500 para todos os casos de Junta Médica
  - Causa: backend rejeita qualquer certificado (self-signed e BRY ECDSA P-384 são DESCONHECIDO)
  - Workaround: assinatura removida; testes de Junta passam com status `SignaturePending` ou `Accepted`

## Estado Atual

- PMV: 29 regras implementadas
- PPV: 54 regras implementadas
- GUI: 84 regras totais + botão "Homologar Tudo"
- `massa_criada.json` atual tem chaves antigas sem prefixo PMV_ → precisa recriar massa PMV
