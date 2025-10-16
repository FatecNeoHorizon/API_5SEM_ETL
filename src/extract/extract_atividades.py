from src.config import parameters

def extrair_atividades(projetos):
    atividades = []

    try:
        for projeto in projetos:
            projeto_nome = projeto['nome']
            JQL = f'project="{projeto_nome}"'
            data = parameters.JIRA_SESSION.enhanced_jql(JQL)

            for issue in data.get('issues', []):
                fields = issue.get('fields', {})

                status = fields.get('status', {}).get('name', '').lower()
                ativo = status != 'concluído'

                nome = fields.get('summary') or "Atividade sem Título"
                descricao = fields.get('description') or "Descrição não fornecida"

                atividade = {
                    "nome": nome,
                    "descricao": descricao,
                    "atividade_jira_id": issue.get('id'),
                    "ativo": ativo
                }

                atividades.append(atividade)

    except Exception as e:
        print(f"Erro ao extrair atividades: {e}")
        return []
    return atividades 
