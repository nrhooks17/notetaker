import os
import logging
from flask import Flask
from flask_cors import CORS
from api.routes import api_blueprint
from api.errors import errors_blueprint
from pymongo import MongoClient


def create_app():
    app = Flask(__name__)

    # CORS is used here to allow cross-origin requests from the frontend.
    CORS(app)

    # set logging level to debug if we are in development mode.
    if os.getenv('FLASK_ENV') == 'development':
        app.logger.setLevel(logging.DEBUG)

    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(errors_blueprint)
    app.mongo_client = MongoClient(os.getenv('MONGO_URI'))

    # setting the amount_per_page variable in the app context so that it can be accessed by other parts of the app.
    with app.app_context():
        app.amount_per_page = int(os.getenv('AMOUNT_PER_PAGE', 10))

    # These values are set in the docker-compose.yml file and Kubernetes deployment file if we decide to use Kubernetes.
    # They need to be converted to boolean values because os.getenv() always returns a string.
    app.config['TESTING'] = True if os.getenv('APP_TESTING') == 'True' else False
    app.config['DEBUG'] = True if os.getenv('APP_DEBUG') == 'True' else False
    app.config['ENV'] = os.getenv('FLASK_ENV')
    app.config['AMOUNT_PER_PAGE'] = os.getenv('AMOUNT_PER_PAGE')

    return app
