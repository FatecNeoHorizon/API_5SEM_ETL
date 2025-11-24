import pytest
from unittest.mock import patch
from src.extract.extract_periodos import extrair_periodos

@pytest.fixture
def mock_jira_issues():
    return [
        {
            "fields": {
                "worklog": {
                    "worklogs": [
                        {"started": "2025-01-01T10:00:00.000-0300"}
                    ]
                }
            }
        },
        {
            "fields": {
                "worklog": {
                    "worklogs": [
                        {"started": "2025-02-15T14:30:00.000-0300"}
                    ]
                }
            }
        },
        {
            "fields": {
                "worklog": {
                    "worklogs": []
                }
            }
        }
    ]

@patch("src.extract.extract_periodos.convert_datetime_to_periodo")
def test_extrair_periodos(mock_convert, mock_jira_issues):
    mock_convert.side_effect = ["2025-01", "2025-02"]

    resultado = extrair_periodos(mock_jira_issues)

    assert len(resultado) == 2

    assert resultado[0] == "2025-01"
    assert resultado[1] == "2025-02"

    assert mock_convert.call_count == 2
    
@patch("src.extract.extract_periodos.logger")
def test_extrair_periodos_com_erro(mock_logger):
    issues_invalidas = [
        {
            "fields": None
        }
    ]

    resultado = extrair_periodos(issues_invalidas)

    assert resultado == []
    assert mock_logger.warning.called
