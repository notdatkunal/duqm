import pandas as pd
from fob_postgres.tables import fob_internal_consumption, FobGatePass, FobInternalGateIn, \
    fob_internal_stock
from fob_postgres.pg_session import postgres_session
from datetime import datetime
from sqlalchemy import update, and_, func, text
from helpers.commonn_utils import model_to_dict, format_date_postgres_timestamp
from helpers.exceptions import BadRequestException


def get_table_name(module: str):
    if module in ('consumption', "issue"):
        return "fob_internal_consumption"
    elif module == "gatein":
        return "fob_internal_gate_in"
    return 'fob_internal_consumption'


def fetch_bar_chart_service(module: str):
    query = text(f"""
        select 
	        TO_CHAR(month_series,'MON YY') as month,
	        coalesce(count(c.date_time_approved),0) as count
	            from
		            generate_series(
			            date_trunc('month',CURRENT_DATE)-INTERVAL'11 months' ,
			            date_trunc('month',CURRENT_DATE),
			            INTERVAL'1 month'
		        ) as month_series
	        left join {get_table_name(module)} as c  on date_trunc('month',date_time_approved) = month_series
	            and {" c.remarks is not null " if module == "issue" else True}
	            group by month_series
	            order by month_series
    """)
    result = postgres_session.get_session().execute(query).fetchall()
    result = [dict(row._mapping) for row in result]
    return result


def fetch_pending_status(customer_code):
    sess = postgres_session.get_session()
    gate_in_sub_query = sess.query(FobInternalGateIn.gate_pass_key).filter(
        FobInternalGateIn.date_time_approved.is_not(None)
    ).scalar_subquery()

    gate_in_count_query = sess.query(func.count()).filter(
        FobGatePass.gate_pass_key.not_in(gate_in_sub_query)
    ).scalar()

    store_receipt_query = text("""
        select count(*) from fob_internal_store_receipt where 
        int_gate_in_date_time  not in (select int_gate_in_date_time from fob_internal_gate_in
         where fob_internal_gate_in.date_time_approved is not null
         ) 
    """)
    store_receipt_count = sess.execute(store_receipt_query).one()

    internal_gate_pass_query = text("""
        select count(*) from fob_internal_gate_pass where int_gate_pass_no not in (
	    select int_gate_pass_no from fob_internal_consumption where fob_internal_consumption.date_time_approved is not null)
    """)

    internal_gate_pass_count = sess.execute(internal_gate_pass_query).one()
    internal_consumption_query = text("""
            select count(*) from fob_internal_consumption where approved_by is null and issue_to_customer_code = customer_code
    """)
    consumption_count = sess.execute(internal_consumption_query).one()

    issue_count = sess.query(fob_internal_consumption).filter(
        fob_internal_consumption.issue_to_customer_code != customer_code,
        fob_internal_consumption.remarks is not None,
        fob_internal_consumption.date_time_closed is None,
    ).count()

    return {
        'gatein_count': gate_in_count_query,
        'store_receipt_count': store_receipt_count._mapping.count,
        'internal_gate_pass_count': internal_gate_pass_count._mapping.count,
        'internal_consumption_count': consumption_count._mapping.count,
        'internal_issue_count': issue_count,
    }


def inventory_size_service():
    sess = postgres_session.get_session()
    query = sess.query(func.sum(fob_internal_stock.qty).label("total_stock"))
    result = pd.read_sql(query.statement, query.session.bind)
    return result.to_dict(orient='records')


def recent_activity_service(module: str | None):
    if module is None:
        module = "consumption"
    module = module.strip()
    sess = postgres_session.get_session()
    if module == "consumption":
        query = sess.query(
            func.trim(fob_internal_consumption.item_code).label("item_code"),
            fob_internal_consumption.qty,
            fob_internal_consumption.issue_to_customer_code,
            fob_internal_consumption.customer_code == fob_internal_consumption.issue_to_customer_code,
            fob_internal_consumption.remarks.is_(None)
        ).order_by(
            fob_internal_consumption.int_consumption_no.desc()
        ).limit(3)
    elif module == "gatein":
        query = sess.query(
            FobInternalGateIn.int_gate_in_date_time,
            FobInternalGateIn.no_of_packages,
            FobInternalGateIn.received_from
        ).order_by(
            FobInternalGateIn.int_gate_in_date_time.desc()
        ).limit(3)
    elif module == "issue":
        query = sess.query(
            func.trim(fob_internal_consumption.item_code).label("item_code"),
            fob_internal_consumption.qty,
            fob_internal_consumption.issue_to_customer_code,
            fob_internal_consumption.remarks.is_not(None)
        ).order_by(
            fob_internal_consumption.int_consumption_no.desc()
        ).limit(3)

    result = pd.read_sql(query.statement, query.session.bind)
    if module == "gatein":
        result['int_gate_in_date_time'] = result['int_gate_in_date_time'].apply(format_date_postgres_timestamp)
    return result.to_dict(orient="records")
