import requests
from src.config import parameters

def carregar_status(status_array):
    jira_id_array = []
    
    for status in status_array:
        jira_id_atual = status["statusJiraId"]
        if not jira_id_atual in jira_id_array:
            inserir_um_status(status)
            jira_id_array.append(jira_id_atual)
        else:
            print(f"Status de ID interno {jira_id_atual} já existente")


def inserir_um_status(status):
    url = f"{parameters.BACK_BASE_URL}/dim-status"
    response = requests.post(url, json = status)

    if response.status_code in (200,201):
        resposta = response.json()
        status['id'] = resposta['id']
        print(f"Status {status['nome']} de ID {status['id']} inserido com sucesso")
    else:
        print(f"Erro ao chamar endpoint {url}: {response.status_code}, {response.content}")