from flask import jsonify, request
from flask_restx import Namespace, Resource
from modules.dashboard import services

dashboard_ns = Namespace('dashboard', description='dashboard api')


@dashboard_ns.route("/chart/bar")
class DashboardBarChart(Resource):
    def get(self):
        module = request.args.get("module", default="consumption")
        result = services.fetch_bar_chart_service(module)
        return jsonify(result)


@dashboard_ns.route("/pending")
class DashboardBarChart(Resource):
    def get(self):
        customer_code = request.args.get("customer_code")
        result = services.fetch_pending_status(customer_code)
        return jsonify(result)


@dashboard_ns.route("/inventory/size")
class DashboardInventorySize(Resource):
    def get(self):
        result = services.inventory_size_service()
        return jsonify(result[0])


@dashboard_ns.route("/recent-activity")
class DashboardRecentActivity(Resource):
    @dashboard_ns.param(name="module")
    def get(self):
        module = request.args.get("module", default='consumption')
        result = services.recent_activity_service(module)
        return jsonify(result)
