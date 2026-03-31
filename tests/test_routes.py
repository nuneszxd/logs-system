import pytest
import os
os.environ["DB_PATH"] = ":memory:"

from app.routes import app
from app.database import criar_tabela

@pytest.fixture
def client():
    import sqlite3
    from app import database

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    database.get_connection = lambda: conn
    criar_tabela()

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

    conn.close()

def test_post_log_valido(client):
    response = client.post("/logs", json={
        "timestamp": "2025-01-27 10:00:00",
        "level": "INFO",
        "message": "Teste via rota",
        "service": "test-service"
    })
    assert response.status_code == 201
    assert response.get_json()["status"] == "ok"

def test_post_log_campo_faltando(client):
    response = client.post("/logs", json={
        "timestamp": "2025-01-27 10:00:00",
        "level": "INFO"
    })
    assert response.status_code == 400

def test_post_log_body_vazio(client):
    response = client.post("/logs", content_type="application/json", data="")
    assert response.status_code == 400

def test_get_logs(client):
    client.post("/logs", json={
        "timestamp": "2025-01-27 10:00:00",
        "level": "INFO",
        "message": "Log pra buscar",
        "service": "test-service"
    })
    response = client.get("/logs?date=2025-01-27")
    assert response.status_code == 200
    assert len(response.get_json()) == 1