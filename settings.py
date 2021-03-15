import os


# Bot settings
API_TOKEN = os.getenv('ENV_API_TOKEN')

WEBHOOK_ENABLED = os.getenv('ENV_WEBHOOK_ENABLED') == "True"
WEBHOOK_DOMAIN = os.getenv('ENV_WEBHOOK_DOMAIN')
WEBHOOK_PORT = os.getenv('ENV_WEBHOOK_PORT')
WEBHOOK_IP = os.getenv('ENV_WEBHOOK_IP')
WEBHOOK_PATH = os.getenv('ENV_WEBHOOK_PATH')

# Meta-ranking variables
MAX_SOURCE_POOL = int(os.getenv('ENV_MAX_SOURCE_POOL'))

# Messages settings
DEV_LINK = os.getenv('ENV_DEV_LINK')
REPO_LINK = os.getenv('ENV_REPO_LINK')
