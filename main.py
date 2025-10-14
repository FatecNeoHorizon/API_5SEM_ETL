from dotenv import load_dotenv
from src.config import parameters
from src.extract import extract_projetos
from src.extract import extract_atividades
from src.extract import extract_periodos
from src.load import load_projetos
from src.load import load_periodos

def main():
    """main."""

    print('Iniciando ETL')
    print('Lendo variáveis de ambiente')
    print(f'JIRA_BASE_URL: {parameters.JIRA_BASE_URL}')
    print(f'JIRA_USERNAME: {parameters.JIRA_USERNAME}')
    print(f'JIRA_PASSWORD: {parameters.JIRA_PASSWORD}')

    projetos = extract_projetos.extrair_todos_projetos()
    load_projetos.carregar_projetos(projetos)

    atividades = extract_atividades.extract_atividades(projetos)

    #Para os métodos de extração / carga das próximas dimensões,
    #Basta criar um método passando a variável 'atividades' como parâmetro
    #Exemplo:   devs = extract_devs(atividades) 
    #           carregar_devs(devs)

    periodos = extract_periodos.extract_periodos(atividades)
    load_periodos.carregar_periodos(periodos)

if __name__ == "__main__":
    main()