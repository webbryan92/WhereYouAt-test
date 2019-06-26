from flask import Flask, g, jsonify

from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr

from auth import auth

import config
import models
from resources.users import users_api
from resources.events import events_api
from resources.rooms import rooms_api

app = Flask(__name__)
app.register_blueprint(users_api, url_prefix='/api/v1')
app.register_blueprint(events_api, url_prefix='/api/v1')

limiter = Limiter(app,global_limits=[config.DEFAULT_RATE], key_func=get_ipaddr)
limiter.limit("40/day")(users_api)
limiter.limit("5/day", per_method=True,
                methods=["post", "put", "delete"])(events_api)
# limiter.exempt(events_api)
# limiter.exempt(rooms_api)


@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/api/v1/users/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)