from src.config import parameters
import logging

logger = logging.getLogger(__name__)


def extrair_todos_devs(jira_devs):
    back_devs = []

    try:
        for jira_dev in jira_devs:
            issue_dev = jira_dev["fields"]["assignee"]

            if not issue_dev or not issue_dev.get("displayName"):
                continue

            back_tipo = dict(nome=issue_dev["displayName"])
            back_devs.append(back_tipo)

        return back_devs

    except Exception as e:
        logger.warning("Erro ao extrair os desenvolvedores: %s", e)
        return []
