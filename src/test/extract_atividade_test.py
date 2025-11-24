import pytest
from unittest.mock import patch
from src.extract.extract_atividades import extrair_atividades

@pytest.fixture
def mock_jira_issues():
    return [
        {
            "id": "101",
            "fields": {
                "summary": "Criar endpoint de login",
                "description": "Implementar autenticação JWT",
                "status": {"name": "Em andamento"}
            }
        },
        {
            "id": "102",
            "fields": {
                "summary": None,
                "description": None,
                "status": {"name": "Concluído"}
            }
        },
        {
            "id": "103",
            "fields": {
                "status": {"name": "A Fazer"}
            }
        }
    ]


def test_extrair_atividades(mock_jira_issues):
    resultado = extrair_atividades(mock_jira_issues)

    assert len(resultado) == 3

    assert resultado[0]["nome"] == "Criar endpoint de login"
    assert resultado[0]["descricao"] == "Implementar autenticação JWT"
    assert resultado[0]["atividade_jira_id"] == "101"
    assert resultado[0]["ativo"] is True 

    assert resultado[1]["nome"] == "Atividade sem Título"
    assert resultado[1]["descricao"] == "Descrição não fornecida"
    assert resultado[1]["ativo"] is False

    assert resultado[2]["nome"] == "Atividade sem Título"
    assert resultado[2]["descricao"] == "Descrição não fornecida"
    assert resultado[2]["ativo"] is True


@patch("src.extract.extract_atividades.logger")
def test_extrair_atividades_com_erro(mock_logger):
    issues = [
        {
            "fields": None
        }
    ]

    resultado = extrair_atividades(issues)

    assert resultado == []
    assert mock_logger.warning.called
