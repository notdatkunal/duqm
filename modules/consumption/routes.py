from flask import request, jsonify
from flask_restx import Resource, Namespace
from sqlalchemy import text, func, and_
from datetime import datetime
from modules.consumption import services
from helpers import exceptions

consumption_ns = Namespace('consumption', description='duqm consumption api')


@consumption_ns.route('')
class Consumption(Resource):
    def put(self):
        login_id: str = request.get_json().get('loginId')
        consumption_list: list = request.get_json().get('int_cunsumption_no_list')
        services.approve_consumptions(consumption_list, login_id)
        return {'status': 'done'}

    @consumption_ns.param(name='status')
    @consumption_ns.param(name='closed')
    def get(self):
        """
        Consumption List
        query param

            `status`
            `closed` (bool)
            `self_customer_code` send self customer code in case of issue only
            `self_consumptions` send self_consumptions false in case of issue only default true
        -------

        """
        status = request.args.get('status')
        closed = request.args.get('closed')
        self_customer_code = request.args.get('self_customer_code')
        self_consumptions = request.args.get('self_consumptions', default='true')
        r_data = services.get_data_consumption(status, closed, self_customer_code, self_consumptions)
        return jsonify(r_data)


@consumption_ns.route('/initiate')
class InitiateConsumption(Resource):

    def get(self):
        """
        Returns  Stock List with item 
        query param

            `item_code`
        -------

        """
        item_code = request.args.get('item_code')
        print("item_code ", item_code)
        result = services.stock_list_service(item_code)
        return jsonify(result)

    def post(self):
        cons_list = request.get_json().get('consumptions')
        required_list = self.create_list_req(cons_list)
        services.save_multiple_consumptions(required_list)
        return {'status': 'done'}

    def create_list_req(self, cons_list):
        required_list: list = []
        # print(list_[0].keys())
        # 'date_time_issued' = take current date time
        # 'item desc not reqd'
        # 'iwo serial must be null' but not to hardcoded / keep it on frontend side
        # int _consumption no to be generated in runtime
        # all other fields are nullable
        cons_key = ['consumption_type', 'customer_code', 'issue_to_customer_code',
                    'issued_by', 'iwo_srl', 'item_code', 'qty', 'sh_no', 'station_code']
        for item in cons_list:
            required_obj = {}
            for key in cons_key:
                required_obj[key] = item[key]
            required_list.append(required_obj)
        return required_list


@consumption_ns.route('/close')
class CloseConsumption(Resource):
    def put(self):
        """
        Close Consumption
        request body

            `login_id` str required
            `int_consumption_no_list` list[int] required 
        -------

        """
        int_consumption_no_list = request.get_json().get("int_consumption_no_list")
        login_id = request.get_json().get("login_id")
        if int_consumption_no_list is None:
            raise exceptions.BadRequestException("int_consumption_no_list IS required")
        login_id = request.get_json().get("login_id")
        if login_id is None:
            raise exceptions.BadRequestException("login_id query param IS required")
        res = services.close_consumption_service(int_consumption_no_list, login_id)
        if res == True:
            return {'message': "Success"}


@consumption_ns.route("/<int_gate_pass_no>")
class ConsumptionByGatePassNo(Resource):
    def get(self, int_gate_pass_no):
        return jsonify(services.get_consumption_by_gate_pass_no(int_gate_pass_no))
