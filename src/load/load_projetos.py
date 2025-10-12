import requests
from src.config import parameters


def carregar_projetos(projetos_array):
    
    for projeto in projetos_array:
        inserir_um_projeto(projeto)


def inserir_um_projeto(projeto):
    url = f"{parameters.BACK_BASE_URL}/dim-projeto"
    response = requests.post(url, json = projeto)

    if response.status_code in (200,201):
        resposta = response.json()
        projeto['id'] = resposta['id']
        print(f"Projeto {projeto['nome']} de ID {projeto['id']} inserido com sucesso")
    else:
        print(f"Erro ao chamar endpoint {url}: {response.status_code}, {response.content}")