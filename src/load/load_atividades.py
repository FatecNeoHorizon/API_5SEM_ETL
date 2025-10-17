import logging
from src.config import parameters
from src.utils.http_client import post_json

logger = logging.getLogger(__name__)


def carregar_atividades(atividades):
    for atividade in atividades:
        inserir_atividade(atividade)


def inserir_atividade(atividade, timeout: int = parameters.REQUEST_TIMEOUT):
    url = f"{parameters.BACK_BASE_URL}/dim-atividade"
    resposta = post_json(url, atividade, timeout=timeout, expect_id=True)
    if not resposta:
        return

    resp_id = resposta.get('id')
    if not resp_id:
        logger.error("Resposta do backend para criar atividade não contém 'id'. Resposta: %s", resposta)
        return

    atividade['id'] = resp_id
    logger.info(
        "Atividade %s de Id do Jira: %s inserida com sucesso",
        atividade.get('nome'),
        atividade.get('atividade_jira_id'),
    )
