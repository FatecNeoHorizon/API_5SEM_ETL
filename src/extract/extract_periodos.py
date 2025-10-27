import logging
from src.utils.convert_datetime_to_periodo import convert_datetime_to_periodo

logger = logging.getLogger(__name__)

def extrair_periodos(jira_issues):
    periodos = []

    try:
        for jira_issue in jira_issues:
            worklogs = jira_issue["fields"]["worklog"]["worklogs"]

            if len(worklogs) > 0:
                started_datetime = worklogs[0]["started"]
                periodo = convert_datetime_to_periodo(started_datetime)
                periodos.append(periodo)
        return periodos
        
    except Exception as e:
        logger.warning("Erro ao extrair períodos: %s", e)
        return []