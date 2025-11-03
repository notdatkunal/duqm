import datetime
from typing import Type

import pandas as pd
from sqlalchemy import func, Integer, Row
from sqlalchemy.orm import query

from fob_postgres.pg_session import postgres_session
from fob_postgres.tables import fob_internal_gate_pass, fob_internal_consumption, fob_internal_stock
from modules.internal_gatepass.queries import get_pending_internal_gatepass_q, get_internal_gatepass_q, \
    get_cons_from_int_gp_q
from helpers.serials import create_internal_gatepass_serial, create_internal_gatepass_serial_f
from fob_postgres.exceptions import PostgresError


def get_pending_internal_gate_pass(customer_code):
    query = get_pending_internal_gatepass_q(customer_code)
    df_internal_gatepass_pending = pd.read_sql(query.statement, query.session.bind)

    df_internal_gatepass_pending = df_internal_gatepass_pending.fillna('').astype(str)

    return df_internal_gatepass_pending.to_dict(orient='records')


def get_internal_gate_pass():
    query = get_internal_gatepass_q()
    df_internal_gatepass = pd.read_sql(query.statement, query.session.bind)
    df_internal_gatepass = df_internal_gatepass.fillna('').astype(str)
    return df_internal_gatepass.to_dict(orient='records')


def save_gate_pass_entries(gate_pass_data, cons_list):
    with (postgres_session.get_session() as sess):
        int_gate_pass_obj = fob_internal_gate_pass(**gate_pass_data)

        running_serial_f = create_internal_gatepass_serial_f(station_code=int_gate_pass_obj.station_code,
                                                             customer_code=int_gate_pass_obj.customer_code)

        running_serial_c = (sess.query(fob_internal_gate_pass)
                            .filter(fob_internal_gate_pass.int_gate_pass_no.startswith(running_serial_f))
                            .count()
                            )

        int_gate_pass_obj.int_gate_pass_no = create_internal_gatepass_serial(
            station_code=int_gate_pass_obj.station_code
            , customer_code=int_gate_pass_obj.customer_code
            , running_serial_c=int(running_serial_c)
        )
        int_gate_pass_obj.int_gate_pass_key = datetime.datetime.now()
        # int_gate_pass_obj.transportation_mode = 'RD'
        sess.add(int_gate_pass_obj)
        sess.flush()
        for cons_item in cons_list:
            item_con: Type[fob_internal_consumption] = sess.query(fob_internal_consumption).filter(
                fob_internal_consumption.int_consumption_no == func.cast(cons_item, Integer)).one()
            item_con.int_gate_pass_no = int_gate_pass_obj.int_gate_pass_no
            sess.flush()
        sess.commit()
        return {
            'int_gatepass_no': int_gate_pass_obj.int_gate_pass_no
            , 'int_gatepass_key': int_gate_pass_obj.int_gate_pass_key
        }


def gate_pass_details(int_gate_pass_no):
    with postgres_session.get_session() as sess:
        item_int_gp: Type[fob_internal_gate_pass] = sess.query(fob_internal_gate_pass).filter(
            fob_internal_gate_pass.int_gate_pass_no == int_gate_pass_no).one()
        item_r = item_int_gp.__dict__
        item_r.pop('_sa_instance_state', None)
        int_cons_q = get_cons_from_int_gp_q(int_gate_pass_no, sess)
        df_internal_cons = pd.read_sql(int_cons_q.statement, int_cons_q.session.bind)
        df_internal_cons = df_internal_cons.fillna('').astype(str)
        item_r['internal_consumption'] = df_internal_cons.to_dict(orient='records')
        return item_r


def approve_int_gate_pass(int_gate_pass_list: list, approved_by: str):
    with postgres_session.get_session() as sess:
        for int_gate_pass_no in int_gate_pass_list:
            item_gp: Type[fob_internal_gate_pass] = sess.query(fob_internal_gate_pass).filter(
                fob_internal_gate_pass.int_gate_pass_no == int_gate_pass_no).one()
            item_gp.approved_by = approved_by.strip()
            item_gp.date_time_approved = datetime.datetime.now()
            sess.flush()
            int_cons_list: Row[Type[fob_internal_consumption]] = get_cons_from_int_gp_q(int_gate_pass_no, sess).all()
            for item_cons in int_cons_list:
                if isinstance(item_cons, fob_internal_consumption):

                    # if pending for approval is equal to the qty then more cons must not be allowed to made
                    # if total stock is 11 and the qty for internal gp is to be approved asx 10 then it must subtract from all the stock of that item code in fifo manner so that the old stock gets allocated from db
                    # fob_internal_stock qty > 0
                    # item_stock_list: list[Type[fob_internal_stock]] = sess.query(fob_internal_stock).filter(
                    #     fob_internal_stock.item_code == item_cons.item_code
                    # ).all()
                    cons_qty: float = float(item_cons.qty)
                    item_stock_list: query = sess.query(fob_internal_stock).filter(
                        fob_internal_stock.item_code == item_cons.item_code
                        , fob_internal_stock.qty > 0.0
                    ).order_by(fob_internal_stock.int_stock_serial)
                    print(f'this is count {item_stock_list.count()}')
                    check_total_stock = sess.query(func.sum(fob_internal_stock.qty)).filter(
                        fob_internal_stock.item_code == item_cons.item_code).first()[0]
                    # check if the qty in consumption is not greater than the total stock for that item
                    if cons_qty > check_total_stock:
                        raise PostgresError(code=500,
                                            message='consumption should not be greater than the total stock for that item')
                    for item_stock_ in item_stock_list.all():
                        if cons_qty == 0:
                            break
                        stock_qty: float = float(item_stock_.qty)
                        if cons_qty > stock_qty:
                            cons_qty -= stock_qty
                            item_stock_.qty = 0
                            sess.add(item_stock_)
                        else:
                            item_stock_.qty = float(item_stock_.qty) - cons_qty
                            sess.add(item_stock_)
                            break

                    sess.commit()
