import pytest
import os
import sqlite3
os.environ["DB_PATH"] = ":memory:"

from app import database
from app.database import criar_tabela, inserir_log, buscar_logs, buscar_logs_after_id

@pytest.fixture(autouse=True)
def banco():
    # força uma conexão persistente durante o teste
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    database._conn_teste = conn
    database.get_connection = lambda: conn
    criar_tabela()
    yield
    conn.close()
    
def test_inserir_e_buscar_log(banco):
    log = {
        "timestamp": "2025-01-27 10:00:00",
        "level": "INFO",
        "message": "Teste de inserção",
        "service": "test-service"
    }
    inserir_log(log)
    resultado = buscar_logs(data="2025-01-27")
    assert len(resultado) == 1
    assert resultado[0]["message"] == "Teste de inserção"

def test_buscar_after_id(banco):
    for i in range(3):
        inserir_log({
            "timestamp": "2025-01-27 10:00:00",
            "level": "INFO",
            "message": f"Log {i}",
            "service": "test-service"
        })
    resultado = buscar_logs_after_id(1)
    assert len(resultado) == 2