import requests
from requests import RequestException
import logging
from src.config import parameters

logger = logging.getLogger(__name__)

def gerar_token():
    try:
        payload = dict(
                    email = parameters.BACK_ETL_USUARIO,
                    password = parameters.BACK_ETL_SENHA,
                )
        url = f"{parameters.BACK_BASE_URL}/login"
        resp = requests.post(url, json=payload, timeout=parameters.REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        parameters.BACK_TOKEN = data['token']
        return data
    except RequestException as exc:
        detalhe = getattr(exc, 'response', None)
        if detalhe is not None:
            try:
                resp_text = detalhe.text
            except Exception:
                resp_text = str(detalhe)
            status = getattr(detalhe, 'status_code', 'n/a')
            logger.error("Erro ao chamar endpoint %s: %s, %s", url, status, resp_text)
        else:
            logger.error("Erro de rede ao chamar %s: %s", url, str(exc))
        return None