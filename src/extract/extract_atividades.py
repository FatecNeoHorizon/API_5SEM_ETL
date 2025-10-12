from src.config import parameters


def extract_atividades(projetos):
    atividades = []

    try:

        for projeto in projetos:

            projeto_nome = projeto['nome']
            JQL = f'project="{projeto_nome}"'
            data = parameters.JIRA_SESSION.enhanced_jql(JQL)

            atividades += data['issues']

        return atividades
    except Exception as e:
        print(e)
        return[]

    
