from dotenv import load_dotenv
from src.config import parameters
from src.extract import extract_projetos
from src.load import load_projetos
from atlassian import Jira
import requests

from src.config import jira_api

def main():
    """main."""

    print('Iniciando ETL')
    print('Lendo variáveis de ambiente')
    print(f'JIRA_BASE_URL: {parameters.JIRA_BASE_URL}')
    print(f'JIRA_USERNAME: {parameters.JIRA_USERNAME}')
    print(f'JIRA_PASSWORD: {parameters.JIRA_PASSWORD}')

    projetos = extract_projetos.extrair_todos_projetos()
    load_projetos.carregar_projetos(projetos)

if __name__ == "__main__":
    main()