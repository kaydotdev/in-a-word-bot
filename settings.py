import os


# Core settings
API_TOKEN = os.getenv('ENV_API_TOKEN')
MAX_MESSAGE_LENGTH = 4096
MAX_FILE_SIZE = 20480
WEBHOOK_ENABLED = os.getenv('ENV_WEBHOOK_ENABLED') == "True"

# Webhook mode settings
WEBHOOK_HOST = os.getenv('ENV_WEBHOOK_HOST')
WEBHOOK_PORT = os.getenv('ENV_WEBHOOK_PORT')
WEBHOOK_PATH = os.getenv('ENV_WEBHOOK_PATH')

WEBAPP_HOST = os.getenv('ENV_WEBAPP_HOST')
WEBAPP_PORT = os.getenv('ENV_WEBAPP_PORT')

# Miscellaneous settings
DEV_LINK = os.getenv('ENV_DEV_LINK')
REPO_LINK = os.getenv('ENV_REPO_LINK')
