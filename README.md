# 📋 Logs System

Sistema leve de coleta e visualização de logs em tempo real, containerizado com Docker e com interface web estilo terminal.

Desenvolvido para monitoramento de serviços em produção, com persistência de 3 dias e visualização por data.

---

## 🖥️ Interface

> Página estilo terminal com atualização automática, filtro por dia e scroll inteligente que não interrompe a navegação durante debug.

---

## 🏗️ Arquitetura

```
app_logs ──► POST /logs ──► API Flask ──► SQLite ──► UI Web
                                 │
                            API fora do ar?
                                 │
                         salva em fallback local
```

Cada serviço envia seus próprios logs diretamente para a API via HTTP — sem agente externo, sem leitura de socket.

---

## ⚙️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.11 | Backend e gerador de logs |
| Flask | API REST e servidor web |
| SQLite | Persistência leve (sem servidor) |
| Docker + Compose | Containerização e orquestração |
| HTML + JS (Vanilla) | Interface web sem frameworks |

---

## 📁 Estrutura

```
logs-system/
├── app/
│   ├── routes.py          # rotas da API e servidor web
│   ├── database.py        # conexão e queries SQLite
│   └── templates/
│       └── index.html     # interface web
├── scripts/
│   └── log_generator.py   # gerador de logs para testes locais
├── data/
│   └── .gitkeep           # pasta criada no deploy, não versionada
├── log_app.py             # serviço simulado que envia logs
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## 🚀 Como rodar

### Pré-requisitos

- [Docker](https://www.docker.com/) instalado
- [Docker Compose](https://docs.docker.com/compose/) disponível

### 1. Clone o repositório

```bash
git clone https://github.com/nuneszxd/logs-system.git
cd logs-system
```

### 2. Suba os containers

```bash
docker compose up --build
```

### 3. Acesse a interface

```
http://localhost:5000
```

Pronto. Os logs começam a aparecer automaticamente em tempo real.

---

## 🔌 API

### Enviar log

```http
POST /logs
Content-Type: application/json

{
  "timestamp": "2025-01-27 10:00:00",
  "level": "INFO",
  "message": "Usuário autenticado",
  "service": "auth-service"
}
```

**Níveis aceitos:** `INFO` `WARNING` `ERROR` `DEBUG`

**Resposta:**
```json
{ "status": "ok" }
```

### Buscar logs

```http
GET /logs                        # últimos 50 logs
GET /logs?date=2025-01-27        # todos os logs do dia
GET /logs?after_id=150           # logs após o ID 150 (usado pelo frontend)
```

---

## 🔧 Integrar seu serviço

Para enviar logs do seu próprio serviço, basta fazer um `POST /logs` com o payload acima.

Exemplo em Python:

```python
import requests
from datetime import datetime

def enviar_log(message: str, level: str = "INFO", service: str = "meu-servico"):
    requests.post("http://api:5000/logs", json={
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "message": message,
        "service": service
    }, timeout=2)
```

---

## 🗄️ Dados

- Logs ficam armazenados por **3 dias** em SQLite
- Limpeza automática executada diariamente à meia-noite
- Em caso de falha na API, logs são salvos localmente em `data/logs_fallback.jsonl`
- A pasta `data/` não é versionada — é criada automaticamente no primeiro uso

---

## 🧪 Testando localmente sem Docker

```bash
# instale as dependências
pip install -r requirements.txt

# terminal 1 — sobe a API
python -m app.routes

# terminal 2 — gera logs de teste
python -m scripts.log_generator
```

---

## 📌 Decisões técnicas

**Por que SQLite?**
Leve, sem servidor, arquivo único fácil de fazer backup. Para o volume de logs desse sistema (dezenas por minuto), performa perfeitamente.

**Por que sem collector externo?**
Cada serviço envia seus próprios logs via HTTP. É o padrão da indústria — mais simples, mais resiliente e funciona em qualquer ambiente.

**Por que fallback em arquivo?**
Logs não podem se perder. Se a API estiver fora do ar, o serviço continua operando e salva localmente até a API voltar.