from flask import request, jsonify
from sqlalchemy import text
from fob_postgres.pg_session import postgres_session
from helpers.exceptions import BadRequestException


def ensure_single_logo_active_role():
    from main import cache
    print(f'this is endpoint {request.endpoint}')
    if (request.endpoint in ("static", None, "/api/docs", '/fob/index.html')
        or request.endpoint.startswith("user")) \
            or "OPTIONS"==request.method or "/fob/" in request.endpoint or 'GET'==request.method or 'login' in request.endpoint:
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
            raise BadRequestException("Two users with role LOGO found please close one")
            # return jsonify({"message": "Two users with role LOGO found please close one",
            #                 "error": "ROLE_CONFLICT"
            #                 }), 400
    elif cache_count > 1:
        # raise UnAuthorizedException("Two users with role LOGO found please close one")
        return jsonify({
            "message": "Two users with role LOGO found please close one",
            "error": "ROLE_CONFLICT"
        }), 400
