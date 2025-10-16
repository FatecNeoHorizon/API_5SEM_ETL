from src.config import parameters

def extrair_jira_issues(projetos):
    atividades = []

    try:
        for projeto in projetos:
            projeto_nome = projeto['nome']
            JQL = f'project="{projeto_nome}"'
            data = parameters.JIRA_SESSION.enhanced_jql(JQL)

            atividades += data['issues']

    except Exception as e:
        print(f"Erro ao extrair JIRA Isuues: {e}")
        return []
    return atividades 