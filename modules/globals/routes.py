import os
from flask import request, jsonify, send_from_directory
from flask_jwt_extended import create_access_token
from modules.imports.import_service import import_data
import pandas as pd
from helpers.exceptions import AppException
from modules.globals.models import ResUserModel, ReqLoginUser
from flask_restx import Resource, Namespace
from modules.globals.services import check_username_pg, validate_pg, list_closing_codes, list_priority_codes, \
    list_ship_customers, list_code_values
from helpers.constants import Check
from modules.globals import services

global_ns = Namespace('globals', description='duqm srv api')
global_ns.models[ResUserModel.name] = ResUserModel
global_ns.models[ReqLoginUser.name] = ReqLoginUser


@global_ns.route('/download')
class Download(Resource):
    @global_ns.param('path', default='', description='input path here ')
    def get(self):
        partial_path = request.args.get('path')
        try:
            print(f'this is path {partial_path}')
            return send_from_directory(os.path.dirname(partial_path), partial_path.split('\\').pop(),
                                       as_attachment=True)
        except FileNotFoundError as e:
            raise AppException(message=e.args, error_code=404)


@global_ns.route('/code/closing')
class ClosingCode(Resource):
    def get(self):
        results_data = list_closing_codes()
        return jsonify(results_data)


@global_ns.route('/code/priority')
class PriorityCode(Resource):
    def get(self):
        results_data = list_priority_codes()
        return jsonify(results_data)


@global_ns.route('/code/data/<column_name>')
class CodeTable(Resource):
    def get(self, column_name: str):
        """
        example Parameters = IntStoreReceiptChoice
        ----------
        column_name

        """
        results_data = list_code_values(column_name)
        return jsonify(results_data)


@global_ns.route('/import')
class Import(Resource):
    def post(self):
        file_data = request.files['file']
        df = pd.read_csv(file_data)
        print(df.head())
        print(df.keys())
        import_data(df)
        response = jsonify({'status': f'successful'})
        response.status = 200
        return response


@global_ns.route('/customers')
class Customers(Resource):
    def get(self):
        results_data = list_ship_customers()
        return jsonify(results_data)


@global_ns.route('/login')
@global_ns.doc(security=None)
class Login(Resource):
    @global_ns.marshal_with(ResUserModel)
    @global_ns.expect(ReqLoginUser, validate=True)
    def post(self):
        """
        login api for duqm user
        """
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        check: bool = check_username_pg(username)
        validation: bool = False
        count: int = 0
        print(f'proof that this exists {check}')
        while check and not validation and (count < 3):
            validation = validate_pg(username, password)
            print(f'checking login')
            count += 1

        check = check and validation
        if not check:
            response_data = {
                'status': Check.INVALID.name
                , 'username': username
                , 'message': 'wrong credentials'
            }
            return response_data, 401
        access_token = create_access_token(identity=username)

        user_details = services.fetch_user_details(username=username)
        user_details['token'] = access_token
        user_details['status'] = Check.VALID
        user_details['message'] = "Login success"
        return user_details


@global_ns.route('/stationcode')
@global_ns.doc(security=None)
class StationCode(Resource):
    def get(self):
        """
        Returns Station codes
        -------

        """
        return jsonify(services.station_code_service())


@global_ns.route('/packagetype')
@global_ns.doc(security=None)
class PackageType(Resource):
    def get(self):
        """
        Returns Package type
        -------

        """
        return jsonify(services.package_type_service())


@global_ns.route('/received-from')
class ReceivedFrom(Resource):
    def get(self):
        """
        Returns Received from 
        -------

        """
        return jsonify(services.received_from_service())


@global_ns.route('/stores')
@global_ns.doc(security=None)
class InternalSH(Resource):
    def get(self):
        """
        Returns stores
        -------

        """
        return jsonify(services.internal_sh())

@global_ns.route("/address/<customer_code>")
@global_ns.param("customer_code","Customer Code",type="string")
class CustomerAddress(Resource):
    def get(self,customer_code):
        """
        Returns address of customer
        
        """
        # customer_address_service
        return jsonify(services.customer_address_service(customer_code))