from src.config import parameters
import logging

logger = logging.getLogger(__name__)


def extrair_todos_tipos(jira_issues):
    back_tipos = []

    try:

        for jira_issue in jira_issues:
            issue_type = jira_issue["fields"]["issuetype"]

            back_tipo = dict(
            nome = issue_type['name'],
            descricao = issue_type['description'],
            tipoJiraId = issue_type['id']  )

            back_tipos.append(back_tipo)

        return back_tipos
        
    except Exception as e:
        logger.warning("Erro ao extrair períodos: %s", e)
        return[]