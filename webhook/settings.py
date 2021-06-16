import os


# Core settings
API_TOKEN = os.getenv('ENV_API_TOKEN')
MAX_MESSAGE_LENGTH = 4096
MAX_FILE_SIZE = 20480

# TODO: Load configs from Azure Blob Storage
# TOKENIZER_CONFIGS = os.getenv('ENV_TOKENIZER_CONFIGS')
# TRANSFORMER_WEIGHTS_CONFIGS = os.getenv('ENV_TRANSFORMER_WEIGHTS_CONFIGS')

# Miscellaneous settings
DEV_LINK = os.getenv('ENV_DEV_LINK')
REPO_LINK = os.getenv('ENV_REPO_LINK')

# State storage settings
REDIS_HOST = os.getenv('ENV_REDIS_HOST')
REDIS_PORT = int(os.getenv('ENV_REDIS_PORT'))
REDIS_DB = int(os.getenv('ENV_REDIS_DB'))
REDIS_PASSWORD = os.getenv('ENV_REDIS_PASSWORD')
