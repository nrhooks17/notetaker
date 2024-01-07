from flask import Blueprint, current_app, jsonify
from flask import request

errors_blueprint = Blueprint('api_errors', __name__)


# 400 error handler
@errors_blueprint.app_errorhandler(400)
def bad_request_400(error):
    current_app.logger.error(f'bad request: {error}')
    current_app.logger.info(f'inside of bad_request_400()')
    return jsonify(error=str(error)), 400

