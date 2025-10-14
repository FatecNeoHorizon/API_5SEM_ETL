import requests
from src.config import parameters
from src.utils import get_periodos_filter

def carregar_periodos(periodos_array):
    for periodo in periodos_array:
        if not verificar_periodo_existente(periodo):
            inserir_um_periodo(periodo)
        else:
            print(f"Período dia {periodo['dia']} mês {periodo['mes']} semana {periodo['semana']} já existente")


def inserir_um_periodo(periodo):
    url = f"{parameters.BACK_BASE_URL}/dim-periodo"
    response = requests.post(url, json = periodo)

    if response.status_code in (200,201):
        resposta = response.json()
        periodo['id'] = resposta['id']
        print(f"Periodo dia {periodo['dia']} mês {periodo['mes']} semana {periodo['semana']} de ID {periodo['id']} inserido com sucesso")
    else:
        print(f"Erro ao chamar endpoint {url}: {response.status_code}, {response.content}")


def verificar_periodo_existente(periodo):

    periodos_banco = get_periodos_filter.get_periodos_filter(periodo['dia'], periodo['semana'], periodo['mes'], periodo['ano'])
    return len(periodos_banco) > 0