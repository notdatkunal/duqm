from os import getenv
from flask import request
from jwt import ExpiredSignatureError, InvalidTokenError
from helpers.constants import PUBLIC_ENDPOINTS
from helpers.exceptions import TokenExpiredException


def load_auth():
    print(f'this is path {request.path}')
    if request.path in PUBLIC_ENDPOINTS or request.method == 'OPTIONS' or 'swagger' in request.path or 'static' in request.path:
        return
    if '/file' in request.path and request.method == 'GET':
        return
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise TokenExpiredException(message='token absent')
    token = auth_header.split(None, 1)[1]
    from jwt import decode
    try:
        payload = decode(token, getenv('JWT_SECRET_KEY', 'your-secret-key'), algorithms=['HS256'])
        return
    except ExpiredSignatureError:
        raise TokenExpiredException()
    except InvalidTokenError:
        raise TokenExpiredException(message='invalid token found')
