from src.config import parameters


def extrair_todos_projetos():
    back_projetos = []

    try:
        jira_projetos = parameters.JIRA_SESSION.get_all_projects()
        for jira_projeto in jira_projetos:
            projeto_id = jira_projeto.get('id')
            if not projeto_id:
                print(f"Projeto Jira sem 'id' encontrado: {jira_projeto}. Pulando...")
                continue

            back_projeto = dict(
                nome = jira_projeto.get('name'),
                key = jira_projeto.get('key'),
                projeto_jira_id = projeto_id,
            )

            back_projetos.append(back_projeto)

        return back_projetos

    except Exception as e:
        print(f"Erro ao extrair projetos: {e}")
        return []