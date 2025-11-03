from flask import jsonify, request
from flask_restx import Namespace, Resource
from modules.issue import services
from helpers.exceptions import BadRequestException
from datetime import datetime
issue_ns = Namespace('issue', description='Issue api')

@issue_ns.route("/pending")
class PendingIssue(Resource):
    @issue_ns.param(name="customer_code")
    def get(self):
        """
        Returns pending demands for issue
        query params 
            `customer_code` int required
            `raised_for_customer` int
        """
        customer_code = request.args.get("customer_code")
        raised_for_customer = request.args.get("raised_for_customer")

        if customer_code is None:
            raise BadRequestException("customer_code is required query param")
            customer_code=int(customer_code)
        result = services.pending_issue_service(customer_code=customer_code, raised_for_customer=raised_for_customer)
        return jsonify(result)

    def post(self):
        """
        Saved consumption by demand
            # "int_consumption_no"
            # "customer_code"
            # "int_stock_serial"
            # "item_code"
            # "qty"
            # "issue_to_customer_code"
            # "issued_by"
            # "station_code"
            # "sh_no"
        """
        body = request.get_json()
        if body is None or len(body) <1:
            raise BadRequestException("Consumption body is required")
        result_dict = services.save_issue_service(body)
        return jsonify(result_dict)