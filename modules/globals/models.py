from flask_restx import Model, fields

ReqLoginUser = Model('ReqLoginUser', {
    'username': fields.String(required=True, description="this is username "),
    'password': fields.String(required=True, description="this is password"),
})

ResUserModel = Model('ResUser', {
    'username': fields.String(required=True, description="this is username "),
    'token': fields.String(required=True, description="token for auth"),
    'status': fields.String(required=True, description="status for response"),
    'stationcode': fields.String(required=True, description="station of a user"),
    'roles': fields.List(fields.String(required=False, description="roles of user")),
    'rank': fields.String(required=False, description="rank of a user"),
    'message': fields.String(required=False, description="message"),
    'name': fields.String(required=True, description="name of a user"),
    'department': fields.String(required=True, description="dept of a user"),
    'customer_code': fields.String(required=True, description="Customer Code"),
    'customer_name': fields.String(required=True, description="Customer Code"),
})
