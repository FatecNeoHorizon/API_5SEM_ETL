from dotenv import load_dotenv #pip install python-dotenv
import os

from src.config import jira_api

load_dotenv()

JIRA_BASE_URL =  os.getenv("JIRA_BASE_URL")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD")

JIRA_SESSION = jira_api.start_jira_session()

BACK_BASE_URL = os.getenv("BACK_BASE_URL")