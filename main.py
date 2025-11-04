import http
import os
import time
import webbrowser
from datetime import timedelta
from flask import Flask, jsonify
from os import getenv
from flask import send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from fob_postgres.db_utils import ensure_single_logo_active_role
from helpers.exceptions import AppException, TokenExpiredException, NotFoundAppException
from modules.issue.routes import issue_ns
from modules.globals.routes import global_ns
from modules.demand.routes import demand_ns
from modules.gatein.routes import gatein_ns
from modules.gatepass.routes import gatepass_ns
from modules.dashboard.routes import dashboard_ns
from modules.internal_gatepass.routes import int_gatepass_ns
from modules.store_receipt.routes import srv_ns
from modules.consumption.routes import consumption_ns
from modules.internal_stock.routes import int_stock_ns
from modules.user.routes import user_ns
from flask_restx import Api
from helpers.handlers import before_request_handler, after_request_handler
from helpers.exceptions import BadRequestException
from werkzeug.exceptions import MethodNotAllowed, NotFound
from config.config import config
from flask import render_template
from flask_caching import Cache

app = Flask(__name__, template_folder='templates/dist')
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'jwt token required'
    }
}
api = Api(app, version='0.1'
          , title='duqm backend'
          , authorizations=authorizations
          , description='Duqm module'
          , security='Bearer Auth'
          , doc='/api/docs'
          )

app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)
app.config['SECRET_KEY'] = 'ilmsdev'
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
app.config['SWAGGER_UI_CUSTOM_CSS'] = 'static/custom.css'
# app.config['SWAGGER_UI_PERSIST_AUTHORIZATION'] = 'True'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fob_module')


def token_timeout(token_name='access'):
    # from audit_application.services.host_service import is_dev
    if token_name == 'refresh':
        return timedelta(hours=7)
    else:
        return timedelta(minutes=60)


app.config['JWT_ACCESS_TOKEN_EXPIRES'] = token_timeout()
# app.config['JWT_REFRESH_TOKEN_EXPIRES'] = token_timeout(token_name='refresh')
app.config['JWT_ERROR_MESSAGE_KEY'] = 'session expired'
cors = CORS(app, origins='*', supports_credentials=True, expose_headers='Authorization')

api.add_namespace(global_ns)
api.add_namespace(demand_ns)
api.add_namespace(gatein_ns)
api.add_namespace(gatepass_ns)
api.add_namespace(srv_ns)
api.add_namespace(consumption_ns)
api.add_namespace(int_gatepass_ns)
api.add_namespace(dashboard_ns)
api.add_namespace(user_ns)
api.add_namespace(int_stock_ns)
api.add_namespace(issue_ns)
# auth repo
# app.before_request(load_auth)
app.before_request(before_request_handler)
app.before_request(ensure_single_logo_active_role)
app.after_request(after_request_handler)
jwt = JWTManager(app)

cache = Cache(app, config={"CACHE_TYPE": "simple"})


@app.route('/fob/<path:path>')
def base_url(path):
    dist_path = os.path.join(app.template_folder)
    file_path = os.path.join(dist_path, path)
    if os.path.exists(file_path):
        return send_from_directory(dist_path, path)
    else:
        # If the file doesn’t exist, serve index.html so React Router can handle it
        return send_from_directory(dist_path, 'index.html')


# Optional: handle /fob (without trailing slash)
@app.route('/fob')
def serve_fob_root():
    return send_from_directory(app.template_folder, 'index.html')


@app.get('/imports')
def home():
    return render_template('index.html')


@app.route('/')
def root_index():
    """Serve a simple landing page with a button to open /fob."""
    # Serve a lightweight static HTML that links to /fob so users visiting base URL
    # can navigate into the React app mounted at /fob
    return send_from_directory(app.template_folder, 'root_index.html')


@app.errorhandler(AppException)
def exception_handler(e: AppException):
    return jsonify({'message': str(e.args)}), e.error_code


@app.errorhandler(Exception)
def exception_handler(e: Exception):
    import traceback
    print(f'traceback for the error is : {traceback.format_exc()}')
    return jsonify({'message': e.args}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@app.errorhandler(TokenExpiredException)
def exception_handler(e: TokenExpiredException):
    return jsonify({'message': e.message}), http.HTTPStatus.UNAUTHORIZED


@app.errorhandler(NotFoundAppException)
def exception_handler(e: NotFoundAppException):
    return jsonify({'message': e.message}), http.HTTPStatus.NOT_FOUND


@app.errorhandler(BadRequestException)
def bad_request_handler(e: BadRequestException):
    return jsonify({'message': e.message}), http.HTTPStatus.BAD_REQUEST


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    return jsonify({
        "message": "This endpoint does not support the requested HTTP method"
    }), http.HTTPStatus.METHOD_NOT_ALLOWED


@app.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({
        "message": "URI not found",
    }), http.HTTPStatus.NOT_FOUND


def open_browser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:8989/fob')


if __name__ == '__main__':
    open_browser()
    print("\n-----------\n")
    print(f"App started on port {config.PORT}")
    print("\n-----------\n")
    app.run(host='0.0.0.0', port=config.PORT, debug=True)
