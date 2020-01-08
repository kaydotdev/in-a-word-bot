from api.app import app
from api.settings.apisettings import IS_IN_DEBUG_MODE, API_PORT

if __name__ == '__main__':
    app.debug = IS_IN_DEBUG_MODE
    app.run(port=API_PORT)
