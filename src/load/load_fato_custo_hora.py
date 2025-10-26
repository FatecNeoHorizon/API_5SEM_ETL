import logging
from src.config import parameters
from src.utils.http_client import post_json

logger = logging.getLogger(__name__)

def carregar_fato_custo_hora(fato_custo_hora_dict):
    try:
        for key in fato_custo_hora_dict:
            inserir_um_fato_custo_hora(fato_custo_hora_dict[key])
    except Exception as e:
        logger.warning("Erro ao carregar fato_custo_hora: %s", e)
        return []


def inserir_um_fato_custo_hora(fato_custo_hora, timeout: int = parameters.REQUEST_TIMEOUT):
    url = f"{parameters.BACK_BASE_URL}/fato-custo-hora"
    resposta = post_json(url, fato_custo_hora, timeout=timeout, expect_id=True)
    if not resposta:
        return

    resp_id = resposta.get('id')
    if not resp_id:
        logger.error("Resposta do backend para criar fato_custo_hora não contém 'id'. Resposta: %s", resposta)
        return

    fato_custo_hora['id'] = resp_id
    logger.info("Fato Custo Hora de ID %s inserido com sucesso", fato_custo_hora.get('id'))
