import datetime
from typing import Type

from sqlalchemy import func, and_, Integer, text
from sqlalchemy.orm import aliased
from fob_postgres.pg_session import postgres_session
from fob_postgres.tables import fob_internal_stock, FobItem, fob_internal_store_receipt, fob_internal_consumption \
    , fob_internal_demand, fob_internal_demand_line
import pandas as pd
from helpers import exceptions
from modules.consumption.queries import get_consumption_data_q


def stock_list_service(item_code: str | None):
    item_code = item_code.strip() if item_code is not None else None
    sub_query = (postgres_session.get_session().query(
        func.sum(fob_internal_consumption.qty).label('pending_for_approval_qty'),
        func.trim(fob_internal_consumption.item_code).label('item_code')
    ).filter(
        fob_internal_consumption.int_gate_pass_no.is_(None),
        fob_internal_consumption.item_code.ilike(f"%{item_code}%") if item_code is not None and len(
            item_code) > 0 else True,
        fob_internal_consumption.date_time_closed.is_(None),
    ).group_by(func.trim(fob_internal_consumption.item_code)))

    query = (postgres_session.get_session().query(
        # *[c for c in fob_internal_stock.__table__.columns if c.name not in ['int_stock_serial', 'int_store_receipt_no']],
        func.sum(fob_internal_stock.qty).label('qty')
        , fob_internal_stock.sh_no
        # , fob_internal_stock.miqp_qty
        , FobItem.item_code
        , func.trim(FobItem.item_desc).label('item_desc'),
        FobItem.crp_category,
        FobItem.item_deno
        # fob_internal_store_receipt.mo_demand_no
    ).join(
        FobItem, func.TRIM(FobItem.item_code) == func.TRIM(fob_internal_stock.item_code)
    ).join(
        fob_internal_store_receipt,
        fob_internal_store_receipt.int_store_receipt_no == fob_internal_stock.int_store_receipt_no
    ).filter(
        func.round(fob_internal_stock.qty) > 0.000,
        # fob_internal_store_receipt.condition_code.in_(['New', 'Rpd', 'Usd']),
        fob_internal_stock.item_code.ilike(f"%{item_code}%") if item_code is not None and len(item_code) > 0 else True,
    )
    .group_by(
        FobItem.item_code
        , func.trim(FobItem.item_desc),
        FobItem.crp_category,
        FobItem.item_deno,
        fob_internal_stock.sh_no
        # , fob_internal_stock.miqp_qty

    )
    )

    df_result: pd.DataFrame = pd.read_sql(query.statement, query.session.bind)
    sub_query_result = pd.read_sql(sub_query.statement, sub_query.session.bind)
    merged_df = df_result.merge(sub_query_result[["pending_for_approval_qty", "item_code"]], on="item_code", how="left")
    merged_df["pending_for_approval_qty"] = merged_df["pending_for_approval_qty"].fillna(0)
    res = merged_df.to_dict(orient='records')
    return res


def save_multiple_consumptions(required_list: list[dict]):
    # int _consumption no to be generated in runtime
    with postgres_session.get_session() as sess:
        for consumption_dict in required_list:
            cons_obj: fob_internal_consumption = fob_internal_consumption(**consumption_dict)
            cons_obj.date_time_issued = datetime.datetime.now()
            # TODO find oldest from db
            data = sess.query(fob_internal_stock.int_stock_serial).filter(fob_internal_stock.qty > 0,
                                                                          fob_internal_stock.item_code == cons_obj.item_code).first()
            cons_obj.int_stock_serial = data.int_stock_serial
            max_num = sess.query(func.max(fob_internal_consumption.int_consumption_no)).scalar()
            if max_num is None:
                max_num = 0
            cons_obj.int_consumption_no = max_num + 1
            sess.add(cons_obj)
            print(f'logging: {cons_obj.int_consumption_no}')
            sess.commit()


def get_data_consumption(status: str, closed: str, self_customer_code: str, self_consumptions):
    query = get_consumption_data_q(status, closed, self_customer_code, self_consumptions)
    df_consumption = pd.read_sql(query.statement, query.session.bind)

    df_consumption = df_consumption.fillna('').astype(str)

    return df_consumption.to_dict(orient='records')


def approve_consumptions(consumption_list: list, login_id: str):
    is_full_dict = {}
    with postgres_session.get_session() as sess:
        for con_id in consumption_list:
            item_con: Type[fob_internal_consumption] = sess.query(fob_internal_consumption).filter(
                fob_internal_consumption.int_consumption_no == func.cast(con_id, Integer)).one()
            item_con.approved_by = login_id
            item_con.date_time_approved = datetime.datetime.now()

            if item_con.remarks is None:
                sess.add(item_con)
                sess.flush()
                continue
            [internal_demand_no, id_line_no] = str(item_con.remarks).split()

            line_data: Type[fob_internal_demand_line] = (
                sess.query(fob_internal_demand_line)
                .filter(
                    fob_internal_demand_line.internal_demand_no == internal_demand_no,
                    fob_internal_demand_line.id_line_no == int(id_line_no),
                )
            ).one()
            if line_data is None:
                sess.add(item_con)
                sess.flush()
                continue
            print(f"line_data\n", line_data)
            line_data.int_consumption_no = int(con_id)
            if line_data.qty > item_con.qty:
                line_data.closing_code = "P"
                has = is_full_dict.get(internal_demand_no)
                if has is None:
                    is_full_dict[internal_demand_no] = True
            else:
                line_data.closing_code = "F"
                is_full_dict[internal_demand_no] = False

            line_data.date_time_closed = datetime.datetime.now()

            sess.add(item_con)
            sess.flush()

            sess.add(line_data)
            sess.flush()

        # for int_demand_no,is_full in is_full_dict.items():
        #     update_query = (
        #         sess.query(fob_internal_demand).filter(
        #             fob_internal_demand.internal_demand_no == int_demand_no
        #         ).update({
        #             "closing_code": "F" if is_full else "P",
        #             "date_time_closed": datetime.datetime.now()
        #         })
        #     )

        sess.commit()


def close_consumption_service(int_consumption_no_list, login_id: str):
    with postgres_session.get_session() as sess:
        for int_consumption_no in int_consumption_no_list:
            try:
                consumption: fob_internal_consumption = sess.query(fob_internal_consumption).filter(
                    fob_internal_consumption.int_consumption_no == int_consumption_no
                ).one()
                consumption.date_time_closed = datetime.datetime.now()
                consumption.closed_by = login_id
                sess.add(consumption)
                sess.commit()
            except Exception as ex:
                raise exceptions.AppException(ex.args)
    return True


def get_consumption_by_gate_pass_no(gate_pass_no):
    sess = postgres_session.get_session()
    query = sess.query(
        fob_internal_consumption,
        func.trim(FobItem.item_desc).label("item_desc")
    ).join(
        FobItem, func.trim(FobItem.item_code) == func.trim(fob_internal_consumption.item_code)
    ).filter(
        fob_internal_consumption.int_gate_pass_no == gate_pass_no
    )
    result = pd.read_sql(query.statement, query.session.bind)
    return result.to_dict(orient='records')
