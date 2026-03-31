from unittest.mock import patch, MagicMock
import scripts.log_app as log_app

def test_enviar_log_sucesso():
    log = {
        "timestamp": "2025-01-27 10:00:00",
        "level": "INFO",
        "message": "Teste",
        "service": "test-service"
    }
    with patch("scripts.log_app.requests.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=201)
        mock_post.return_value.raise_for_status = lambda: None
        log_app.enviar_log(log)
        mock_post.assert_called_once()

def test_enviar_log_api_fora(tmp_path, monkeypatch):
    monkeypatch.setattr(log_app, "FALLBACK_FILE", str(tmp_path / "fallback.jsonl"))

    log = {
        "timestamp": "2025-01-27 10:00:00",
        "level": "ERROR",
        "message": "Teste fallback",
        "service": "test-service"
    }
    with patch("scripts.log_app.requests.post", side_effect=Exception("API fora")):
        log_app.enviar_log(log)

    conteudo = open(str(tmp_path / "fallback.jsonl")).read()
    assert "Teste fallback" in conteudo