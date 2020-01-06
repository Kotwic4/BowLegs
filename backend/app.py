import logging.config
import logging.config
import os

from flask import Flask, Blueprint

from api.api import api
from api.endpoints.pictures import ns as picture_namespace
import settings
from database import db_session, init_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def initialize_app(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(picture_namespace)
    flask_app.register_blueprint(blueprint)
    init_db()


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://0.0.0.0:{}/api/ <<<<<'.format(settings.PORT))
    app.run(host='0.0.0.0', port=settings.PORT, debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
