import pytest
from unittest.mock import patch
from src.extract import extract_projetos, extract_jira_issues, extract_status
from src.load import load_status

@pytest.fixture
def mock_projetos():
    return [
        {"nome": "Projeto A", "projeto_jira_id": "1001"},
        {"nome": "Projeto B", "projeto_jira_id": "1002"}
    ]

@pytest.fixture
def mock_issues():
    return [
        {
            "key": "ISSUE-1",
            "id": "2001",
            "fields": {
                "statusCategory": {"id": 1, "name": "To Do", "colorName": "blue"}
            }
        },
        {
            "key": "ISSUE-2",
            "id": "2002",
            "fields": {
                "statusCategory": {"id": 2, "name": "In Progress", "colorName": "yellow"}
            }
        }
    ]

@pytest.fixture
def mock_status_array():
    return [
        {"nome": "To Do", "statusJiraId": 1, "colorName": "blue"},
        {"nome": "In Progress", "statusJiraId": 2, "colorName": "yellow"}
    ]

@patch("src.extract.extract_projetos.extrair_todos_projetos")
@patch("src.extract.extract_jira_issues.extrair_jira_issues")
@patch("src.extract.extract_status.extrair_todos_status")
@patch("src.load.load_status.carregar_status")
def test_etl_status_flow(
    mock_carregar_status,
    mock_extrair_todos_status,
    mock_extrair_jira_issues,
    mock_extrair_todos_projetos,
    mock_projetos,
    mock_issues,
    mock_status_array
):
    mock_extrair_todos_projetos.return_value = mock_projetos
    mock_extrair_jira_issues.return_value = mock_issues
    mock_extrair_todos_status.return_value = mock_status_array

    projetos = extract_projetos.extrair_todos_projetos()
    assert projetos == mock_projetos

    issues = extract_jira_issues.extrair_jira_issues(projetos)
    assert issues == mock_issues

    status_array = extract_status.extrair_todos_status(issues)
    assert status_array == mock_status_array

    status_unicos = {s["statusJiraId"]: s for s in status_array}
    assert len(status_unicos) == 2
    assert status_unicos[1]["nome"] == "To Do"
    assert status_unicos[2]["nome"] == "In Progress"

    load_status.carregar_status(status_array)
    mock_carregar_status.assert_called_once_with(mock_status_array)

    for status in status_array:
        assert isinstance(status["nome"], str)
        assert isinstance(status["statusJiraId"], int)
        assert status["colorName"] in ["blue", "yellow"]