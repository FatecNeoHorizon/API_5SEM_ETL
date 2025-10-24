import logging
from src.utils.convert_datetime_to_periodo import convert_datetime_to_periodo
from src.utils import retorno_dimensoes

logger = logging.getLogger(__name__)

def extrair_todos_fatos_atividades(jira_issues, projetos, status_array, tipos):

    global projeto
    global periodo
    global status
    global tipo
    
    fato_atividade_dict = dict()
    pk_sequence_array = []
    qtd_final = dict()

    try:

        for jira_issue in jira_issues:

            extrair_dimensoes(jira_issue, projetos, status_array, tipos)

            pk_sequence_current = f"{projeto['id']}-{periodo['id']}-{status['id']}-{tipo['id']}"

            if pk_sequence_current in pk_sequence_array:
                qtd_final[pk_sequence_current] += 1
            else:
                qtd_final[pk_sequence_current] = 1
                pk_sequence_array.append(pk_sequence_current)

            fato_atividade = dict(
            dimProjeto = projeto,
            dimPeriodo = periodo,
            dimStatus = status,
            dimTipo = tipo,
            quantidade = qtd_final[pk_sequence_current]  )

            fato_atividade_dict[pk_sequence_current] = fato_atividade

        return fato_atividade_dict
        
    except Exception as e:
        logger.warning("Erro ao fato_atividade: %s", e)
        return[]
    

def extrair_dimensoes(jira_issue, projetos, status_array, tipos):
    
    #Extrair Projeto
    global projeto
    projeto_jira_id = jira_issue["fields"]["project"]["id"]
    projeto = retorno_dimensoes.retornar_dim_projeto(projetos, projeto_jira_id)
    if not projeto:
        logger.warning("Erro ao extrair fato_atividade: Projeto não encontrada")

    #Extrair Período
    global periodo
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

    periodo = retorno_dimensoes.retornar_dim_periodo(filtro_periodo)
    if not periodo:
        logger.warning("Erro ao extrair fato_atividade: Período não encontrado")

    #Extrair Status
    global status
    statusJiraId = jira_issue["fields"]["statusCategory"]["id"]
    status = retorno_dimensoes.retornar_dim_status(status_array, statusJiraId)
    if not status:
        logger.warning("Erro ao extrair fato_atividade: Status não encontrado")

    #Extrair Tipo
    global tipo
    tipoJiraId = jira_issue["fields"]["issuetype"]["id"]
    tipo = retorno_dimensoes.retornar_dim_tipo(tipos, tipoJiraId)
    if not tipo:
        logger.warning("Erro ao extrair fato_atividade: Tipo não encontrado")