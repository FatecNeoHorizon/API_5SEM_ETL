from dotenv import load_dotenv
from src.config import parameters
from src.extract import extract_projetos
from src.extract import extract_atividades
from src.extract import extract_periodos
from src.load import load_projetos
from src.load import load_periodos
from src.load import load_atividades

def main():
    """main."""

    print('Iniciando ETL')
    print('Lendo variáveis de ambiente')
    print(f'JIRA_BASE_URL: {parameters.JIRA_BASE_URL}')
    print(f'JIRA_USERNAME: {parameters.JIRA_USERNAME}')
    print(f'JIRA_PASSWORD: {parameters.JIRA_PASSWORD}')

    projetos = extract_projetos.extrair_todos_projetos()
    load_projetos.carregar_projetos(projetos)

    atividades = extract_atividades.extrair_atividades(projetos)
    load_atividades.carregar_atividades(atividades)

    periodos = extract_periodos.extrair_periodos(atividades)
    load_periodos.carregar_periodos(periodos)

    #Para os métodos de extração / carga das próximas dimensões,
    #Basta criar um método passando a variável 'atividades' como parâmetro
    #Exemplo:   devs = extract_devs(atividades) 
    #           carregar_devs(devs)

    

if __name__ == "__main__":
    main()