from src.config import parameters
import logging

logger = logging.getLogger(__name__)

def extrair_todos_fatos_atividades(jira_issues, atividades, projetos):

    fato_atividade_array = []
    atividade = None
    projeto = None
    flag = True

    try:

        for jira_issue in jira_issues:
            status_category = jira_issue["fields"]["statusCategory"]

            if flag:

                atividade_jira_id = jira_issue["id"]
                atividade = retornar_dim_atividade(atividades,atividade_jira_id)
                if not atividade:
                    logger.warning("Erro ao extrair fato_atividade: Atividade não encontrada")
                

                projeto_jira_id = jira_issue["fields"]["project"]["id"]
                projeto = retornar_dim_projeto(projetos, projeto_jira_id)
                if not projeto:
                    logger.warning("Erro ao extrair fato_atividade: Projeto não encontrada")

                flag = False



            fato_atividade = dict(
            atividade = atividade,
            projeto = projeto,
            periodo_id = 1,
            status_id = 1,
            tipo_id = 1,
            atividade_quantidade_numeric = 1,
            nome = status_category['name'],
            statusJiraId = status_category['id']  )

            fato_atividade_array.append(fato_atividade)

        return fato_atividade_array
        
    except Exception as e:
        logger.warning("Erro ao extrair status: %s", e)
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