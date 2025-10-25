from datetime import datetime
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

            flag = extrair_dimensoes(jira_issue, atividades, projetos, devs)

            if not flag:
                continue

            jira_data_atualizacao = jira_issue["fields"]["updated"]
            jira_data_criacao = jira_issue["fields"]["created"]

            descricao_trabalho = jira_issue["fields"]["description"]
            horas_trabalhadas = jira_issue["fields"]["timespent"]
            data_atualizacao = converter_jira_datetime_para_back(jira_data_atualizacao)
            data_criacao = converter_jira_datetime_para_back(jira_data_criacao)

            if not horas_trabalhadas:
                horas_trabalhadas = 1

            if not descricao_trabalho:
                descricao_trabalho = 'Descrição não fornecida'

            pk_sequence_current = f"{atividade['id']}-{projeto['id']}-{periodo['id']}-{dev['id']}"

            fato_apontamento_horas = dict(
            dimAtividade = atividade,
            dimProjeto = projeto,
            dimPeriodo = periodo,
            dimDev = dev,
            dataAtualizacao = data_atualizacao,
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
    assignee = jira_issue["fields"]["assignee"]

    if not assignee:
        return False

    displayName = assignee['displayName']
    dev = retorno_dimensoes.retornar_dim_dev(devs, displayName)
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

    return True

def converter_jira_datetime_para_back(jira_horas_trabalhadas):
    aux_horas_trabalhadas = jira_horas_trabalhadas.split('.')[0]
    aux_datetime = datetime.strptime(aux_horas_trabalhadas, '%Y-%m-%dT%H:%M:%S')
    back_horas_trabalhadas = aux_datetime.strftime("%d-%m-%Y %H:%M:%S")
    return back_horas_trabalhadas