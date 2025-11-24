import requests
from src.config import parameters
import logging
from src.utils.http_client import post_json
from src.utils.retorno_todos_devs_banco import retorno_devs

logger = logging.getLogger(__name__)

def carregar_devs(devs_array):
    dev_nome_array = []

    banco_devs = retorno_devs()
    inserir_dev_banco_em_array(banco_devs, devs_array, dev_nome_array)
    
    sem_atribuicao = "Não atribuido"
    if sem_atribuicao not in dev_nome_array:
        inserir_dev({"nome": sem_atribuicao, "custoHora": 1})
        dev_nome_array.append(sem_atribuicao)

    for dev in devs_array:
        dev_nome_atual = dev["nome"]
        if dev_nome_atual not in dev_nome_array:
            inserir_dev(dev) 
            dev_nome_array.append(dev_nome_atual)
        else:
            logger.info("Desenvolvedor - %s já cadastrado", dev.get('nome'))

def inserir_dev(dev, timeout: int = parameters.REQUEST_TIMEOUT):
    url = f"{parameters.BACK_BASE_URL}/dim-dev"

    payload = {
        "nome": dev.get("nome"),
        "custoHora": dev.get("custoHora", 10) 
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

    dev['id'] = resp_id
    dev.setdefault('custoHora', payload['custoHora'])

    logger.info("Dev de nome %s - ID %s inserido com sucesso", dev.get('nome'), dev.get('id'))

def inserir_dev_banco_em_array(banco_devs, devs_array, dev_nome_array):
    for banco_dev in banco_devs:
        dev_nome_array.append(banco_dev["nome"])

        for dev_array in devs_array:
            if dev_array["nome"] == banco_dev["nome"]:
                dev_array["id"] = banco_dev["id"]