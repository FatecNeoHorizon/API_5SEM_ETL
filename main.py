from dotenv import load_dotenv
from src.config import parameters
from src.extract import extract_projetos
from src.extract import extract_jira_issues
from src.extract import extract_atividades
from src.extract import extract_periodos
from src.extract import extract_tipos
from src.extract import extract_devs
from src.load import load_projetos
from src.load import load_periodos
from src.load import load_atividades
from src.load import load_tipos
from src.load import load_devs

def main():
    """main."""

    print('Iniciando ETL')
    print('Lendo variáveis de ambiente')
    print(f'JIRA_BASE_URL: {parameters.JIRA_BASE_URL}')
    print(f'JIRA_USERNAME: {parameters.JIRA_USERNAME}')
    print(f'JIRA_PASSWORD: {parameters.JIRA_PASSWORD}')

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

    #Para os métodos de extração / carga das próximas dimensões,
    #Basta criar um método passando a variável 'atividades' como parâmetro
    #Exemplo:   devs = extract_devs(atividades) 
    #           carregar_devs(devs)

if __name__ == "__main__":
    main()