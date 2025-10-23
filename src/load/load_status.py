import logging
from src.config import parameters
from src.utils.http_client import post_json

logger = logging.getLogger(__name__)

def carregar_status(status_array):
    jira_id_array = []
    
    for status in status_array:
        jira_id_atual = status["statusJiraId"]
        if not jira_id_atual in jira_id_array:
            inserir_um_status(status)
            jira_id_array.append(jira_id_atual)
        else:
            logger.info(
                "Status de nome %s e statusJiraId %s já existente",
                status.get('nome'),
                status.get('statusJiraId')
            )

def inserir_um_status(status,timeout: int = parameters.REQUEST_TIMEOUT):
    url = f"{parameters.BACK_BASE_URL}/dim-status"
    resposta = post_json(url, status, timeout=timeout, expect_id=True)
    if not resposta:
        return

    resp_id = resposta.get('id')
    if not resp_id:
        logger.error("Resposta do backend para criar status não contém 'id'. Resposta: %s", resposta)
        return

    status['id'] = resp_id
    logger.info(
        "Status de nome %s e statusJiraId %s de ID %s inserido com sucesso",
        status.get('nome'),
        status.get('statusJiraId'),
        status.get('id')
    )