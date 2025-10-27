from src.utils.get_periodos_filter import get_periodos_filter
from src.config import parameters
from src.utils.http_client import post_json
import logging

logger = logging.getLogger(__name__)

def inserir_periodo_coringa():
    filtro_periodo = dict(
                    dia = 31,
                    semana = 99,
                    mes = 12,
                    ano = 99 )
    
    banco_periodos = get_periodos_filter(filtro_periodo['dia'], filtro_periodo['semana'], filtro_periodo['mes'], filtro_periodo['ano'])
    
    if len(banco_periodos) > 0:
        return
    
    url = f"{parameters.BACK_BASE_URL}/dim-periodo"
    resposta = post_json(url, filtro_periodo, timeout=parameters.REQUEST_TIMEOUT, expect_id=True)

    if not resposta:
        return
    
    logger.info(
        "Periodo dia %s mês %s semana %s de ID %s inserido com sucesso",
        filtro_periodo.get('dia'),
        filtro_periodo.get('mes'),
        filtro_periodo.get('semana'),
        filtro_periodo.get('id'),
    )
