from flask_restx import Resource, Namespace
import pandas as pd
import numpy as np
from flask import request, jsonify
from fob_postgres import functions as pf
from modules.gatepass import services

gatepass_ns = Namespace('gatepass', description='GatePass api')


@gatepass_ns.route('/import')
class GatePassImport(Resource):
    def post(self):
        file = request.files['file']
        customer_code = request.form.get('customer_code')
        print(f'this is customer code{customer_code}')
        return services.import_gatepass_service(file, int(customer_code.strip()))


@gatepass_ns.route('/gatein-not-made')
class GatePassNotMade(Resource):
    def get(self):
        return jsonify(services.gatein_not_made_service())


@gatepass_ns.route('/list')
class GatePassList(Resource):
    """
    Returns list

    `from_date` , `to_date`, `gate_pass_key`
    -------

    """

    def get(self):
        from_date = request.args.get("from_date")
        to_date = request.args.get("to_date")
        gate_pass_key = request.args.get("gate_pass_key")
        result = services.gatepass_list_service(from_date=from_date, to_date=to_date, gate_pass_key=gate_pass_key)
        return jsonify(result)


@gatepass_ns.route('/<gate_pass_key>')
class GatePassByGatePassKey(Resource):
    """
    Returns list
    -------

    """

    def get(self, gate_pass_key):
        result = services.gate_pass_by_gatepass_key(gate_pass_key)
        return jsonify(result)
