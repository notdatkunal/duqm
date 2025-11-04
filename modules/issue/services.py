import pandas as pd
from fob_postgres.tables import fob_internal_demand, fob_internal_demand_line, \
    fob_internal_stock, fob_internal_consumption, fob_item
from fob_postgres.pg_session import postgres_session
from datetime import datetime
from sqlalchemy import update, and_, func, text, Integer
from helpers.commonn_utils import model_to_dict, format_date_postgres_timestamp
from helpers.exceptions import BadRequestException


def pending_issue_service(customer_code: int, raised_for_customer: int):
    sess = postgres_session.get_session()

    query = (
        sess.query(
            func.trim(fob_internal_demand_line.item_code).label('item_code'),
            fob_internal_demand_line.qty,
            fob_internal_demand_line.id_line_no,
            fob_internal_demand.internal_demand_no,
            fob_internal_demand.authority_type,
            fob_internal_demand.raised_for_customer,
            fob_internal_demand.station_code,
            func.trim(fob_item.item_desc).label("item_desc"),
            fob_internal_demand.date_time_authorised,
        ).join(
            fob_internal_demand, fob_internal_demand.internal_demand_no == fob_internal_demand_line.internal_demand_no
        ).join(
            fob_item, func.trim(fob_item.item_code) == func.trim(fob_internal_demand_line.item_code)
        ).join(
            fob_internal_consumption,
            fob_internal_consumption.int_consumption_no == fob_internal_demand_line.int_consumption_no,
            isouter=True
        ).filter(
            fob_internal_demand.raised_for_customer != customer_code,
            fob_internal_demand.raised_for_customer == raised_for_customer if raised_for_customer is not None else True,
            fob_internal_demand.authorised_by.is_not(None),
            fob_internal_demand_line.closing_code.is_(None),
            fob_internal_demand_line.int_consumption_no.is_(None),
            # fob_internal_demand_line.internal_demand_no != func.split_part(fob_internal_consumption.remarks, " ", 1),
            # fob_internal_demand_line.id_line_no != func.cast(func.split_part(fob_internal_consumption.remarks, " ", 2),
            #                                                  Integer),
        )
    )

    result = pd.read_sql(query.statement, query.session.bind)
    result['date_time_authorised'] = result['date_time_authorised'].apply(format_date_postgres_timestamp)
    stock_sum_query = (
        sess.query(
            func.trim(fob_internal_stock.item_code).label('item_code'),
            func.sum(fob_internal_stock.qty).label("balance"),
            fob_internal_stock.sh_no
        ).filter(
            fob_internal_stock.item_code.in_(list(result["item_code"]))
        ).group_by(
            func.trim(fob_internal_stock.item_code),
            fob_internal_stock.sh_no,
        )
    )

    pending_qty_query = (postgres_session.get_session().query(
        func.coalesce(func.sum(fob_internal_consumption.qty), 0).label('pending_for_approval_qty'),
        func.trim(fob_internal_consumption.item_code).label('item_code').label('item_code')
    ).filter(
        fob_internal_consumption.int_gate_pass_no.is_(None),
        fob_internal_consumption.item_code.in_(list(result["item_code"])),
        fob_internal_consumption.date_time_closed.is_(None),
    ).group_by(func.trim(fob_internal_consumption.item_code)))

    pending_qty_result = pd.read_sql(pending_qty_query.statement, pending_qty_query.session.bind)
    stock_result = pd.read_sql(stock_sum_query.statement, stock_sum_query.session.bind)
    merged = pd.merge(stock_result, pending_qty_result, on="item_code", how="left")
    merged["pending_for_approval_qty"] = merged["pending_for_approval_qty"].fillna(0)

    merged = pd.merge(result, merged, on='item_code', how='inner')
    merged = merged.to_dict(orient='records')
    return merged


def save_issue_service(body):
    sess = postgres_session.get_session()
    for obj in body:
        obj["date_time_issued"] = datetime.now()
        obj["consumption_type"] = "S"
        max_no = (
            sess.query(
                func.max(fob_internal_consumption.int_consumption_no)
            ).one()
        )[0]
        if max_no is None:
            max_no = 0
        obj["int_consumption_no"] = max_no + 1
        id_line_no = obj.pop("id_line_no")
        internal_demand_no = obj.pop("internal_demand_no")
        consumption = fob_internal_consumption(**obj)
        consumption.remarks = f"{internal_demand_no} {id_line_no}"
        sess.add(consumption)
        sess.flush()
        sess.flush()
    sess.commit()
    return body


def issue_list_service():
    sess = postgres_session.get_session()

    sub_query = (
        sess.query(text("select 1")).filter(
            fob_internal_demand_line.int_consumption_no.is_not(None),
        )
    )

    # query = (
    #     sess.
    # )
    pass
