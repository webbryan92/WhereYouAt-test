from flask import Flask

import models
from resources.users import users_api
from resources.events import events_api

DEBUG = True
HOST = 'localhost'
PORT = 8000

app = Flask(__name__)
app.register_blueprint(users_api, url_prefix='/api/v1')
app.register_blueprint(events_api, url_prefix='/api/v1')

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)