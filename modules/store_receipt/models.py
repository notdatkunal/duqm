from flask_restx import Model, fields


class NullableInteger(fields.Integer):
    def format(self, value):
        if value is None:
            return None
        return super().format(value)


ApproveStoreReceipt = Model('UpdateSRV', {
    'username': fields.String(required=True)
})

CreateStoreReceipt = Model('StoreReceipt', {
    'miqp_qty': fields.Integer(required=True, default=1),
    'qty_received': fields.Integer(required=True),
    'qty_on_charge': fields.Integer(required=True),
    'id_line_no': NullableInteger(required=False),
    'issued_int_stock_serial': fields.Integer(required=False),
    'date_time_received': fields.DateTime(required=False),
    'date_manufactured': fields.DateTime(required=False),
    'int_gate_in_date_time': fields.DateTime(required=False),
    'issue_date_time': fields.DateTime(required=False),
    'date_expiry': fields.DateTime(required=False),
    'customer_code': fields.String(required=True),
    'int_store_receipt_choice': fields.String(required=True),
    'internal_demand_no': fields.String(required=False),
    'item_code': fields.String(required=True),
    'sh_no': fields.String(required=True),
    'location_marking': fields.String(required=True),
    'pack_type': fields.String(required=True),
    'station_code': fields.String(required=True),
    'refit_customer_code': fields.String(required=False),
    'return_id': fields.String(required=False),
    'mo_demand_no': fields.String(required=True),
    'condition_code': fields.String(required=True),
    'gate_pass_no': fields.String(required=True),
    'remarks': fields.String(required=False),
    'reason': fields.String(required=False),
})
