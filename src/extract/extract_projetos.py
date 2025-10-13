from src.config import parameters


def extrair_todos_projetos():
    back_projetos = []

    try:
        jira_projetos = parameters.JIRA_SESSION.get_all_projects()
        for jira_projeto in jira_projetos:
            
            back_projeto = dict(
                nome = jira_projeto['name'],
                key = jira_projeto['key'],
                projeto_jira_id = jira_projeto['id']  )
            
            back_projetos.append(back_projeto)

        return back_projetos

    except Exception as e:
        print(e)
        return[]