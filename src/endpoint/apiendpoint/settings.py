import os


# Core settings
API_TOKEN = os.getenv('ENV_API_TOKEN')
MAX_MESSAGE_LENGTH = 4096
MAX_FILE_SIZE = 51200

# Miscellaneous settings
DEV_LINK = os.getenv('ENV_DEV_LINK')
REPO_LINK = os.getenv('ENV_REPO_LINK')

# State storage settings
MONGO_CONNECTION_URL = os.getenv('ENV_MONGO_CONNECTION_URL')

# Request data storage
REQUEST_STORAGE_CONNECTION_STRING = os.getenv('ENV_REQUEST_STORAGE_CONNECTION_STRING')
