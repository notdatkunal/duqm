from flask_restx import Resource, Namespace
from flask import request ,jsonify
from modules.gatein import services

gatein_ns = Namespace('gatein', description='GateIn api')

@gatein_ns.route('/list')
class GateInList(Resource):
    def get(self):
        from_date = request.args.get("from_date")
        to_date = request.args.get("to_date")
        approved = request.args.get("approved")
        
        result = services.gatein_list_service(from_date,to_date,approved)
        return jsonify(result)


@gatein_ns.route('/create')
class CreateGateInDetails(Resource):
    def post(self):
        data = request.get_json()
        result = services.gate_in_insert_service(data)
        return result


@gatein_ns.route('/approve/<int_gate_in_time>')
class CreateGateInApprove(Resource):
    def post(self, int_gate_in_time):
        """
        Approve Gatein
        
         query param `approved_by`
        -------

        """
        approved_by = request.args.get("approved_by")
        if approved_by is None:
            return {'message':"approved_by is requires in query param"}

        if int_gate_in_time is None or len(int_gate_in_time) < 7:
            return {'message':"int_gate_in_date_time is invalid"}
        result = services.approve_gate_in_service(int_gate_in_time,approved_by)
        return jsonify(result)


@gatein_ns.route('<int_gate_in_time>')
class CreateGateByKey(Resource):

    def post(self, int_gate_in_time):
        """
        Update Gatein

         no_of_packages=?, package_type=?, received_from=?, transporter_name=?, remarks=?
        -------

        """
        if int_gate_in_time is None or len(int_gate_in_time) < 7:
            return {'message': "int_gate_in_date_time is invalid"}
        result = services.update_gate_in_service(int_gate_in_time)
        return jsonify(result)


@gatein_ns.route('/get/<int_gate_in_time>')
class CreateGateGetByKey(Resource):
    def get(self, int_gate_in_time):
        if int_gate_in_time is None or len(int_gate_in_time) < 7:
            return {'message': "int_gate_in_date_time is invalid"}
        print("int_gate_in_time\n",int_gate_in_time)
        return jsonify(services.get_int_gate_obj(int_gate_in_time))
