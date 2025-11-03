from flask_restx import Model, fields

CreateDemandModel = Model('CreateDemand', {
    'username': fields.String(required=True, description="this is username "),
})