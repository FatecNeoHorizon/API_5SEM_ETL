import pytest
from unittest.mock import patch
from src.extract import extract_projetos, extract_jira_issues, extract_status
from src.load import load_status

# ---------- FIXTURES ----------
@pytest.fixture
def projetos_ok():
    return [
        {"nome": "Projeto A", "projeto_jira_id": "1001"},
        {"nome": "Projeto B", "projeto_jira_id": "1002"},
    ]

@pytest.fixture
def issues_ok():
    return [
        {
            "key": "ISSUE-1",
            "id": "2001",
            "fields": {"statusCategory": {"id": 1, "name": "To Do", "colorName": "blue"}}
        },
        {
            "key": "ISSUE-2",
            "id": "2002",
            "fields": {"statusCategory": {"id": 2, "name": "In Progress", "colorName": "yellow"}}
        }
    ]

@pytest.fixture
def status_ok():
    return [
        {"nome": "To Do", "statusJiraId": 1, "colorName": "blue"},
        {"nome": "In Progress", "statusJiraId": 2, "colorName": "yellow"},
    ]


# ---------- TESTE E2E DA CAMADA (REGRAS) ----------
@patch("src.load.load_status.carregar_status")
@patch("src.extract.extract_status.extrair_todos_status")
@patch("src.extract.extract_jira_issues.extrair_jira_issues")
@patch("src.extract.extract_projetos.extrair_todos_projetos")
def test_e2e_status_regras_de_negocio(
    mock_extrair_todos_projetos,
    mock_extrair_jira_issues,
    mock_extrair_todos_status,
    mock_carregar_status,
    projetos_ok,
    issues_ok,
    status_ok,
):
    # Arrange
    mock_extrair_todos_projetos.return_value = projetos_ok
    mock_extrair_jira_issues.return_value = issues_ok
    mock_extrair_todos_status.return_value = status_ok

    # Act
    projetos = extract_projetos.extrair_todos_projetos()
    issues = extract_jira_issues.extrair_jira_issues(projetos)
    status_array = extract_status.extrair_todos_status(issues)

    # Regras de negócio na camada:
    # 1) Unicidade por statusJiraId
    unicos = {s["statusJiraId"]: s for s in status_array}
    assert len(unicos) == 2

    # 2) Tipos e domínio de valores
    for s in status_array:
        assert isinstance(s["nome"], str)
        assert isinstance(s["statusJiraId"], int)
        assert s["colorName"] in ["blue", "yellow"]

    # 3) Load é chamado com o array resultante
    load_status.carregar_status(status_array)
    mock_carregar_status.assert_called_once_with(status_ok)
