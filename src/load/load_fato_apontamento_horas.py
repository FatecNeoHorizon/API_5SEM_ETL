from src.config import parameters
import logging
from src.utils.http_client import post_json

logger = logging.getLogger(__name__)

def carregar_fato_apontamento_horas(fato_apontamento_horas_dict):

    try:
        for key in fato_apontamento_horas_dict: 
            inserir_um_fato_apontamento_horas(fato_apontamento_horas_dict[key])

    except Exception as e:
        logger.warning("Erro ao carregar fato_atividades: %s", e)
        return[]


def inserir_um_fato_apontamento_horas(fato_apontamento_hora, timeout: int = parameters.REQUEST_TIMEOUT):
    url = f"{parameters.BACK_BASE_URL}/fato-apontamento-horas"

    resposta = post_json(url, fato_apontamento_hora, timeout=timeout, expect_id=True)
    if not resposta:
        return

    resp_id = resposta.get('id')
    if not resp_id:
        logger.error("Resposta do backend para criar fato_atividade não contém 'id'. Resposta: %s", resposta)
        return

    fato_apontamento_hora['id'] = resp_id
    logger.info(
        "Fato Atividade de ID %s inserido com sucesso",
        fato_apontamento_hora.get('id'),
    )