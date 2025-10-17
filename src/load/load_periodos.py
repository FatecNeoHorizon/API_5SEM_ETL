import logging
from src.config import parameters
from src.utils import get_periodos_filter
from src.utils.http_client import post_json

logger = logging.getLogger(__name__)


def carregar_periodos(periodos_array):
    for periodo in periodos_array:
        if not verificar_periodo_existente(periodo):
            inserir_um_periodo(periodo)
        else:
            logger.info(
                "Período dia %s mês %s semana %s já existente",
                periodo.get('dia'),
                periodo.get('mes'),
                periodo.get('semana'),
            )


def inserir_um_periodo(periodo, timeout: int = parameters.REQUEST_TIMEOUT):
    url = f"{parameters.BACK_BASE_URL}/dim-periodo"
    resposta = post_json(url, periodo, timeout=timeout, expect_id=True)
    if not resposta:
        return

    resp_id = resposta.get('id')
    if not resp_id:
        logger.error("Resposta do backend para criar periodo não contém 'id'. Resposta: %s", resposta)
        return

    periodo['id'] = resp_id
    logger.info(
        "Periodo dia %s mês %s semana %s de ID %s inserido com sucesso",
        periodo.get('dia'),
        periodo.get('mes'),
        periodo.get('semana'),
        periodo.get('id'),
    )


def verificar_periodo_existente(periodo):

    periodos_banco = get_periodos_filter.get_periodos_filter(periodo['dia'], periodo['semana'], periodo['mes'], periodo['ano'])
    return len(periodos_banco) > 0