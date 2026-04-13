"""
Popup para criar massa e homologar uma regra de perícia (PMV ou PPV).
Uso: python executar_regra.py
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# ──────────────────────────────────────────────────────────────────────────────
# Mapeamento completo de regras → arquivos e nomes de teste exatos
# ──────────────────────────────────────────────────────────────────────────────
REGRAS = [
    # ── PMV / LTS / Geral ──────────────────────────────────────────────────
    {"suite": "PMV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "1 dia",
     "especialista": "Médico Trabalho", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 1 Dia - CID Geral - Medico Trabalho",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 1 Dia - CID Geral - Deve ir para Medico Trabalho"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "3 dias (borda)",
     "especialista": "Médico Trabalho", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 3 Dias - CID Geral - Limite Medico Trabalho",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 3 Dias - CID Geral - Deve ir para Medico Trabalho"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "4 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 4 Dias - CID Geral - Inicio Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 4 Dias - CID Geral - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "14 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 14 Dias - CID Geral - Limite Faixa 4-14",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 14 Dias - CID Geral - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "15 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 15 Dias - CID Geral - Inicio Faixa 15-59",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 15 Dias - CID Geral - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "59 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 59 Dias - CID Geral - Limite Antes Junta",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 59 Dias - CID Geral - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "60+ dias → Junta",
     "especialista": "Clínico Geral (Junta)", "junta": True,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 61 Dias - CID Geral - Junta Medica Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 60 Dias - CID Geral - Deve ir para Junta Medica"},

    # ── PMV / LTS / Psiquiatria ─────────────────────────────────────────────
    {"suite": "PMV", "tipo": "LTS", "cid": "Psiquiatria (F32)", "dias": "4 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 4 Dias - CID F - Inicio Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 4 Dias - CID F - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Psiquiatria (F32)", "dias": "29 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 29 Dias - CID F - Limite Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 29 Dias - CID F - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Psiquiatria (F32)", "dias": "30 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 30 Dias - CID F - Inicio Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 30 Dias - CID F - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Psiquiatria (F32)", "dias": "59 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 59 Dias - CID F - Limite Antes Junta",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 59 Dias - CID F - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Psiquiatria (F32)", "dias": "60+ dias → Junta",
     "especialista": "Psiquiatra (Junta)", "junta": True,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 61 Dias - CID F - Junta Medica Psiquiatra e Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 60 Dias - CID F - Deve ir para Junta Psiquiatra"},

    # ── PMV / LTS / Ortopedia ───────────────────────────────────────────────
    {"suite": "PMV", "tipo": "LTS", "cid": "Ortopedia (M54)", "dias": "4 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 4 Dias - CID M S - Inicio Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 4 Dias - CID MS - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Ortopedia (M54)", "dias": "14 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 14 Dias - CID M S - Limite Faixa 4-14 Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 14 Dias - CID MS - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Ortopedia (M54)", "dias": "15 dias (borda)",
     "especialista": "Ortopedista", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 15 Dias - CID M S - Inicio Ortopedista",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 15 Dias - CID MS - Deve ir para Ortopedista"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Ortopedia (M54)", "dias": "59 dias (borda)",
     "especialista": "Ortopedista", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 59 Dias - CID M S - Limite Antes Junta Ortopedista",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 59 Dias - CID MS - Deve ir para Ortopedista"},

    {"suite": "PMV", "tipo": "LTS", "cid": "Ortopedia (M54)", "dias": "60+ dias → Junta",
     "especialista": "Ortopedista (Junta)", "junta": True,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS - 61 Dias - CID M S - Junta Medica Ortopedista e Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS - 60 Dias - CID MS - Deve ir para Junta Ortopedista"},

    # ── PMV / LTS INSS ──────────────────────────────────────────────────────
    {"suite": "PMV", "tipo": "LTS INSS", "cid": "—", "dias": "1 dia",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTS INSS - 1 Dia - Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTS INSS - 1 Dia - Deve ir para Clinico Geral"},

    # ── PMV / LTF ────────────────────────────────────────────────────────────
    {"suite": "PMV", "tipo": "LTF", "cid": "—", "dias": "1 dia",
     "especialista": "Médico Trabalho", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTF - 1 Dia - Medico Trabalho",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTF - 1 Dia - Deve ir para Medico Trabalho"},

    {"suite": "PMV", "tipo": "LTF", "cid": "—", "dias": "3 dias (borda)",
     "especialista": "Médico Trabalho", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTF - 3 Dias - Limite Medico Trabalho",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTF - 3 Dias - Deve ir para Medico Trabalho"},

    {"suite": "PMV", "tipo": "LTF", "cid": "—", "dias": "4 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTF - 4 Dias - Inicio Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTF - 4 Dias - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTF", "cid": "—", "dias": "59 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTF - 59 Dias - Limite Antes Junta",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTF - 59 Dias - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "LTF", "cid": "—", "dias": "60+ dias → Junta",
     "especialista": "Clínico Geral (Junta)", "junta": True,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "LTF - 61 Dias - Junta Medica Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "LTF - 60 Dias - Deve ir para Junta Medica"},

    # ── PMV / Outros ─────────────────────────────────────────────────────────
    {"suite": "PMV", "tipo": "Consulta Médica", "cid": "—", "dias": "1 dia",
     "especialista": "Médico Trabalho", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "Consulta Medica - 1 Dia - Medico Trabalho",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "Consulta Medica - Deve ir para Medico Trabalho"},

    {"suite": "PMV", "tipo": "Admissional", "cid": "—", "dias": "1 dia",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "Exame Admissional - 1 Dia - Clinico Geral",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "Exame Admissional - Deve ir para Clinico Geral"},

    {"suite": "PMV", "tipo": "Acidente de Trabalho", "cid": "—", "dias": "1 dia",
     "especialista": "Médico Trabalho", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "Acidente de Trabalho - 1 Dia - Medico Trabalho",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "Acidente Trabalho - Deve ir para Medico Trabalho"},

    {"suite": "PMV", "tipo": "Processos Adm.", "cid": "—", "dias": "1 dia",
     "especialista": "Médico Trabalho", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "Processos Administrativos - 1 Dia - Medico Trabalho",
     "homolog_file": "tests/pmv/api/homologacao.robot",
     "homolog_test": "Processos Administrativos - Deve ir para Medico Trabalho"},

    {"suite": "PMV", "tipo": "Gestação", "cid": "—", "dias": "120 dias",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "Licenca Gestacao - 120 Dias - Clinico Geral",
     "homolog_file": None,
     "homolog_test": None},

    {"suite": "PMV", "tipo": "Restrição de Atividade", "cid": "—", "dias": "1 dia",
     "especialista": "Clínico Geral (Junta)", "junta": True,
     "setup_file": "tests/pmv/setup/criar_massa.robot",
     "setup_test": "Atividade Com Restricao - 1 Dia - Junta Medica Clinico Geral",
     "homolog_file": None,
     "homolog_test": None},

    # ── PPV / LTS / Geral ───────────────────────────────────────────────────
    {"suite": "PPV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "1 dia",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 1 Dia - CID Geral - Clinico Geral",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 1 Dia - CID Geral - Deve ir para Clinico Geral"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "14 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 14 Dias - CID Geral - Limite Antes Faixa 15",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 14 Dias - CID Geral - Deve ir para Clinico Geral"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "15 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 15 Dias - CID Geral - Inicio Faixa 15",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 15 Dias - CID Geral - Deve ir para Clinico Geral"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "29 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 29 Dias - CID Geral - Limite Antes Faixa 30",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 29 Dias - CID Geral - Deve ir para Clinico Geral"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Geral (J00)", "dias": "30 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 30 Dias - CID Geral - Inicio Faixa 30",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 30 Dias - CID Geral - Deve ir para Clinico Geral"},

    # ── PPV / LTS / Psiquiatria ─────────────────────────────────────────────
    {"suite": "PPV", "tipo": "LTS", "cid": "Psiquiatria (F32)", "dias": "1 dia",
     "especialista": "Psiquiatra", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 1 Dia - CID F - Psiquiatra",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 1 Dia - CID F - Deve ir para Psiquiatra"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Psiquiatria (F32)", "dias": "14 dias (borda)",
     "especialista": "Psiquiatra", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 14 Dias - CID F - Limite Antes Faixa 15",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 14 Dias - CID F - Deve ir para Psiquiatra"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Psiquiatria (F32)", "dias": "15 dias (borda)",
     "especialista": "Psiquiatra", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 15 Dias - CID F - Inicio Faixa 15",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 15 Dias - CID F - Deve ir para Psiquiatra"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Psiquiatria (F32)", "dias": "29 dias (borda)",
     "especialista": "Psiquiatra", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 29 Dias - CID F - Limite Antes Faixa 30",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 29 Dias - CID F - Deve ir para Psiquiatra"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Psiquiatria (F32)", "dias": "30 dias (borda)",
     "especialista": "Psiquiatra", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 30 Dias - CID F - Inicio Faixa 30",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 30 Dias - CID F - Deve ir para Psiquiatra"},

    # ── PPV / LTS / Ortopedia ───────────────────────────────────────────────
    {"suite": "PPV", "tipo": "LTS", "cid": "Ortopedia (M54)", "dias": "1 dia",
     "especialista": "Ortopedista", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 1 Dia - CID M S - Ortopedista",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 1 Dia - CID MS - Deve ir para Ortopedista"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Ortopedia (M54)", "dias": "14 dias (borda)",
     "especialista": "Ortopedista", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 14 Dias - CID M S - Limite Antes Faixa 15",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 14 Dias - CID MS - Deve ir para Ortopedista"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Ortopedia (M54)", "dias": "15 dias (borda)",
     "especialista": "Ortopedista", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 15 Dias - CID M S - Inicio Faixa 15",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 15 Dias - CID MS - Deve ir para Ortopedista"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Ortopedia (M54)", "dias": "29 dias (borda)",
     "especialista": "Ortopedista", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 29 Dias - CID M S - Limite Antes Faixa 30",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 29 Dias - CID MS - Deve ir para Ortopedista"},

    {"suite": "PPV", "tipo": "LTS", "cid": "Ortopedia (M54)", "dias": "30 dias (borda)",
     "especialista": "Ortopedista", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTS - 30 Dias - CID M S - Inicio Faixa 30",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTS - 30 Dias - CID MS - Deve ir para Ortopedista"},

    # ── PPV / LTF ────────────────────────────────────────────────────────────
    {"suite": "PPV", "tipo": "LTF", "cid": "—", "dias": "1 dia",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTF - 1 Dia - Clinico Geral",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTF - 1 Dia - Deve ir para Clinico Geral"},

    {"suite": "PPV", "tipo": "LTF", "cid": "—", "dias": "29 dias (borda)",
     "especialista": "Clínico Geral", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTF - 29 Dias - Limite Antes Assistente Social",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTF - 29 Dias - Deve ir para Clinico Geral"},

    {"suite": "PPV", "tipo": "LTF", "cid": "—", "dias": "30 dias (borda)",
     "especialista": "Clínico Geral + Assistente Social", "junta": False,
     "setup_file": "tests/ppv/setup/criar_massa_ppv.robot",
     "setup_test": "LTF - 30 Dias - Clinico Geral e Assistente Social",
     "homolog_file": "tests/ppv/api/homologacao_ppv.robot",
     "homolog_test": "LTF - 30 Dias - Deve ir para Clinico Geral e Assistente Social"},
]

# ──────────────────────────────────────────────────────────────────────────────
# Helpers para filtrar a lista de regras
# ──────────────────────────────────────────────────────────────────────────────
def _suites():
    seen = []
    for r in REGRAS:
        if r["suite"] not in seen:
            seen.append(r["suite"])
    return seen

def _tipos(suite):
    seen = []
    for r in REGRAS:
        if r["suite"] == suite and r["tipo"] not in seen:
            seen.append(r["tipo"])
    return seen

def _cids(suite, tipo):
    seen = []
    for r in REGRAS:
        if r["suite"] == suite and r["tipo"] == tipo and r["cid"] not in seen:
            seen.append(r["cid"])
    return seen

def _dias_options(suite, tipo, cid):
    return [r["dias"] for r in REGRAS
            if r["suite"] == suite and r["tipo"] == tipo and r["cid"] == cid]

def _find_regra(suite, tipo, cid, dias):
    for r in REGRAS:
        if r["suite"] == suite and r["tipo"] == tipo and r["cid"] == cid and r["dias"] == dias:
            return r
    return None


# ──────────────────────────────────────────────────────────────────────────────
# App
# ──────────────────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Executar Regra de Perícia — Mihmo QA")
        self.minsize(760, 560)
        self.configure(bg="#1e1e2e")

        self._running = False
        self._suite  = tk.StringVar(value="PMV")
        self._tipo   = tk.StringVar()
        self._cid    = tk.StringVar()
        self._dias   = tk.StringVar()

        self._build_ui()
        self._refresh_tipos()

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        PAD = {"padx": 10, "pady": 6}

        # ── topo ──
        top = tk.Frame(self, bg="#313244", pady=10)
        top.pack(fill="x")
        tk.Label(top, text="Perícia Rápida", bg="#313244", fg="#cdd6f4",
                 font=("Segoe UI", 14, "bold")).pack()

        # ── painel principal (esquerda + direita) ──
        main = tk.Frame(self, bg="#1e1e2e")
        main.pack(fill="both", expand=True, padx=14, pady=10)

        left = tk.Frame(main, bg="#1e1e2e", width=300)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        right = tk.Frame(main, bg="#1e1e2e")
        right.pack(side="left", fill="both", expand=True)

        # ── seleções ──
        def lbl(parent, text):
            return tk.Label(parent, text=text, bg="#1e1e2e", fg="#a6adc8",
                            font=("Segoe UI", 9), anchor="w")

        def combo(parent, var, values=(), width=28, state="readonly"):
            c = ttk.Combobox(parent, textvariable=var, values=values,
                             width=width, state=state)
            c.configure(font=("Segoe UI", 10))
            return c

        # Clínica / Suite
        lbl(left, "Clínica (suite)").pack(fill="x", **PAD)
        suite_frame = tk.Frame(left, bg="#1e1e2e")
        suite_frame.pack(fill="x", padx=10)
        for s in _suites():
            tk.Radiobutton(suite_frame, text=s, variable=self._suite, value=s,
                           bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244",
                           activebackground="#1e1e2e", activeforeground="#cdd6f4",
                           font=("Segoe UI", 10), command=self._refresh_tipos
                           ).pack(side="left", padx=4)

        # Tipo
        lbl(left, "Tipo de perícia").pack(fill="x", **PAD)
        self._cb_tipo = combo(left, self._tipo)
        self._cb_tipo.pack(fill="x", padx=10)
        self._cb_tipo.bind("<<ComboboxSelected>>", self._refresh_cids)

        # CID
        lbl(left, "CID").pack(fill="x", **PAD)
        self._cb_cid = combo(left, self._cid)
        self._cb_cid.pack(fill="x", padx=10)
        self._cb_cid.bind("<<ComboboxSelected>>", self._refresh_dias)

        # Duração / Regra
        lbl(left, "Duração").pack(fill="x", **PAD)
        self._cb_dias = combo(left, self._dias)
        self._cb_dias.pack(fill="x", padx=10)
        self._cb_dias.bind("<<ComboboxSelected>>", self._refresh_especialista)

        # Especialista esperado
        sep = tk.Frame(left, bg="#45475a", height=1)
        sep.pack(fill="x", padx=10, pady=10)

        lbl(left, "Especialista esperado").pack(fill="x", padx=10)
        self._lbl_esp = tk.Label(left, text="—", bg="#313244", fg="#a6e3a1",
                                  font=("Segoe UI", 11, "bold"),
                                  anchor="w", relief="flat", padx=8, pady=6)
        self._lbl_esp.pack(fill="x", padx=10, pady=(2, 0))

        self._lbl_junta = tk.Label(left, text="", bg="#1e1e2e", fg="#f38ba8",
                                    font=("Segoe UI", 9, "italic"), anchor="w")
        self._lbl_junta.pack(fill="x", padx=10)

        # Botões
        sep2 = tk.Frame(left, bg="#45475a", height=1)
        sep2.pack(fill="x", padx=10, pady=10)

        self._btn = tk.Button(left, text="▶  Executar",
                              command=self._executar,
                              bg="#89b4fa", fg="#1e1e2e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat", cursor="hand2",
                              padx=10, pady=8, activebackground="#74c7ec")
        self._btn.pack(fill="x", padx=10)

        tk.Button(left, text="Limpar saída", command=self._limpar,
                  bg="#313244", fg="#a6adc8",
                  font=("Segoe UI", 9), relief="flat", cursor="hand2",
                  pady=4).pack(fill="x", padx=10, pady=(6, 0))

        # ── output ──
        tk.Label(right, text="Saída", bg="#1e1e2e", fg="#a6adc8",
                 font=("Segoe UI", 9)).pack(anchor="w")
        self._out = scrolledtext.ScrolledText(
            right, bg="#11111b", fg="#cdd6f4",
            font=("Consolas", 9), relief="flat",
            insertbackground="#cdd6f4", wrap="word",
            state="disabled"
        )
        self._out.pack(fill="both", expand=True)
        self._out.tag_config("ok",    foreground="#a6e3a1")
        self._out.tag_config("erro",  foreground="#f38ba8")
        self._out.tag_config("info",  foreground="#89b4fa")
        self._out.tag_config("aviso", foreground="#f9e2af")

    # ── Cascata de filtros ────────────────────────────────────────────────────
    def _refresh_tipos(self, *_):
        tipos = _tipos(self._suite.get())
        self._cb_tipo["values"] = tipos
        self._tipo.set(tipos[0] if tipos else "")
        self._refresh_cids()

    def _refresh_cids(self, *_):
        cids = _cids(self._suite.get(), self._tipo.get())
        self._cb_cid["values"] = cids
        self._cid.set(cids[0] if cids else "")
        # ocultar CID se só há opção "—"
        if cids == ["—"]:
            self._cb_cid.configure(state="disabled")
        else:
            self._cb_cid.configure(state="readonly")
        self._refresh_dias()

    def _refresh_dias(self, *_):
        opts = _dias_options(self._suite.get(), self._tipo.get(), self._cid.get())
        self._cb_dias["values"] = opts
        self._dias.set(opts[0] if opts else "")
        self._refresh_especialista()

    def _refresh_especialista(self, *_):
        r = _find_regra(self._suite.get(), self._tipo.get(),
                        self._cid.get(), self._dias.get())
        if r:
            self._lbl_esp.configure(text=r["especialista"])
            self._lbl_junta.configure(
                text="⚠ Junta Médica" if r["junta"] else "")
        else:
            self._lbl_esp.configure(text="—")
            self._lbl_junta.configure(text="")

    # ── Execução ──────────────────────────────────────────────────────────────
    def _executar(self):
        if self._running:
            return
        r = _find_regra(self._suite.get(), self._tipo.get(),
                        self._cid.get(), self._dias.get())
        if not r:
            self._log("Nenhuma regra selecionada.\n", "erro")
            return

        self._running = True
        self._btn.configure(state="disabled", text="Executando...")
        threading.Thread(target=self._run_regra, args=(r,), daemon=True).start()

    def _run_regra(self, r):
        self._log(f"\n{'═'*60}\n", "info")
        self._log(f"  Suite    : {r['suite']}\n", "info")
        self._log(f"  Tipo     : {r['tipo']}\n", "info")
        self._log(f"  CID      : {r['cid']}\n", "info")
        self._log(f"  Duração  : {r['dias']}\n", "info")
        self._log(f"  Esperado : {r['especialista']}"
                  + (" (Junta)" if r["junta"] else "") + "\n", "info")
        self._log(f"{'═'*60}\n\n", "info")

        # ── Limpar massa anterior ──
        massa_file = os.path.join(ROOT, "results", "massa_criada.json")
        if os.path.exists(massa_file):
            os.remove(massa_file)
            self._log("  massa_criada.json limpo.\n\n", "aviso")

        # ── Fase 1: Criar Massa ──
        ok = self._run_robot(r["setup_file"], r["setup_test"], "CRIAR MASSA")

        # ── Fase 2: Homologação ──
        if ok and r["homolog_file"]:
            self._run_robot(r["homolog_file"], r["homolog_test"], "HOMOLOGAÇÃO")
        elif not r["homolog_file"]:
            self._log("\n[!] Este tipo não possui teste de homologação.\n", "aviso")

        self.after(0, self._finalizar)

    def _run_robot(self, rel_file, test_name, fase):
        listener = "resources/keywords/console_listener.py"
        cmd = ["robot", "--outputdir", "results",
               "--listener", listener,
               "--test", test_name, rel_file]

        self._log(f"\n── {fase} ──────────────────────────────────────\n", "aviso")
        self._log(f"$ robot --test \"{test_name}\"\n\n", "info")

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=ROOT,
                encoding="utf-8",
                errors="replace",
            )
        except FileNotFoundError:
            self._log("ERRO: 'robot' não encontrado no PATH.\n", "erro")
            return False

        for line in proc.stdout:
            tag = None
            low = line.lower()
            if "→" in line:
                tag = "info"
            elif "| pass |" in low or "passed" in low:
                tag = "ok"
            elif "| fail |" in low or "failed" in low or "error" in low:
                tag = "erro"
            self._log(line, tag)

        proc.wait()
        success = proc.returncode == 0
        if success:
            self._log(f"\n✔ {fase} concluída com sucesso.\n", "ok")
        else:
            self._log(f"\n✘ {fase} falhou (código {proc.returncode}).\n", "erro")
        return success

    def _finalizar(self):
        self._running = False
        self._btn.configure(state="normal", text="▶  Executar")

    # ── Helpers de output ─────────────────────────────────────────────────────
    def _log(self, text, tag=None):
        self.after(0, self._append, text, tag)

    def _append(self, text, tag):
        self._out.configure(state="normal")
        if tag:
            self._out.insert("end", text, tag)
        else:
            self._out.insert("end", text)
        self._out.see("end")
        self._out.configure(state="disabled")

    def _limpar(self):
        self._out.configure(state="normal")
        self._out.delete("1.0", "end")
        self._out.configure(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()
