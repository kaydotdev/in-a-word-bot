import os


# Core settings
API_TOKEN = os.getenv("API_TOKEN")
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH") or 0)
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE") or 0)

REPO_LINK = os.getenv("REPO_LINK")
DEV_LINK = os.getenv("DEV_LINK")

# webhook settings
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = os.getenv("WEBAPP_HOST")
WEBAPP_PORT = os.getenv("WEBAPP_PORT")
