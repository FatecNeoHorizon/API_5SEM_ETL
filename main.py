from src.config import parameters
from src.utils.inserir_periodo_coringa import inserir_periodo_coringa
from src.extract import extract_projetos
from src.extract import extract_jira_issues
from src.extract import extract_atividades
from src.extract import extract_periodos
from src.extract import extract_tipos
from src.extract import extract_status
from src.extract import extract_devs
from src.extract import extract_fato_atividades
from src.extract import extract_fato_apontamento_horas
from src.load import load_projetos
from src.load import load_periodos
from src.load import load_atividades
from src.load import load_tipos
from src.load import load_devs
from src.load import load_status
from src.load import load_fato_atividades
from src.load import load_fato_apontamento_horas

def main():
    """main."""

    print('Iniciando ETL')
    print('Lendo variáveis de ambiente')
    print(f'JIRA_BASE_URL: {parameters.JIRA_BASE_URL}')
    print(f'JIRA_USERNAME: {parameters.JIRA_USERNAME}')
    print(f'JIRA_PASSWORD: {parameters.JIRA_PASSWORD}')
    print(f'BACK_BASE_URL: {parameters.BACK_BASE_URL}')

    inserir_periodo_coringa()

    projetos = extract_projetos.extrair_todos_projetos()
    load_projetos.carregar_projetos(projetos)

    jira_issues = extract_jira_issues.extrair_jira_issues(projetos)

    atividades = extract_atividades.extrair_atividades(jira_issues)
    load_atividades.carregar_atividades(atividades)

    periodos = extract_periodos.extrair_periodos(jira_issues)
    load_periodos.carregar_periodos(periodos)

    tipos = extract_tipos.extrair_todos_tipos(jira_issues)
    load_tipos.carregar_tipos(tipos)

    devs = extract_devs.extrair_todos_devs(jira_issues)
    load_devs.carregar_devs(devs)

    status_array = extract_status.extrair_todos_status(jira_issues)
    load_status.carregar_status(status_array)

    fato_atividade_dict = extract_fato_atividades.extrair_todos_fatos_atividades(jira_issues, projetos, status_array, tipos)
    load_fato_atividades.carregar_fato_atividades(fato_atividade_dict)

    fato_apontamento_horas_dict = extract_fato_apontamento_horas.extrair_todos_fatos_apontamento_horas(jira_issues, atividades, projetos, devs)
    load_fato_apontamento_horas.carregar_fato_apontamento_horas(fato_apontamento_horas_dict)


if __name__ == "__main__":
    main()