import pytest
from src.extract import extract_status

# ---------- FIXTURES ----------
@pytest.fixture
def issues_ok():
    return [
        {
            "key": "ISSUE-1",
            "id": "2001",
            "fields": {
                "statusCategory": {"id": 1, "name": "To Do"}
            },
        },
        {
            "key": "ISSUE-2",
            "id": "2002",
            "fields": {
                "statusCategory": {"id": 2, "name": "In Progress"}
            },
        },
    ]


@pytest.fixture
def issues_duplicadas():
    # Mesmo status em issues diferentes (id = 1 repetido)
    return [
        {
            "key": "ISSUE-1",
            "id": "2001",
            "fields": {
                "statusCategory": {"id": 1, "name": "To Do"}
            },
        },
        {
            "key": "ISSUE-2",
            "id": "2002",
            "fields": {
                "statusCategory": {"id": 1, "name": "To Do"}
            },
        },
        {
            "key": "ISSUE-3",
            "id": "2003",
            "fields": {
                "statusCategory": {"id": 2, "name": "In Progress"}
            },
        },
    ]


@pytest.fixture
def issues_faltando_campos():
    # Primeira issue sem campo obrigatório em statusCategory
    return [
        {
            "key": "ISSUE-1",
            "id": "2001",
            "fields": {
                "statusCategory": {"id": 1}  # falta "name"
            },
        },
        {
            "key": "ISSUE-2",
            "id": "2002",
            "fields": {
                "statusCategory": {"id": 2, "name": "In Progress"}
            },
        },
    ]


@pytest.fixture
def issues_tipos_invalidos():
    # Tipos "errados", mas a função atual não valida tipo
    return [
        {
            "key": "ISSUE-1",
            "id": "2001",
            "fields": {
                "statusCategory": {"id": "um", "name": 123}
            },
        }
    ]


@pytest.fixture
def issues_vazio():
    return []


# ---------- TESTES (ALINHADOS À IMPLEMENTAÇÃO ATUAL) ----------

def test_extract_status_mapeamento_basico(issues_ok):
    """
    A função deve mapear corretamente 'name' -> 'nome' e 'id' -> 'statusJiraId',
    retornando uma lista de dicionários com essas duas chaves.
    """
    status_array = extract_status.extrair_todos_status(issues_ok)

    assert isinstance(status_array, list)
    assert len(status_array) == 2

    s1, s2 = sorted(status_array, key=lambda s: s["statusJiraId"])
    assert s1 == {"nome": "To Do", "statusJiraId": 1}
    assert s2 == {"nome": "In Progress", "statusJiraId": 2}


def test_extract_status_deduplicacao_por_id(issues_duplicadas):
    """
    A função NÃO faz deduplicação internamente, mas o resultado pode ser deduplicado
    externamente usando o 'statusJiraId'. Este teste garante que o formato de saída
    permite isso (3 entradas de saída -> 2 únicas por ID).
    """
    status_array = extract_status.extrair_todos_status(issues_duplicadas)

    assert len(status_array) == 3  # função apenas mapeia linha a linha

    # Deduplicação feita no teste, fora da função
    unicos = {s["statusJiraId"]: s for s in status_array}
    assert len(unicos) == 2
    assert set(s["nome"] for s in unicos.values()) == {"To Do", "In Progress"}


@pytest.mark.parametrize("campo_removido", ["id", "name"])
def test_extract_status_campos_obrigatorios_retorna_lista_vazia(issues_ok, campo_removido):
    """
    Se faltar 'id' OU 'name' em algum statusCategory, a função atual captura a exceção,
    registra o log e retorna uma lista vazia.
    """
    issues = [dict(i) for i in issues_ok]
    # Clona o dicionário interno de statusCategory da primeira issue
    status_cat = dict(issues[0]["fields"]["statusCategory"])
    del status_cat[campo_removido]
    issues[0]["fields"]["statusCategory"] = status_cat

    status_array = extract_status.extrair_todos_status(issues)

    # Como a função trata a exceção e retorna [], não deve levantar erro
    assert status_array == []


def test_extract_status_tipos_invalidos_sem_excecao(issues_tipos_invalidos):
    """
    A função atual não valida tipos (somente lê os campos e os replica).
    Este teste garante que, mesmo com tipos "inesperados", ela não levante exceção
    e apenas mapeie o que foi recebido.
    """
    status_array = extract_status.extrair_todos_status(issues_tipos_invalidos)

    assert isinstance(status_array, list)
    assert len(status_array) == 1

    s = status_array[0]
    # A função simplesmente copia 'name' e 'id' para 'nome' e 'statusJiraId'
    assert s["nome"] == 123
    assert s["statusJiraId"] == "um"


def test_extract_status_lista_vazia(issues_vazio):
    """
    Se nenhuma issue é recebida, a função deve retornar lista vazia.
    """
    status_array = extract_status.extrair_todos_status(issues_vazio)
    assert status_array == []
