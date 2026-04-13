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
# Categorias
# ──────────────────────────────────────────────────────────────────────────────
# Sentinels para categorias com suite fixa (independem do radio selecionado)
_PMV       = object()
_PPV       = object()
_PMV_PPV   = object()

CATEGORIAS_DEF = [
    ("Todas PMV",          _PMV),
    ("Todas PPV",          _PPV),
    ("Todas (PMV + PPV)",  _PMV_PPV),
    ("Todas as Juntas",    lambda r: r["junta"]),
    ("Médico Trabalho",    lambda r: r["especialista"] == "Médico Trabalho"),
    ("Clínico Geral",      lambda r: "Clínico Geral" in r["especialista"] and not r["junta"]),
    ("Ortopedista",        lambda r: "Ortopedista" in r["especialista"] and not r["junta"]),
    ("Psiquiatra",         lambda r: "Psiquiatra" in r["especialista"] and not r["junta"]),
    ("Assistente Social",  lambda r: "Assistente Social" in r["especialista"]),
]

def _resolve_regras(suite, fn):
    if fn is _PMV:      return [r for r in REGRAS if r["suite"] == "PMV"]
    if fn is _PPV:      return [r for r in REGRAS if r["suite"] == "PPV"]
    if fn is _PMV_PPV:  return list(REGRAS)
    return [r for r in REGRAS if r["suite"] == suite and fn(r)]

def _categorias_disponiveis(suite):
    result = []
    for nome, fn in CATEGORIAS_DEF:
        matching = _resolve_regras(suite, fn)
        if matching:
            result.append((nome, len(matching)))
    return result

