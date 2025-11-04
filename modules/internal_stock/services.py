import datetime
import os
import pandas as pd
from pydantic import dataclasses
import numpy as np
from fob_postgres.tables import fob_internal_stock, fob_item, fob_internal_item_details, FobInternalGateIn, \
    fob_internal_store_receipt, fob_item, fob_internal_item_details
from fob_postgres.pg_session import postgres_session
from sqlalchemy import func, text, text
from helpers import exceptions

from helpers.exceptions import BadRequestException, AppException
from modules.store_receipt.services import create_srv_object, approve_srv

REQUIRED_COLUMNS = {'item_code',
                    'stock_qty',
                    'allowance_qty',
                    'hsn_code'}


@dataclasses.dataclass
class StockItem:
    item_code: str
    stock_qty: float
    allowance_qty: float
    hsn_code: str

    def __post_init__(self):
        """validation for the data imported"""
        ...


def internal_stock_list(item_code: str | None, page: int, rows: int):
    if item_code is not None and "=" in item_code:
        raise exceptions.BadRequestException("invalid item_code")
    base_query = postgres_session.get_session().query(
        fob_internal_stock,
        func.trim(fob_item.item_desc).label("item_desc")
    ).join(
        fob_item, func.trim(fob_item.item_code) == func.trim(fob_internal_stock.item_code)
    )
    if item_code is not None:
        base_query.filter(
            fob_internal_stock.item_code.ilike(f"%{item_code}%"),
        )

    count_result = base_query.count()
    query = base_query.offset(page * rows).limit(rows)
    result = pd.read_sql(query.statement, query.session.bind)
    result["miqp_qty"] = result["miqp_qty"].fillna(0)
    result = result.to_dict(orient="records")
    return {
        'count': count_result,
        'internal_stock_list': result
    }


def import_stock(temp_path, customer_code, login_id, role, station_code, sh_no):
    with postgres_session.get_session() as sess:
        # with sess.begin():
        try:
            df = pd.read_csv(temp_path)
            df = df.dropna(subset=['item_code'])
            missing_cols = REQUIRED_COLUMNS - set(df.columns)
            if missing_cols:
                raise BadRequestException(f'missing required columns {missing_cols} ')
            # there should be a check when an item code which does not have item line entry is attempted for insertion
            # in that case that is considered as Non MO item, and it must be shown
            # item_code , stock_qty , authorised_qty , hsn_code
            # manual srv + allowance
            print(f'this is df {df}')
            if df['item_code'].isnull().any():
                raise AppException(error_code=500, message='item_code column contains null values')
            if df['item_code'].duplicated().any():
                raise AppException(error_code=500, message='duplicate item codes found in csv')
            if df['stock_qty'].notnull().any():
                # TODO create gatein and srv object since there's stock data present in csv
                # There will be fix value for package type and no of packages
                # fob_internal_gate_in_obj = FobInternalGateIn(
                #     customer_code=customer_code,
                #     gate_in_type='M',
                #     no_of_packages=1,
                #     package_type='NA',
                #     received_from='CWH(MB)',
                #     approved_by=login_id,
                #     station_code=station_code)
                # sess.add(fob_internal_gate_in_obj)
                # sess.flush([fob_internal_gate_in_obj])
                ...
            df['stock_qty'] = df['stock_qty'].fillna(0)
            df['allowance_qty'] = df['allowance_qty'].fillna(0)
            df['hsn_code'] = df['hsn_code'].fillna('')
            for row in df.to_dict(orient="records"):
                ob = StockItem(**row)
                item_check_allowance = 0 != sess.query(fob_internal_item_details).filter(
                    fob_internal_item_details.item_code == ob.item_code).count()

                if int(ob.stock_qty) != 0:
                    """
                        create stock entry
                        """
                    # TODO gate in --> srv --> stock stock
                    data_srv = {
                        'prepared_by': login_id
                        , 'int_store_receipt_choice': 'A'
                        , 'station_code': station_code
                        , 'item_code': ob.item_code
                        , 'sh_no': sh_no
                        , 'date_time_received': datetime.datetime.now()
                        # , 'int_gate_in_date_time': str(fob_internal_gate_in_obj.int_gate_in_date_time)
                        , 'qty_on_charge': ob.stock_qty
                        , 'qty_received': ob.stock_qty
                        , 'customer_code': customer_code
                        , 'pack_type': 'NA'
                        , 'condition_code': 'Emp'
                        , 'location_marking': 'AUTO'
                    }
                    item_srv = create_srv_object(data_srv, sess)
                    approve_srv(item_srv.int_store_receipt_no, login_id)
                    ...

                if item_check_allowance:
                    obj_int_all = get_item_details(ob, sess)
                else:
                    obj_int_all = fob_internal_item_details()
                    ...
                if int(ob.allowance_qty) != 0:
                    """
                        update the allowance if exists else create new entry
                        """
                    obj_int_all.allowance_qty = ob.allowance_qty

                if len(ob.hsn_code) != 0:
                    """
                        update if exists or create new entry
                        """
                    obj_int_all.hsn_code = ob.hsn_code

                print('this is loop')
                print(ob)
                if obj_int_all.hsn_code or obj_int_all.allowance_qty:
                    obj_int_all.item_code = ob.item_code
                    sess.add(obj_int_all)
                    sess.flush()
        finally:
            # sess.commit()
            if os.path.exists(temp_path):
                os.remove(temp_path)


def get_item_details(ob, sess):
    return sess.query(fob_internal_item_details).filter(
        fob_internal_item_details.item_code == ob.item_code).one()


def deficiency_service(interval: str, item_code: str) -> list[dict]:
    sess = postgres_session.get_session()
    interval_query = interval_filter(interval)

    query = sess.query(
        func.trim(fob_internal_stock.item_code).label("item_code"),
        func.trim(fob_item.item_desc).label("item_desc"),
        func.sum(fob_internal_stock.qty).label("total_qty"),
        fob_internal_stock.sh_no,
        fob_internal_stock.condition_code,
        func.coalesce(fob_internal_item_details.allowance_qty, 0).label("allowance_qty"),
    ).join(
        fob_item, func.trim(fob_item.item_code) == func.trim(fob_internal_stock.item_code)
    ).join(
        fob_internal_item_details,
        func.trim(fob_internal_stock.item_code) == func.trim(fob_internal_item_details.item_code),
        isouter=True
    ).filter(
        fob_internal_stock.item_code.ilike(f"%{item_code.strip()}%") if item_code is not None and len(
            item_code.strip()) > 0 else True
    ).group_by(
        func.trim(fob_internal_stock.item_code),
        func.trim(fob_item.item_desc),
        fob_internal_stock.sh_no,
        fob_internal_stock.condition_code,
        fob_internal_item_details.allowance_qty
    ).having(
        interval_query
    )

    result = pd.read_sql(query.statement, query.session.bind)

    result = result.to_dict(orient="records")
    return result


def interval_filter(interval: str | None):
    if interval is None or interval not in ["0-25", "25-50", "50-75", "75-100"]:
        return True

    [from_no, to_no] = interval.split("-")

    return func.sum(fob_internal_stock.qty).between(
        (int(from_no) / 100) * func.coalesce(fob_internal_item_details.allowance_qty, 0),
        (int(to_no) / 100) * func.coalesce(fob_internal_item_details.allowance_qty, 0)
    )
