from flask import jsonify, request
from flask_restx import Namespace, Resource
from modules.internal_stock import services
from modules.user import services

user_ns = Namespace('user', description='User Management api')

@user_ns.route("")
class UserManagement(Resource):
    def get(self):
        result = services.user_list_service()
        return jsonify(result)

    def post(self):
        '''
        Create User API
        login_id: string;
        id: string;
        name: string;
        rank: string;
        department: string;
        role_name: string;
        customer_code: string;
        added_by: string;
        station_code: string;
        '''
        data = request.get_json()
        result = services.create_user_service(data)
        if result:
            return jsonify({'message':"User created"})
        return {'message':"Something went wrong"},500


@user_ns.route("/close")
class UserClose(Resource):
    def post(self):
        """
        Close User Role
        login_id: string;
        role_name: string;
        """
        login_id = request.get_json().get("login_id")
        role_name = request.get_json().get("role_name")
        user_result = services.close_user_service(login_id, role_name)
        return jsonify({'message': "User Role Deactivated", 'user': user_result})