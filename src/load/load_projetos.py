import logging
from src.config import parameters
from src.utils.http_client import post_json

logger = logging.getLogger(__name__)


def carregar_projetos(projetos_array):
    for projeto in projetos_array:
        inserir_um_projeto(projeto)


def inserir_um_projeto(projeto, timeout: int = parameters.REQUEST_TIMEOUT):
    url = f"{parameters.BACK_BASE_URL}/dim-projeto"
    resposta = post_json(url, projeto, timeout=timeout, expect_id=True)
    if not resposta:
        return

    resp_id = resposta.get('id')
    if not resp_id:
        logger.error("Resposta do backend para criar projeto não contém 'id'. Resposta: %s", resposta)
        return

    projeto['id'] = resp_id
    logger.info(
        "Projeto %s de ID %s inserido com sucesso",
        projeto.get('nome'),
        projeto.get('id'),
    )