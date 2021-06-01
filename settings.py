import os


# Core settings
API_TOKEN = os.getenv('ENV_API_TOKEN')
WEBHOOK_ENABLED = os.getenv('ENV_WEBHOOK_ENABLED') == "True"

# Webhook mode settings
WEBHOOK_DOMAIN = os.getenv('ENV_WEBHOOK_DOMAIN')
WEBHOOK_PORT = os.getenv('ENV_WEBHOOK_PORT')
WEBHOOK_IP = os.getenv('ENV_WEBHOOK_IP')
WEBHOOK_PATH = os.getenv('ENV_WEBHOOK_PATH')

# Miscellaneous settings
DEV_LINK = os.getenv('ENV_DEV_LINK')
REPO_LINK = os.getenv('ENV_REPO_LINK')
