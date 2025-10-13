import requests
from src.config import parameters

def carregar_periodos(periodos_array):
    for periodo in periodos_array:
        inserir_um_periodo(periodo)


def inserir_um_periodo(periodo):
    url = f"{parameters.BACK_BASE_URL}/dim-periodo"
    response = requests.post(url, json = periodo)

    if response.status_code in (200,201):
        resposta = response.json()
        periodo['id'] = resposta['id']
        print(f"Periodo de ID {periodo['id']} inserido com sucesso")
    else:
        print(f"Erro ao chamar endpoint {url}: {response.status_code}, {response.content}")