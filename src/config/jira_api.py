from src.config import parameters
from atlassian import Jira
import requests

def start_jira_session():

    session = requests.Session()
    jira = Jira(
    url = parameters.JIRA_BASE_URL,
    username = parameters.JIRA_USERNAME,
    password = parameters.JIRA_PASSWORD,
    cloud=True,  # Ensure this is set to True for Jira Cloud
    session=session  # Optional: use a session for persistent connections
    )

    return jira