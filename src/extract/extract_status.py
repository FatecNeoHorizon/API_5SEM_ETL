from src.config import parameters
import logging

logger = logging.getLogger(__name__)

def extrair_todos_status(jira_issues):
    back_status_array = []

    try:

        for jira_issue in jira_issues:
            status_category = jira_issue["fields"]["statusCategory"]

            back_status = dict(
            nome = status_category['name'],
            statusJiraId = status_category['id']  )

            back_status_array.append(back_status)

        return back_status_array
        
    except Exception as e:
        logger.warning("Erro ao extrair status: %s", e)
        return[]