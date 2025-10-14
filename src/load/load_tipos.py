import requests
from src.config import parameters

def carregar_tipos(tipos_array):
    jira_id_array = []
    
    for tipo in tipos_array:
        jira_id_atual = tipo["tipoJiraId"]
        if not jira_id_atual in jira_id_array:
            inserir_um_tipo(tipo)
            jira_id_array.append(jira_id_atual)
        else:
            print(f"Tipo de ID interno {jira_id_atual} já existente")


def inserir_um_tipo(tipo):
    url = f"{parameters.BACK_BASE_URL}/dim-tipo"
    response = requests.post(url, json = tipo)

    if response.status_code in (200,201):
        resposta = response.json()
        tipo['id'] = resposta['id']
        print(f"Tipo {tipo['nome']} de ID {tipo['id']} inserido com sucesso")
    else:
        print(f"Erro ao chamar endpoint {url}: {response.status_code}, {response.content}")