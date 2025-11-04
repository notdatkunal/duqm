from fob_postgres.pg_session import postgres_session
from fob_postgres.tables import fob_internal_consumption, fob_item
from sqlalchemy import func


def get_consumption_data_q(status: str, closed: str, self_customer_code: str, self_consumptions):
    self_consumptions = 'true' == self_consumptions

    query = postgres_session.get_session().query(
        fob_internal_consumption,
        fob_item.item_desc,
    ).join(
        fob_item, func.trim(fob_item.item_code) == func.trim(fob_internal_consumption.item_code)
    )
    if status:
        query = query.filter(fob_internal_consumption.approved_by.is_not(
            None) if status.strip() == 'true' else fob_internal_consumption.approved_by.is_(None))

    if closed is not None:
        query = query.filter(fob_internal_consumption.date_time_closed.is_not(
            None) if closed.strip() == 'true' else fob_internal_consumption.date_time_closed.is_(None))
    if self_customer_code is not None and self_consumptions:
        query = query.filter(
            func.trim(fob_internal_consumption.issue_to_customer_code) == self_customer_code.strip()
        )
    else:
        query = query.filter(
            func.trim(fob_internal_consumption.issue_to_customer_code) != self_customer_code.strip()
        )

    return query
