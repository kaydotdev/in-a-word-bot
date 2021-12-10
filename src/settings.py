import os


# Core settings
API_TOKEN = os.getenv("ENV_API_TOKEN")
MAX_MESSAGE_LENGTH = int(os.getenv("ENV_MAX_MESSAGE_LENGTH") or 0)
MAX_FILE_SIZE = int(os.getenv("ENV_MAX_FILE_SIZE") or 0)

REPO_LINK = os.getenv("ENV_REPO_LINK")
DEV_LINK = os.getenv("ENV_DEV_LINK")

WEBHOOK_MODE = os.getenv('ENV_WEBHOOK_MODE') == "True"

# webhook settings (optional if WEBHOOK_MODE is False)
WEBHOOK_HOST = os.getenv("ENV_WEBHOOK_HOST")
WEBHOOK_PATH = os.getenv("ENV_WEBHOOK_PATH")
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = os.getenv("ENV_WEBAPP_HOST")
WEBAPP_PORT = int(os.getenv("ENV_WEBAPP_PORT") or 0)
