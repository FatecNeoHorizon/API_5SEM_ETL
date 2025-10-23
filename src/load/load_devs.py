import requests
from src.config import parameters
import logging
from src.utils.http_client import post_json

logger = logging.getLogger(__name__)

def carregar_devs(devs_array):
    dev_nome_array = []
    for dev in devs_array:
        dev_nome_atual = dev["nome"]
        if dev_nome_atual not in dev_nome_array:
            inserir_dev(dev)  # dev pode ter só "nome"
            dev_nome_array.append(dev_nome_atual)
        else:
            logger.info("Desenvolvedor - %s já cadastrado", dev.get('nome'))

def inserir_dev(dev, timeout: int = parameters.REQUEST_TIMEOUT):
    url = f"{parameters.BACK_BASE_URL}/dim-dev"

    # Cria o campo aqui no ETL: se não vier, envia 0
    payload = {
        "nome": dev.get("nome"),
        "custoHora": dev.get("custoHora", 10)  # default no ETL
    }

    if not payload["nome"]:
        logger.error("Nome do desenvolvedor ausente no payload: %s", dev)
        return

    resposta = post_json(url, payload, timeout=timeout, expect_id=True)
    if not resposta:
        return

    resp_id = resposta.get('id')
    if not resp_id:
        logger.error("Resposta do backend para criar dev não contém 'id'. Resposta: %s", resposta)
        return

    # opcional: refletir no objeto original
    dev['id'] = resp_id
    dev.setdefault('custoHora', payload['custoHora'])

    logger.info("Dev de nome %s - ID %s inserido com sucesso", dev.get('nome'), dev.get('id'))
