from api.app import app
from api.settings.ports import AI_MICROSERVICE_PORT
from api.settings.launch import DEBUG_MODE

if __name__ == '__main__':
    app.debug = DEBUG_MODE
    app.run(port=AI_MICROSERVICE_PORT)
