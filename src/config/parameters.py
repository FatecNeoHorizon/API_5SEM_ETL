from dotenv import load_dotenv
import os

from src.config import jira_api

load_dotenv()

JIRA_BASE_URL =  os.getenv("JIRA_BASE_URL")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD")

JIRA_SESSION = jira_api.start_jira_session()

BACK_BASE_URL = os.getenv("BACK_BASE_URL")

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

BACK_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJVc2VyRGV0YWlscyI6IntcImVtYWlsXCI6XCJldGxAbmVvaG9yaXpvbi5jb21cIixcInBhc3N3b3JkXCI6bnVsbCxcInJvbGVUeXBlc1wiOltcIkVUTFwiXSxcImF1dGhvcml0aWVzXCI6W1wiRVRMXCJdfSIsImlzcyI6ImJyLmNvbS5uZW9ob3Jpem9uIiwic3ViIjoiZXRsQG5lb2hvcml6b24uY29tIiwiZXhwIjoxNzYzOTI5NDI2fQ.uwR9Qk7YTAzshXIn5awpAr5gF-7JPwzJj44XxM8OKhqB29CzLylXx_8YWLwtjIkJGSWCqaPjSL3HhLSpjZEShg"