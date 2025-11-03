from flask import jsonify, request
from flask_restx import Namespace, Resource
from helpers.commonn_utils import get_path_from_req
from modules.internal_stock import services
from modules.internal_stock.services import import_stock

int_stock_ns = Namespace('internal/stock', description='internal Stock api')


@int_stock_ns.route("/")
class InternalStock(Resource):
    def get(self):
        item_code = request.args.get("item_code")
        page = request.args.get("page", 0)
        rows = request.args.get("rows", 10)

        result = services.internal_stock_list(str(item_code).strip(),int(page),int(rows))
        return jsonify(result)


@int_stock_ns.route('/import')
class ImportSRV(Resource):
    def post(self):
        customer_code = request.form.get('customer_code')
        role = request.form.get('role')
        login_id = request.form.get('login_id')
        sh_no = request.form.get('sh_no')
        station_code = request.form.get('station_code')
        temp_path = get_path_from_req(request)
        import_stock(temp_path, customer_code, login_id, role, station_code, sh_no)


@int_stock_ns.route("/deficiency")
class InternalStockDeficiency(Resource):
    def get(self):
        """
        Stock Deficiency list
        query params
            `interval` values( '0-25', '25-50', '50-75', '75-100' )
            `item_code`
        """
        interval = request.args.get("interval")
        item_code = request.args.get("item_code")
        result = services.deficiency_service(interval, item_code)
        return jsonify(result)
