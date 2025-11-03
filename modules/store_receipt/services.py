from datetime import datetime
from typing import Type

import numpy as np
from sqlalchemy import text, func, Numeric, and_
import modules.store_receipt.queries as repo
import pandas as pd
from dateutil import parser
from fob_postgres.tables import fob_internal_store_receipt, fob_internal_stock, fob_internal_consumption
from fob_postgres.pg_session import postgres_session
from helpers.commonn_utils import format_date_postgres_timestamp, get_n_digit_number
from helpers.exceptions import BadRequestException


def srv_not_made_date():
    from helpers.commonn_utils import format_date_postgres_timestamp
    query = repo.srv_not_made_query()
    df_result: pd.DataFrame = pd.read_sql(query.statement, query.session.bind)
    df_result['issue_date_time'] = df_result['issue_date_time'].apply(format_date_postgres_timestamp)
    # df_result['int_gate_in_date_time'] = df_result['int_gate_in_date_time'].apply(format_date_postgres_timestamp)
    df_result['int_gate_in_date_time'] = df_result['int_gate_in_date_time'].apply(format_date_postgres_timestamp)
    df_result['gate_pass_key'] = df_result['gate_pass_key'].apply(format_date_postgres_timestamp)
    return df_result.to_dict(orient='records')


def create_srv(data: dict):
    with postgres_session.get_session() as sess:
        if data['reason'] is None:
            data['reason'] = ''
        item_stock = create_srv_object(data, sess)
        return {'status': 'success', 'srv_no': item_stock.int_store_receipt_no}


def create_srv_object(data, sess):
    item_srv = fob_internal_store_receipt(**data)
    item_srv.int_store_receipt_no = get_store_receipt_no(item_srv, sess)
    item_srv.item_code = str(item_srv.item_code).strip()
    if item_srv.int_gate_in_date_time:
        item_srv.int_gate_in_date_time = parser.parse(item_srv.int_gate_in_date_time)
        item_srv.int_gate_in_date_time = format_date_postgres_timestamp(item_srv.int_gate_in_date_time)
    sess.add(item_srv)
    int_store_receipt_no = item_srv.int_store_receipt_no
    sess.commit()
    # sess.refresh(item_srv)
    return item_srv


def get_store_receipt_no(item, sess) -> str:
    serial = f'{str(datetime.now().year)[2:]}{item.station_code[0]}{item.customer_code.strip()[:4]}{item.sh_no}S'
    query = sess.query(fob_internal_store_receipt.int_store_receipt_no).filter(
        fob_internal_store_receipt.int_store_receipt_no.startswith(serial)).all()
    list_of_serials = list(int(item.int_store_receipt_no[-5:]) for item in query)
    max_number: str = str((max(list_of_serials) if len(list_of_serials) > 0 else 0) + 1)
    return f'{serial}{get_n_digit_number(number=max_number, constant=6)}'


def get_srv_data(status: str | None, srv_type: str | None):
    query = repo.srv_data_query(status, srv_type)
    df_result: pd.DataFrame = pd.read_sql(query.statement, query.session.bind)
    # df_result = df_result.fillna('').astype(str)
    df_result = df_result.replace({pd.NaT: None, np.nan: None})
    return df_result.to_dict(orient='records')


def approve_srv(int_store_receipt_no: str, approved_by_user: str):
    with postgres_session.get_session() as sess:
        srv_obj: Type[fob_internal_store_receipt] = sess.query(fob_internal_store_receipt).filter(
            fob_internal_store_receipt.int_store_receipt_no == int_store_receipt_no.strip()).one()
        srv_obj.approved_by = approved_by_user.strip()
        srv_obj.date_time_approved = datetime.now()
        sess.add(srv_obj)
        sess.flush()
        create_stock_entry(sess, srv_obj)


def create_stock_entry(sess, srv_obj):
    """
    srv must be approved with approved by _column filled and date time approved filled
    Parameters
    ----------
    sess
    srv_obj

    Returns
    -------

    """
    stock_obj: fob_internal_stock = fob_internal_stock()
    # stock_obj.
    stock_obj.item_code = srv_obj.item_code
    stock_obj.nonmo_item_code = srv_obj.nonmo_item_code
    result = sess.execute(text(f'''
                    SELECT COALESCE(MAX(int_stock_serial),0) FROM public.fob_internal_stock WHERE customer_code = \'{srv_obj.customer_code}\' AND item_code = \'{srv_obj.item_code}\' AND station_code = \'{srv_obj.station_code}\' ''')
                          )
    max_serial = result.fetchone()[0]
    int_stock_serial = max_serial + 1  # issued_int_stock_serial
    stock_obj.int_stock_serial = int_stock_serial
    stock_obj.sh_no = srv_obj.sh_no
    stock_obj.condition_code = srv_obj.condition_code
    stock_obj.miqp_qty = func.cast(srv_obj.miqp_qty, Numeric)
    stock_obj.location_marking = str(srv_obj.location_marking).strip()
    stock_obj.qty = func.cast(srv_obj.qty_on_charge, Numeric)
    stock_obj.int_store_receipt_no = srv_obj.int_store_receipt_no
    stock_obj.customer_code = srv_obj.customer_code
    stock_obj.station_code = srv_obj.station_code
    stock_obj.remarks = srv_obj.remarks
    sess.add(stock_obj)
    sess.commit()


def get_srv_obj(int_store_receipt_no: str):
    with postgres_session.get_session() as sess:
        srv_obj: Type[fob_internal_store_receipt] = sess.query(fob_internal_store_receipt).filter(
            fob_internal_store_receipt.int_store_receipt_no == int_store_receipt_no.strip()).one()

        srv_obj_dict = srv_obj.__dict__.copy()
        srv_obj_dict.pop('_sa_instance_state', None)
        return srv_obj_dict


def close_srv(int_store_receipt_no, username: str):
    # TODO: check if cons should not exist
    # TODO: check if cons exists then it must be closed
    if not check_cons_exists(int_store_receipt_no):
        raise BadRequestException(message='tried to close srv with consumption')
    with postgres_session.get_session() as sess, sess.begin():
        srv_obj: Type[fob_internal_store_receipt] = sess.query(fob_internal_store_receipt).filter(
            fob_internal_store_receipt.int_store_receipt_no == int_store_receipt_no.strip()).one()
        srv_obj.closed_by = username
        srv_obj.date_time_closed = datetime.now()
        sess.add(srv_obj)
        sess.flush()
        stock_obj: Type[fob_internal_stock] = sess.query(fob_internal_stock).filter(fob_internal_stock.int_store_receipt_no == int_store_receipt_no).one()
        stock_obj.qty = 0
        sess.add(stock_obj)
        sess.flush()
        sess.commit()


def check_cons_exists(int_store_receipt_no: str) -> bool:
    """
    returns true if approved consumption is present
    returns false if consumption not approved

    """
    with postgres_session.get_session() as sess:
        flag_cons: bool = (0 < sess.query(fob_internal_consumption)
                           .join(fob_internal_stock, and_(
            fob_internal_stock.customer_code == fob_internal_consumption.customer_code
            , fob_internal_stock.int_stock_serial == fob_internal_consumption.int_stock_serial
            , fob_internal_stock.item_code == fob_internal_consumption.item_code
            , fob_internal_stock.int_store_receipt_no == int_store_receipt_no))
                           # .filter(fob_internal_consumption.approved_by.is_not(None))
                           .count())
        return flag_cons
