import logging
import requests
from requests import RequestException
from src.config import parameters

logger = logging.getLogger(__name__)


def post_json(url: str, payload: dict, timeout: int = 30, expect_id: bool = False):
    try:
        headers = {
            "Authorization": f"Bearer {parameters.BACK_TOKEN}",
        }
        resp = requests.post(url, json=payload, timeout=timeout, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if expect_id and data.get('id') is None:
            logger.error("Resposta do endpoint %s não contém 'id'. Resposta: %s", url, data)
            return None
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
