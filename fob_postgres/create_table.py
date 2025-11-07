from sqlalchemy import create_engine
from fob_postgres.pg_admin import init_or_get_pgserver


def create_all_tables():
    # Import all your table model classes
    from fob_postgres.tables import (
        fob_demand_status,
        fob_internal_gate_pass,
        fob_internal_consumption,
        fob_internal_stock,
        fob_internal_item_details,
        fob_internal_store_receipt,
        fob_stock_release,
        fob_internal_demand,
        fob_internal_demand_line,
        FobUsers,
        fob_item,
        FobGatePass,
        FobStockDelivery,
        FobInternalGateIn,
        FobUserRole,
        FobInternalCustomerUser,
        fob_code_table,
        fob_customer,
        fob_item_line
    )
    # List of all your SQLAlchemy model classes
    all_table_models = [
        fob_demand_status,
        fob_internal_gate_pass,
        fob_internal_consumption,
        fob_internal_stock,
        fob_internal_item_details,
        fob_internal_store_receipt,
        fob_stock_release,
        fob_internal_demand,
        fob_internal_demand_line,
        FobUsers,
        fob_item,
        FobGatePass,
        FobStockDelivery,
        FobInternalGateIn,
        FobUserRole,
        FobInternalCustomerUser,
        fob_code_table,
        fob_customer,
        fob_item_line
    ]
    engine = create_engine(init_or_get_pgserver())
    for TableModel in all_table_models:
        print(f"Attempting to create table: {TableModel.__tablename__}")
        TableModel.__table__.create(bind=engine, checkfirst=True)
        print(f"Table {TableModel.__tablename__} checked/created.")
    print("All tables checked/created successfully.")


