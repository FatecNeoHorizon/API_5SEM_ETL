import requests
from src.config import parameters

def carregar_atividades(atividades):
    for atividade in atividades:
        inserir_uma_atividade(atividade)

    
def inserir_uma_atividade(atividade):
    url = f"{parameters.BACK_BASE_URL}/dim-atividade"
    response = requests.post(url, json = atividade)

    if response.status_code in (200,201):
        resposta = response.json()
        atividade['id'] = resposta['id']
        print(f"Atividade {atividade['nome']} de Id do Jira: {atividade['atividade_jira_id']} inserida com sucesso")
    else:
        print(f"Erro ao chamar endpoint {url}: {response.status_code}, {response.content}")
