import logging
from src.utils.convert_datetime_to_periodo import convert_datetime_to_periodo
from src.utils.get_periodos_filter import get_periodos_filter

logger = logging.getLogger(__name__)

def extrair_todos_fatos_atividades(jira_issues, atividades, projetos, status_array, tipos):

    fato_atividade_array = []
    atividade = None
    projeto = None
    periodo = None
    status = None
    tipo = None

    flag = True

    try:

        for jira_issue in jira_issues:

            if flag:

                atividade_jira_id = jira_issue["id"]
                atividade = retornar_dim_atividade(atividades,atividade_jira_id)
                if not atividade:
                    logger.warning("Erro ao extrair fato_atividade: Atividade não encontrada")
                

                projeto_jira_id = jira_issue["fields"]["project"]["id"]
                projeto = retornar_dim_projeto(projetos, projeto_jira_id)
                if not projeto:
                    logger.warning("Erro ao extrair fato_atividade: Projeto não encontrada")

                worklogs = jira_issue["fields"]["worklog"]["worklogs"]
                filtro_periodo = None
                if len(worklogs) > 0:
                    started_datetime = worklogs[0]["started"]
                    filtro_periodo = convert_datetime_to_periodo(started_datetime)
                else:
                    filtro_periodo = dict(
                    dia = 31,
                    semana = 99,
                    mes = 12,
                    ano = 99 )

                periodo = retornar_dim_periodo(filtro_periodo)
                if not periodo:
                    logger.warning("Erro ao extrair fato_atividade: Período não encontrado")

                statusJiraId = jira_issue["fields"]["statusCategory"]["id"]
                status = retornar_dim_status(status_array, statusJiraId)
                if not status:
                    logger.warning("Erro ao extrair fato_atividade: Status não encontrado")

                tipoJiraId = jira_issue["fields"]["issuetype"]["id"]
                tipo = retornar_dim_tipo(tipos, tipoJiraId)
                if not tipo:
                    logger.warning("Erro ao extrair fato_atividade: Tipo não encontrado")
                
                flag = False



                fato_atividade = dict(
                dimAtividade = atividade,
                dimProjeto = projeto,
                dimPeriodo = periodo,
                dimStatus = status,
                dimTipo = tipo,
                quantidade = 1.00  )

                fato_atividade_array.append(fato_atividade)

        return fato_atividade_array
        
    except Exception as e:
        logger.warning("Erro ao fato_atividade: %s", e)
        return[]
    

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