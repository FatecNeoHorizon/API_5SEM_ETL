from src.config import parameters
import logging
from src.utils.http_client import post_json

logger = logging.getLogger(__name__)

def carregar_fato_atividades(fato_atividade_array):

    try:
        for fato_atividade in fato_atividade_array:
                inserir_um_fato_atividade(fato_atividade)

    except Exception as e:
        logger.warning("Erro ao carregar fato_atividades: %s", e)
        return[]


def inserir_um_fato_atividade(fato_atividade, timeout: int = parameters.REQUEST_TIMEOUT):
    url = f"{parameters.BACK_BASE_URL}/fato-atividade"

    resposta = post_json(url, fato_atividade, timeout=timeout, expect_id=True)
    if not resposta:
        return

    resp_id = resposta.get('id')
    if not resp_id:
        logger.error("Resposta do backend para criar fato_atividade não contém 'id'. Resposta: %s", resposta)
        return

    fato_atividade['id'] = resp_id
    logger.info(
        "Fato Atividade de ID %s inserido com sucesso",
        fato_atividade.get('id'),
    )