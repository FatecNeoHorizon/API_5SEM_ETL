import logging
from src.config import parameters

logger = logging.getLogger(__name__)


def extrair_todos_projetos():
    back_projetos = []

    try:
        jira_projetos = parameters.JIRA_SESSION.get_all_projects()
        for jira_projeto in jira_projetos:
            projeto_id = jira_projeto.get('id')
            if not projeto_id:
                logger.error("Projeto Jira sem 'id' encontrado: %s. Pulando...", jira_projeto)
                continue

            back_projeto = dict(
                nome = jira_projeto.get('name'),
                key = jira_projeto.get('key'),
                projeto_jira_id = projeto_id,
            )
            back_projetos.append(back_projeto)

        return back_projetos

    except Exception as e:
        logger.error("Erro ao extrair projetos: %s", e)
        return []