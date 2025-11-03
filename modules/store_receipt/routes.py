from flask import jsonify, request
import modules.store_receipt.services as service
from flask_restx import Namespace, Resource
from modules.store_receipt.models import CreateStoreReceipt, ApproveStoreReceipt

srv_ns = Namespace('srv', description='duqm global api')
srv_ns.models[CreateStoreReceipt.name] = CreateStoreReceipt
srv_ns.models[ApproveStoreReceipt.name] = ApproveStoreReceipt


@srv_ns.route('')
class StoreReceipt(Resource):
    @srv_ns.param(name='status')
    @srv_ns.param(name='srv_type')
    def get(self):
        """
        Parameters: from date , to date , status, srv_type
        if status true --> will return approved receipts only
        if status false --> will return not approved data
        if status null --> will return all data
        if srv_type --> mo for items from mo
        if srv_type --> internal for items as stock as found
        if srv_type --> null for all
        Returns
        -------

        """
        status = request.args.get('status')
        srv_type = request.args.get('srv_type')
        if srv_type and 0 == len(srv_type.strip()):
            srv_type = None
        result = service.get_srv_data(status, srv_type)
        return jsonify(result)

    @srv_ns.expect(CreateStoreReceipt, validate=False)
    #TODO hotfix validation disabled should be modified in future
    def post(self):
        """
        api to create srv
        Returns
        -------

        """
        print(
            f'this is gate in tdate time : {request.get_json().get('int_gate_in_date_time')}  {type(request.get_json().get('int_gate_in_date_time'))}')
        result = service.create_srv(request.get_json())
        return jsonify(result)


@srv_ns.route('/pending')
class StoreReceiptNotMade(Resource):
    # @srv_ns.param('path', default='', description='input path here ')
    def get(self):
        """
        this api is to get list of srv items which have gate in data but srv is not made
        Returns
        -------

        """
        result = service.srv_not_made_date()
        return jsonify({
            'result': result
        })


@srv_ns.route('/<int_store_receipt_no>')
class ApproveSRV(Resource):
    def get(self, int_store_receipt_no: str):
        """
        api to fetch store receipt data
        Parameters
        ----------
        int_store_receipt_no

        Returns
        -------

        """
        srv_obj = service.get_srv_obj(int_store_receipt_no)
        return jsonify(srv_obj)

    @srv_ns.expect(ApproveStoreReceipt)
    def put(self, int_store_receipt_no: str):
        """
        approve store receipt by store receipt number
        Parameters
        ----------
        int_store_receipt_no

        Returns
        -------

        """
        approved_by_user = request.get_json().get('username')
        service.approve_srv(int_store_receipt_no, approved_by_user)
        return {'status': 200}

    @srv_ns.param(name='username')
    def post(self, int_store_receipt_no: str):
        #TODO API to update srv
        """
        API to close srv

        Parameters
        ----------
        int_store_receipt_no

        Returns
        -------

        """
        username:str = request.args.get('username')
        service.close_srv(int_store_receipt_no,username)


