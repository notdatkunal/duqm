from sqlalchemy import and_, cast, SMALLINT,func

from fob_postgres.tables import FobInternalGateIn, FobStockDelivery, fob_internal_demand_line, FobGatePass, \
    fob_internal_store_receipt, FobItem, fob_internal_consumption, fob_internal_stock
from fob_postgres.pg_session import postgres_session
from sqlalchemy.orm import Query, aliased


def srv_data_query(status: str | None, srv_type: str | None) -> Query:
    # cons_alias = aliased(fob_internal_consumption)
    # cons_q = (postgres_session.get_session()
    #           .query(func.count())
    #           .join(fob_internal_stock,and_(fob_internal_stock.customer_code==cons_alias.))
    #           .scalar_subquery()
    #           )
    query: Query = postgres_session.get_session().query(fob_internal_store_receipt)
    if status:
        query = query.filter(fob_internal_store_receipt.approved_by.is_not(None) if status.strip() == 'true' else fob_internal_store_receipt.approved_by.is_(None))
    if srv_type:
        query = query.filter(fob_internal_store_receipt.internal_demand_no.is_not(None) if srv_type.strip() == 'mo' else fob_internal_store_receipt.internal_demand_no.is_(None))
    return query


def srv_not_made_query() -> Query:
    sub_query = (postgres_session.get_session()
                 .query(fob_internal_store_receipt)
                #  .join(FobStockDelivery,FobStockDelivery.item_code == fob_internal_store_receipt.item_code)
                 .filter(fob_internal_store_receipt.int_gate_in_date_time == FobInternalGateIn.int_gate_in_date_time,
                    func.trim(FobStockDelivery.item_code) == func.trim(fob_internal_store_receipt.item_code)
                 )
                 )
                #  and trim(fob_stock_delivery.item_code) = trim(fob_internal_store_receipt.item_code)
    query: Query = (postgres_session.get_session().query(FobInternalGateIn.gate_pass_key
                                                         , FobGatePass.gate_pass_no
                                                        #  , fob_internal_demand_line.mo_demand_no
                                                         ,FobStockDelivery.demand_no.label("mo_demand_no")
                                                         , FobInternalGateIn.package_type
                                                         , FobInternalGateIn.int_gate_in_date_time
                                                         , FobStockDelivery.qty_carried
                                                         , FobStockDelivery.item_code
                                                         , FobStockDelivery.issue_date_time
                                                         , fob_internal_demand_line.id_line_no
                                                         , fob_internal_demand_line.reason
                                                         , fob_internal_demand_line.internal_demand_no
                                                         )
                    .select_from(FobInternalGateIn)
                    .join(FobStockDelivery, FobInternalGateIn.gate_pass_key == FobStockDelivery.gate_pass_key)
                    .join(FobGatePass, FobGatePass.gate_pass_key == FobStockDelivery.gate_pass_key)
                    # .join(FobItem, FobItem.item_code == FobStockDelivery.item_code)
                    .join(fob_internal_demand_line, and_(
                          fob_internal_demand_line.internal_demand_no == FobStockDelivery.internal_demand_no,
                          cast(fob_internal_demand_line.id_line_no, SMALLINT) == cast(FobStockDelivery.id_line_no, SMALLINT)),isouter=True)
                    .filter(~sub_query.exists())
                    )
    query = query.filter(FobInternalGateIn.approved_by.is_not(None))
    query = query.order_by(FobInternalGateIn.int_gate_in_date_time)

    return query
