from flask import jsonify, request
from flask_restx import Namespace, Resource
from modules.internal_gatepass import services as service
int_gatepass_ns = Namespace('internal/gatepass', description='internal GatePass api')


@int_gatepass_ns.route('/<int_gate_pass_no>')
class InternalGatePassDetails(Resource):
    def get(self, int_gate_pass_no: str):
        result_item = service.gate_pass_details(int_gate_pass_no)
        return jsonify(result_item)


@int_gatepass_ns.route('')
class InternalGatePass(Resource):
    def post(self):
        gate_pass_data: dict = request.get_json().get('gatepass')
        cons_list = request.get_json().get('int_consumption_no_list')
        # gate_pass_keys = ['int_gate_pass_no', 'int_gate_pass_key', 'authority_ref', 'transportation_mode', 'transport_no',
        #            'destination', 'escort_name', 'remarks', 'station_code', 'customer_code']
        gate_pass_data.pop('internal_consumption')
        g_no = service.save_gate_pass_entries(gate_pass_data, cons_list)
        return jsonify(g_no)

    def put(self):
        int_gate_pass_list = request.get_json().get('int_gate_pass_no_list')
        approved_by = request.get_json().get('loginId')
        #TODO stock qty to be modified
        service.approve_int_gate_pass(int_gate_pass_list, approved_by)
        return jsonify({'status': "done"})

    def get(self):
        result = service.get_internal_gate_pass()
        return jsonify(result)


@int_gatepass_ns.route('/pending')
class PendingInternalGatePass(Resource):
    @int_gatepass_ns.param(name='customer_code')
    def get(self):
        """

        api for consumptions data pending for internal gatepass

        """
        customer_code = request.args.get('customer_code')
        if customer_code is None:
            return
        result = service.get_pending_internal_gate_pass(customer_code)
        return jsonify(result)
