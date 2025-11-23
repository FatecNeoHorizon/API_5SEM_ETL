import requests
from src.config import parameters

def get_periodos_filter(dia,semana,mes,ano):
    url = f"{parameters.BACK_BASE_URL}/dim-periodo/filter"
    params = {
        "dia": dia,
        "semana": semana,
        "mes": mes,
        "ano": ano
    }

    headers = {
            "Authorization": f"Bearer {parameters.BACK_TOKEN}",
        }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code in (200,201):
        resposta = response.json()
        return resposta
    else:
        print(f"Erro ao chamar endpoint {url}: {response.status_code}, {response.content}")
        return ""
