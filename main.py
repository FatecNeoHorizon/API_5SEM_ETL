from dotenv import load_dotenv
from src.config import parameters
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

    data = parameters.JIRA_SESSION.get_all_projects()
    print(data)

if __name__ == "__main__":
    main()