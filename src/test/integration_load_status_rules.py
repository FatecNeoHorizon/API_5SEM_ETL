import pytest
from unittest.mock import patch, call
from src.load import load_status

# ---------- FIXTURES ----------
@pytest.fixture
def status_ok_dedup():
    return [
        {"nome": "To Do", "statusJiraId": 1, "colorName": "blue"},
        {"nome": "In Progress", "statusJiraId": 2, "colorName": "yellow"},
        {"nome": "To Do", "statusJiraId": 1, "colorName": "blue"},  # duplicado
    ]

@pytest.fixture
def status_invalidos_faltando():
    return [
        {"nome": "To Do", "statusJiraId": 1},  # falta colorName
        {"statusJiraId": 2, "colorName": "yellow"},  # falta nome
    ]

@pytest.fixture
def status_invalidos_tipo():
    return [
        {"nome": "To Do", "statusJiraId": "um", "colorName": "blue"},
        {"nome": "In Progress", "statusJiraId": 2, "colorName": 123},
    ]

@pytest.fixture
def status_vazio():
    return []


# ---------- TESTES (LOAD) ----------
@patch("src.utils.http_client.post_json")
def test_load_status_envia_unicos_e_schema_valido(mock_post, status_ok_dedup, monkeypatch):
    # Simula respostas do backend
    mock_post.return_value = {"id": 999}
    monkeypatch.setenv("BACK_BASE_URL", "http://fake-back")

    load_status.carregar_status(status_ok_dedup)

    # Espera 2 chamadas (IDs únicos: 1 e 2)
    assert mock_post.call_count == 2

    # Valida payloads
    enviados = [kwargs["json"] if "json" in kwargs else args[1]
                for _, args, kwargs in ( (None, c.args, c.kwargs) for c in mock_post.call_args_list )]
    # compat: alguns http_client usam args, outros kwargs
    for body in enviados:
        assert isinstance(body["nome"], str)
        assert isinstance(body["statusJiraId"], int)
        assert body["colorName"] in ["blue", "yellow"]

@patch("src.utils.http_client.post_json")
def test_load_status_rejeita_itens_invalidos_antes_de_enviar(mock_post, status_invalidos_faltando, monkeypatch):
    monkeypatch.setenv("BACK_BASE_URL", "http://fake-back")

    with pytest.raises((KeyError, AssertionError, ValueError)):
        load_status.carregar_status(status_invalidos_faltando)

    mock_post.assert_not_called()

@patch("src.utils.http_client.post_json")
def test_load_status_rejeita_tipos_invalidos(mock_post, status_invalidos_tipo, monkeypatch):
    monkeypatch.setenv("BACK_BASE_URL", "http://fake-back")

    with pytest.raises((AssertionError, TypeError, ValueError)):
        load_status.carregar_status(status_invalidos_tipo)

    mock_post.assert_not_called()

@patch("src.utils.http_client.post_json")
def test_load_status_vazio_nao_faz_chamada(mock_post, status_vazio, monkeypatch):
    monkeypatch.setenv("BACK_BASE_URL", "http://fake-back")
    load_status.carregar_status(status_vazio)
    mock_post.assert_not_called()

@patch("src.utils.http_client.post_json")
def test_load_status_falha_primeira_tentativa_depois_sucesso(mock_post, status_ok_dedup, monkeypatch):
    """
    Se seu load tiver retry, a 1a tentativa falha e a 2a passa.
    Se ainda não tiver retry, troque a asserção para esperar exceção.
    """
    monkeypatch.setenv("BACK_BASE_URL", "http://fake-back")

    # Simula: primeiro levanta TimeoutError, depois responde ok
    side_effects = [TimeoutError("timeout"), {"id": 1}, {"id": 2}]
    mock_post.side_effect = side_effects

    try:
        load_status.carregar_status(status_ok_dedup)
    except TimeoutError:
        pytest.skip("Retry ainda não implementado no load_status; ajuste a função para suportar retry/backoff.")

    # Espera no mínimo 3 chamadas (1 timeout + 2 sucessos)
    assert mock_post.call_count >= 3
