import requests
from src.config import parameters

def retorno_devs():
    url = f"{parameters.BACK_BASE_URL}/dim-dev"
    response = requests.get(url=url)

    if response.status_code in (200,201):
        resposta = response.json()
        return resposta
    else:
        print(f"Erro ao chamar endpoint {url}: {response.status_code}, {response.content}")
        return ""