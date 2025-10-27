import requests
from src.config import parameters
import logging
from src.utils.http_client import post_json

logger = logging.getLogger(__name__)

def carregar_tipos(tipos_array):
    jira_id_array = []
    
    for tipo in tipos_array:
        jira_id_atual = tipo["tipoJiraId"]
        if not jira_id_atual in jira_id_array:
            inserir_um_tipo(tipo)
            jira_id_array.append(jira_id_atual)
        else:
            logger.info(
                "Tipo nome %s, descrição %s, e tipoJiraId %s já existente",
                tipo.get('nome'),
                tipo.get('descricao'),
                tipo.get('tipoJiraId'),
            )


def inserir_um_tipo(tipo, timeout: int = parameters.REQUEST_TIMEOUT):
    url = f"{parameters.BACK_BASE_URL}/dim-tipo"
    # response = requests.post(url, json = tipo)

    resposta = post_json(url, tipo, timeout=timeout, expect_id=True)
    if not resposta:
        return

    resp_id = resposta.get('id')
    if not resp_id:
        logger.error("Resposta do backend para criar tipo não contém 'id'. Resposta: %s", resposta)
        return

    tipo['id'] = resp_id
    logger.info(
        "Tipo de nome %s, descrição %s, e tipoJiraId %s de ID %s inserido com sucesso",
        tipo.get('nome'),
        tipo.get('descricao'),
        tipo.get('tipoJiraId'),
        tipo.get('id'),
    )