from dotenv import load_dotenv
import os

from src.config import jira_api

load_dotenv()

JIRA_BASE_URL =  os.getenv("JIRA_BASE_URL")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD")

JIRA_SESSION = jira_api.start_jira_session()

BACK_BASE_URL = os.getenv("BACK_BASE_URL")
BACK_ETL_USUARIO = os.getenv("BACK_ETL_USUARIO")
BACK_ETL_SENHA = os.getenv("BACK_ETL_SENHA")
BACK_TOKEN = ""
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

