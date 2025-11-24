from src.config import parameters
import logging

logger = logging.getLogger(__name__)

def extrair_jira_issues(projetos):
    atividades = []

    try:
        for projeto in projetos:
            projeto_nome = projeto['nome']
            JQL = f'project="{projeto_nome}"'
            data = parameters.JIRA_SESSION.enhanced_jql(jql=JQL, limit=1000)

            atividades += data['issues']

    except Exception as e:
        logger.error("Erro ao extrair JIRA Issues: %s", e)
        return []
    return atividades