import pytest
from unittest.mock import patch
from src.extract.extract_devs import extrair_todos_devs

@pytest.fixture
def mock_jira_devs():
    return [
        {
            "fields": {
                "assignee": {
                    "displayName": "Vinicius Monteiro"
                }
            }
        },
        {
            "fields": {
                "assignee": {
                    "displayName": "Maria Silva"
                }
            }
        },
        {
            "fields": {
                "assignee": None  
            }
        },
        {
            "fields": {
                "assignee": {
                    "displayName": None  
                }
            }
        }
    ]

def test_extrair_todos_devs(mock_jira_devs):
    resultado = extrair_todos_devs(mock_jira_devs)

    assert len(resultado) == 2
    assert resultado[0] == {"nome": "Vinicius Monteiro"}
    assert resultado[1] == {"nome": "Maria Silva"}

    for dev in resultado:
        assert isinstance(dev["nome"], str)


@patch("src.extract.extract_devs.logger")
def test_extrair_todos_devs_com_erro(mock_logger):
    devs_invalidos = [
        {"fields": None}
    ]

    resultado = extrair_todos_devs(devs_invalidos)

    assert resultado == []
    assert mock_logger.warning.called
