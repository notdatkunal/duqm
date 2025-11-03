import http
import os
from datetime import timedelta
from flask import Flask, jsonify
from os import getenv
from flask import send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from helpers.constants import fetch_origins
from helpers.exceptions import AppException, TokenExpiredException, NotFoundAppException, UnAuthorizedException
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
from security.auth import load_auth
from fob_sybase.DBConfigs import is_dev
from helpers.exceptions import BadRequestException
from werkzeug.exceptions import MethodNotAllowed, NotFound
from config.config import config
from flask import render_template, request
from flask_caching import Cache
from fob_postgres.pg_session import postgres_session
from sqlalchemy import text

app = Flask(__name__)
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
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=(1000 if is_dev() else 8))
app.config['SECRET_KEY'] = 'ilmsdev'
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
app.config['SWAGGER_UI_CUSTOM_CSS'] = 'static/custom.css'
# app.config['SWAGGER_UI_PERSIST_AUTHORIZATION'] = 'True'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fob_module')


def token_timeout(token_name='access'):
    # from audit_application.services.host_service import is_dev
    if token_name == 'refresh':
        if is_dev():
            return timedelta(days=30)
        else:
            return timedelta(hours=7)
    else:
        if is_dev():
            return timedelta(hours=70)
        else:
            return timedelta(minutes=60)


print(fetch_origins())
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
app.after_request(after_request_handler)
jwt = JWTManager(app)

cache = Cache(app, config={"CACHE_TYPE": "simple"})


@app.route('/fob/<path:filename>')
def base_url(filename):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DIST_DIR = os.path.join(BASE_DIR, 'templates', 'dist')
    file_path = os.path.join(DIST_DIR, filename)
    print(f'this is path {file_path}')
    return send_from_directory(DIST_DIR, filename, as_attachment=False)


@app.before_request
def ensure_single_logo_active_role():
    if (request.endpoint in ("static", None, "/api/docs")
        or request.endpoint.startswith("user")) \
            or request.method == "OPTIONS":
        return
    cache_count = cache.get("cache_count")
    if cache_count is None:
        sess = postgres_session.get_session()
        count = sess.execute(text("""
        select count(*) from fob_users u 
            join fob_user_role r on u.login_id = r.login_id
                where r.date_time_closed is null
                    and r.role_name = 'LOGO'
        """)).one()[0]
        cache.set("role_conflict", cache_count, timeout=60)
        if count > 1:
            # raise UnAuthorizedException("Two users with role LOGO found please close one")
            return jsonify({"message": "Two users with role LOGO found please close one",
                            "error": "ROLE_CONFLICT"
                            }), 400
    elif cache_count > 1:
        # raise UnAuthorizedException("Two users with role LOGO found please close one")
        return jsonify({
            "message": "Two users with role LOGO found please close one",
            "error": "ROLE_CONFLICT"
        }), 400


@app.get('/imports')
def home():
    return render_template('index.html')


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


if __name__ == '__main__':
    # is_working()
    print("\n-----------\n")
    print(f"App started on port {config.PORT}")
    print("\n-----------\n")
    app.run(host='0.0.0.0', port=config.PORT, debug=True)
