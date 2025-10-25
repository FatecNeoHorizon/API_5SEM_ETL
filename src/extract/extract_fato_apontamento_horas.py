import logging
from src.utils.convert_datetime_to_periodo import convert_datetime_to_periodo
from src.utils import retorno_dimensoes

logger = logging.getLogger(__name__)

def extrair_todos_fatos_apontamento_horas(jira_issues, atividades, projetos, devs):

    global atividade
    global projeto
    global periodo
    global dev
    
    fato_apontamento_horas_dict = dict()
    # pk_sequence_array = []
    # data_atualização = dict()
    # data_criação = dict()
    # descricao_trabalho = dict()
    # horas_trabalhadas = dict()

    try:

        for jira_issue in jira_issues:

            extrair_dimensoes(jira_issue, atividades, projetos, devs)

            data_atualização = jira_issue["fields"]["updated"]
            data_criacao = jira_issue["fields"]["created"]
            descricao_trabalho = jira_issue["fields"]["description"]
            horas_trabalhadas = jira_issue["fields"]["timespent"]

            if not horas_trabalhadas:
                horas_trabalhadas = 0

            pk_sequence_current = f"{atividade['id']}-{projeto['id']}-{periodo['id']}-{dev['id']}"

            fato_apontamento_horas = dict(
            dimAtividade = atividade,
            dimProjeto = projeto,
            dimPeriodo = periodo,
            dimDev = dev,
            dataAtualizacao = data_atualização,
            dataCriacao = data_criacao,
            descricaoTrabalho = descricao_trabalho,
            horasTrabalhadas = horas_trabalhadas  )

            fato_apontamento_horas_dict[pk_sequence_current] = fato_apontamento_horas

        return fato_apontamento_horas_dict
        
    except Exception as e:
        logger.warning("Erro ao extrair fato_apontamento_horas: %s", e)
        return[]
    

def extrair_dimensoes(jira_issue, atividades, projetos, devs):

    #Extrair Atividade
    global atividade
    atividade_jira_id = jira_issue["id"]
    atividade = retorno_dimensoes.retornar_dim_atividade(atividades,atividade_jira_id)
    if not atividade:
        logger.warning("Erro ao extrair fato_apontamento_horas: Atividade não encontrada")
    
    #Extrair Projeto
    global projeto
    projeto_jira_id = jira_issue["fields"]["project"]["id"]
    projeto = retorno_dimensoes.retornar_dim_projeto(projetos, projeto_jira_id)
    if not projeto:
        logger.warning("Erro ao extrair fato_apontamento_horas: Projeto não encontrada")

    #Extrair Dev
    global dev
    # assignee = jira_issue["fields"]["assignee"]
    # if not assignee or not jira_issue.get("displayName"):
    #     return False

    # displayName = assignee['displayName']
   
    # dev = retorno_dimensoes.retornar_dim_dev(devs, displayName)
    dev = dict(
        id = 1,
        nome = "Eric Lourenço Mendes da SIlva"
    )
    if not dev:
        logger.warning("Erro ao extrair fato_apontamento_horas: Dev não encontrado")

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
        logger.warning("Erro ao extrair fato_apontamento_horas: Período não encontrado")

    