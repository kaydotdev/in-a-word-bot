from api.app import app
from api.settings.ports import MAIN_MICROSERVICE_PORT

if __name__ == '__main__':
    app.debug = True
    app.run(port=MAIN_MICROSERVICE_PORT)
