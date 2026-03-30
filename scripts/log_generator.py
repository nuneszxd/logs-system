import logging
import json
import random
import time
from datetime import datetime

# Criar logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Criar handler para arquivo JSON
file_handler = logging.FileHandler(".\data\logs.jsonl", encoding="utf-8")

# Formatter JSON
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": random.choice([
                "auth-service",
                "api",
                "worker",
                "database"
            ])
        }

        return json.dumps(log_record, ensure_ascii=False)

file_handler.setFormatter(JsonFormatter())

logger.addHandler(file_handler)

levels = [
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.DEBUG
]

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

print("Gerando logs JSON... (Ctrl+C para parar)")

while True:
    level = random.choice(levels)
    message = random.choice(messages)

    logger.log(level, message)

    time.sleep(random.uniform(0.5, 2))