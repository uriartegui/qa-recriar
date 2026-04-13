"""
Robot Framework Listener v2 — imprime mensagens amigáveis no stdout
conforme as keywords relevantes são executadas (feedback em tempo real).
"""
import sys

KEYWORD_MESSAGES = {
    "Autenticar No Mihmo":       "  → Autenticando no Mihmo...",
    "Criar Customer":            "  → Criando customer (mihmado)...",
    "Criar Pericia Api":         "  → Criando perícia e enviando atestado...",
    "Verificar Especialista Api":"  → Verificando especialista na fila da clínica...",
    "Enviar Para Fila":          "  → Enviando para fila do médico...",
    "Homologar Pericia":         "  → Homologando e finalizando atendimento...",
}


class ConsoleListener:
    ROBOT_LISTENER_API_VERSION = 2

    def start_keyword(self, name, attrs):
        kwname = attrs.get("kwname", name)
        msg = KEYWORD_MESSAGES.get(kwname)
        if msg:
            print(msg, flush=True)

    # ── métodos obrigatórios (sem uso) ──────────────────────────────────────
    def end_keyword(self, name, attrs):   pass
    def start_test(self, name, attrs):    pass
    def end_test(self, name, attrs):      pass
    def start_suite(self, name, attrs):   pass
    def end_suite(self, name, attrs):     pass
    def log_message(self, message):       pass
    def close(self):                      pass