def _regras_da_categoria(suite, categ_nome):
    entry = next(((n, fn) for n, fn in CATEGORIAS_DEF if n == categ_nome), None)
    if entry is None:
        return []
    return _resolve_regras(suite, entry[1])


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
        self._proc   = None          # subprocess atual do robot
        self._suite  = tk.StringVar(value="PMV")
        self._tipo   = tk.StringVar()
        self._cid    = tk.StringVar()
        self._dias   = tk.StringVar()
        self._modo   = tk.StringVar(value="individual")
        self._categ  = tk.StringVar()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._refresh_tipos()
        self._refresh_categorias()

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

        # helpers
        def lbl(parent, text):
            return tk.Label(parent, text=text, bg="#1e1e2e", fg="#a6adc8",
                            font=("Segoe UI", 9), anchor="w")

        def combo(parent, var, values=(), width=28, state="readonly"):
            c = ttk.Combobox(parent, textvariable=var, values=values,
                             width=width, state=state)
            c.configure(font=("Segoe UI", 10))
            return c

        # ── Modo toggle ──────────────────────────────────────────────────────
        lbl(left, "Modo").pack(fill="x", **PAD)
        modo_frame = tk.Frame(left, bg="#1e1e2e")
        modo_frame.pack(fill="x", padx=10)
        for val, txt in [("individual", "Regra Individual"), ("categoria", "Por Categoria")]:
            tk.Radiobutton(modo_frame, text=txt, variable=self._modo, value=val,
                           bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244",
                           activebackground="#1e1e2e", activeforeground="#cdd6f4",
                           font=("Segoe UI", 10), command=self._on_modo_change
                           ).pack(side="left", padx=4)

        tk.Frame(left, bg="#45475a", height=1).pack(fill="x", padx=10, pady=8)

        # ── Clínica / Suite (compartilhada entre modos) ──────────────────────
        lbl(left, "Clínica (suite)").pack(fill="x", padx=10)
        suite_frame = tk.Frame(left, bg="#1e1e2e")
        suite_frame.pack(fill="x", padx=10, pady=(2, 8))
        for s in _suites():
            tk.Radiobutton(suite_frame, text=s, variable=self._suite, value=s,
                           bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244",
                           activebackground="#1e1e2e", activeforeground="#cdd6f4",
                           font=("Segoe UI", 10), command=self._on_suite_change
                           ).pack(side="left", padx=4)

        # ── Container que segura o frame de modo (fica sempre acima dos botões) ──
        self._frm_modo_holder = tk.Frame(left, bg="#1e1e2e")
        self._frm_modo_holder.pack(fill="x")

        # ── Frame Individual ─────────────────────────────────────────────────
        self._frm_individual = tk.Frame(self._frm_modo_holder, bg="#1e1e2e")

        lbl(self._frm_individual, "Tipo de perícia").pack(fill="x", **PAD)
        self._cb_tipo = combo(self._frm_individual, self._tipo)
        self._cb_tipo.pack(fill="x", padx=10)
        self._cb_tipo.bind("<<ComboboxSelected>>", self._refresh_cids)

        lbl(self._frm_individual, "CID").pack(fill="x", **PAD)
        self._cb_cid = combo(self._frm_individual, self._cid)
        self._cb_cid.pack(fill="x", padx=10)
        self._cb_cid.bind("<<ComboboxSelected>>", self._refresh_dias)

        lbl(self._frm_individual, "Duração").pack(fill="x", **PAD)
        self._cb_dias = combo(self._frm_individual, self._dias)
        self._cb_dias.pack(fill="x", padx=10)
        self._cb_dias.bind("<<ComboboxSelected>>", self._refresh_especialista)

        tk.Frame(self._frm_individual, bg="#45475a", height=1).pack(
            fill="x", padx=10, pady=10)
        lbl(self._frm_individual, "Especialista esperado").pack(fill="x", padx=10)
        self._lbl_esp = tk.Label(self._frm_individual, text="—",
                                  bg="#313244", fg="#a6e3a1",
                                  font=("Segoe UI", 11, "bold"),
                                  anchor="w", relief="flat", padx=8, pady=6)
        self._lbl_esp.pack(fill="x", padx=10, pady=(2, 0))
        self._lbl_junta = tk.Label(self._frm_individual, text="",
                                    bg="#1e1e2e", fg="#f38ba8",
                                    font=("Segoe UI", 9, "italic"), anchor="w")
        self._lbl_junta.pack(fill="x", padx=10)

        # ── Frame Categoria ──────────────────────────────────────────────────
        self._frm_categoria = tk.Frame(self._frm_modo_holder, bg="#1e1e2e")

        lbl(self._frm_categoria, "Categoria").pack(fill="x", **PAD)
        self._cb_categ = combo(self._frm_categoria, self._categ)
        self._cb_categ.pack(fill="x", padx=10)
        self._cb_categ.bind("<<ComboboxSelected>>", self._update_cat_count)

        self._lbl_cat_count = tk.Label(self._frm_categoria, text="",
                                        bg="#1e1e2e", fg="#a6adc8",
                                        font=("Segoe UI", 9, "italic"), anchor="w")
        self._lbl_cat_count.pack(fill="x", padx=12, pady=(4, 0))

        # Exibe o frame do modo inicial (individual)
        self._frm_individual.pack(fill="x")

        # ── Botões (sempre abaixo dos frames de modo) ─────────────────────────
        tk.Frame(left, bg="#45475a", height=1).pack(fill="x", padx=10, pady=10)

        self._btn = tk.Button(left, text="▶  Executar",
                              command=self._executar,
                              bg="#89b4fa", fg="#1e1e2e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat", cursor="hand2",
                              padx=10, pady=8, activebackground="#74c7ec")
        self._btn.pack(fill="x", padx=10)

        self._btn_parar = tk.Button(left, text="⏹  Parar",
                                    command=self._parar,
                                    bg="#f38ba8", fg="#1e1e2e",
                                    font=("Segoe UI", 11, "bold"),
                                    relief="flat", cursor="hand2",
                                    padx=10, pady=8, activebackground="#eba0ac")
        # aparece só durante execução

        tk.Button(left, text="Limpar saída", command=self._limpar,
                  bg="#313244", fg="#a6adc8",
                  font=("Segoe UI", 9), relief="flat", cursor="hand2",
                  pady=4).pack(fill="x", padx=10, pady=(6, 0))

        # ── output ──────────────────────────────────────────────────────────
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

    # ── Modo ─────────────────────────────────────────────────────────────────
    def _on_modo_change(self, *_):
        if self._modo.get() == "individual":
            self._frm_categoria.pack_forget()
            self._frm_individual.pack(fill="x")
        else:
            self._frm_individual.pack_forget()
            self._frm_categoria.pack(fill="x")
        self._refresh_categorias()

    def _on_suite_change(self, *_):
        self._refresh_tipos()
        self._refresh_categorias()

    # ── Categoria ─────────────────────────────────────────────────────────────
    def _refresh_categorias(self, *_):
        cats = _categorias_disponiveis(self._suite.get())
        labels = [f"{nome}  ({qtd} regra{'s' if qtd > 1 else ''})" for nome, qtd in cats]
        self._cb_categ["values"] = labels
        if labels:
            self._cb_categ.current(0)
            self._categ.set(labels[0])
        self._update_cat_count()

    def _update_cat_count(self, *_):
        nome = self._categ.get().split("  (")[0]  # remove "(X regras)"
        regras = _regras_da_categoria(self._suite.get(), nome)
        if regras:
            specs = sorted({r["especialista"] for r in regras})
            self._lbl_cat_count.configure(
                text=f"{len(regras)} regras → {', '.join(specs)}")
        else:
            self._lbl_cat_count.configure(text="")

    # ── Cascata de filtros (modo individual) ──────────────────────────────────
    def _refresh_tipos(self, *_):
        tipos = _tipos(self._suite.get())
        self._cb_tipo["values"] = tipos
        self._tipo.set(tipos[0] if tipos else "")
        self._refresh_cids()

    def _refresh_cids(self, *_):
        cids = _cids(self._suite.get(), self._tipo.get())
        self._cb_cid["values"] = cids
        self._cid.set(cids[0] if cids else "")
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
        self._running = True
        self._btn.pack_forget()
        self._btn_parar.pack(fill="x", padx=10)

        if self._modo.get() == "categoria":
            nome = self._categ.get().split("  (")[0]
            regras = _regras_da_categoria(self._suite.get(), nome)
            if not regras:
                self._log("Nenhuma regra na categoria selecionada.\n", "erro")
                self.after(0, self._finalizar)
                return
            threading.Thread(target=self._run_lista,
                             args=(regras, nome), daemon=True).start()
        else:
            r = _find_regra(self._suite.get(), self._tipo.get(),
                            self._cid.get(), self._dias.get())
            if not r:
                self._log("Nenhuma regra selecionada.\n", "erro")
                self.after(0, self._finalizar)
                return
            threading.Thread(target=self._run_regra, args=(r,), daemon=True).start()

    # ── Execução: lista de regras (modo categoria) ────────────────────────────
    def _run_lista(self, regras, nome_cat):
        self._log(f"\n{'═'*60}\n", "info")
        self._log(f"  Categoria : {nome_cat}\n", "info")
        self._log(f"  Suite     : {self._suite.get()}\n", "info")
        self._log(f"  Regras    : {len(regras)}\n", "info")
        self._log(f"{'═'*60}\n\n", "info")

        # Limpar massa
        massa_file = os.path.join(ROOT, "results", "massa_criada.json")
        if os.path.exists(massa_file):
            os.remove(massa_file)
            self._log("  massa_criada.json limpo.\n\n", "aviso")

        # Agrupar por arquivo de setup (pode haver PMV e PPV misturados no "Todas")
        from collections import defaultdict
        setup_grupos  = defaultdict(list)
        homolog_grupos = defaultdict(list)
        for r in regras:
            setup_grupos[r["setup_file"]].append(r["setup_test"])
            if r["homolog_file"]:
                homolog_grupos[r["homolog_file"]].append(r["homolog_test"])

        # Fase 1: todos os criar_massa
        ok = True
        for arquivo, testes in setup_grupos.items():
            label = f"CRIAR MASSA ({len(testes)} testes)"
            ok = self._run_robot_multi(arquivo, testes, label) and ok

        # Fase 2: todos os homologação
        if ok:
            for arquivo, testes in homolog_grupos.items():
                label = f"HOMOLOGAÇÃO ({len(testes)} testes)"
                self._run_robot_multi(arquivo, testes, label)

        self.after(0, self._finalizar)

    def _run_robot_multi(self, rel_file, test_names, fase):
        """Roda robot com múltiplos --test em uma única invocação."""
        listener = "resources/keywords/console_listener.py"
        cmd = ["robot", "--outputdir", "results", "--listener", listener]
        for tn in test_names:
            cmd += ["--test", tn]
        cmd.append(rel_file)

        self._log(f"\n── {fase} ──────────────────────────────────────\n", "aviso")
        self._log(f"  {len(test_names)} testes · {rel_file}\n\n", "info")

        try:
            self._proc = subprocess.Popen(
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

        proc = self._proc
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
            self._proc = subprocess.Popen(
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

        proc = self._proc
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

    def _parar(self):
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=3)
            except Exception:
                self._proc.kill()
        self._log("\n⏹ Execução interrompida pelo usuário.\n", "erro")
        self._finalizar()

    def _on_close(self):
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=3)
            except Exception:
                self._proc.kill()
        self.destroy()

    def _finalizar(self):
        self._running = False
        self._proc = None
        self._btn_parar.pack_forget()
        self._btn.pack(fill="x", padx=10)

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
