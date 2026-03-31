import logging
import json
import random
import time
from datetime import datetime
import requests

FLASK_URL = "http://localhost:5000/logs"
FALLBACK_FILE = "./data/logs_fallback.jsonl"


def enviar_log(log: dict):
    try:
        response = requests.post(FLASK_URL, json=log, timeout=2)
        response.raise_for_status()
    except Exception as e:
        print(f"API fora do ar, salvando localmente: {e}")
        with open(FALLBACK_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")


levels = ["INFO", "WARNING", "ERROR", "DEBUG"]

messages = [
    "Usuário autenticado",
    "Falha ao conectar ao banco",
    "Timeout na requisição",
    "Arquivo carregado com sucesso",
    "Erro interno no servidor",
    "Nova conexão recebida",
    "Permissão negada para usuário",
    "Sessão expirada"
]

print("Gerando logs... (Ctrl+C para parar)")

while True:
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": random.choice(levels),
        "message": random.choice(messages),
        "service": random.choice(["auth-service", "api", "worker", "database"])
    }

    enviar_log(log)
    time.sleep(random.uniform(0.5, 2))