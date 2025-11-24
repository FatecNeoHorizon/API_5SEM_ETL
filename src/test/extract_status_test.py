import pytest
from unittest.mock import patch
from src.extract.extract_status import extrair_todos_status

@pytest.fixture
def mock_jira_issues():
    return [
        {
            "fields": {
                "statusCategory": {
                    "id": 1,
                    "name": "To Do"
                }
            }
        },
        {
            "fields": {
                "statusCategory": {
                    "id": 2,
                    "name": "In Progress"
                }
            }
        },
        {
            "fields": {
                "statusCategory": {
                    "id": 3,
                    "name": "Done"
                }
            }
        },
    ]


def test_extrair_todos_status(mock_jira_issues):
    resultado = extrair_todos_status(mock_jira_issues)

    assert len(resultado) == 3

    assert resultado[0] == {"nome": "To Do", "statusJiraId": 1}
    assert resultado[1] == {"nome": "In Progress", "statusJiraId": 2}
    assert resultado[2] == {"nome": "Done", "statusJiraId": 3}

    for status in resultado:
        assert isinstance(status["nome"], str)
        assert isinstance(status["statusJiraId"], int)

@patch("src.extract.extract_status.logger")
def test_extrair_todos_status_com_erro(mock_logger):
    jira_issues_invalidos = [
        {"fields": None}
    ]

    resultado = extrair_todos_status(jira_issues_invalidos)

    assert resultado == []
    assert mock_logger.warning.called
