from src.config import parameters
import logging

logger = logging.getLogger(__name__)

def extrair_atividades(jira_issues):
    atividades = []

    try:
        
        for issue in jira_issues:
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
        logger.warning("Erro ao extrair atividades: %s", e)
        return []
    return atividades
