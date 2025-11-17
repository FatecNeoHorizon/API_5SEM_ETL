from src.utils.get_periodos_filter import get_periodos_filter
from src.config import parameters
from src.utils.http_client import post_json
import logging

logger = logging.getLogger(__name__)

def exclusao_dados():
    url = f"{parameters.BACK_BASE_URL}/deletar-dados"
    resposta = post_json(url, "", timeout=parameters.REQUEST_TIMEOUT, expect_id=False)
    if resposta != True:
        logger.warning("Erro ao excluir dados")
    else:
        logger.info("Exclusão realizada com sucesso")