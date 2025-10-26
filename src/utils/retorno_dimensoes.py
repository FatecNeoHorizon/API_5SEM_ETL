from src.utils.convert_datetime_to_periodo import convert_datetime_to_periodo
from src.utils.get_periodos_filter import get_periodos_filter

def retornar_dim_atividade(atividades,atividade_jira_id):
    for atividade in atividades:
        if atividade['atividade_jira_id'] == atividade_jira_id:
            return atividade
    return None

def retornar_dim_projeto(projetos,projeto_jira_id):
    for projeto in projetos:
        if projeto['projeto_jira_id'] == projeto_jira_id:
            return projeto
    return None

def retornar_dim_periodo(filtro_periodo):
    banco_periodos = get_periodos_filter(filtro_periodo['dia'], filtro_periodo['semana'], filtro_periodo['mes'], filtro_periodo['ano'])
    if len(banco_periodos) > 0:
        return banco_periodos[0]
    
    return None

def retornar_dim_status(status_array, statusJiraId):
    for status in status_array:
        if status['statusJiraId'] == statusJiraId:
            return status
    return None

def retornar_dim_tipo(tipos, tipoJiraId):
    for tipo in tipos:
        if tipo['tipoJiraId'] == tipoJiraId:
            return tipo
    return None

def retornar_dim_dev(devs, devJiraNome):
    alvo = devJiraNome.strip().lower()
    vistos, id_calc = set(), 1  
    for dev in devs or []:
        nome = (dev.get("nome") or "").strip()
        if not nome:
            continue
        k = nome.lower()
        if k in vistos:
            continue
        vistos.add(k)
        id_calc += 1  
        if k == alvo:
            return id_calc
    return 1