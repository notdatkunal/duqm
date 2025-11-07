from datetime import datetime
from sqlalchemy import Column, CHAR, DATETIME, VARCHAR, TIMESTAMP, FLOAT, Integer, REAL, SMALLINT, Numeric, func
from sqlalchemy.orm import validates
from sqlalchemy.event import listens_for
from fob_postgres.exceptions import PostgresError
from fob_postgres.pg_session import postgres_session


class fob_demand_status(postgres_session.App_Base):
    __tablename__ = 'fob_demand_status'
    internal_demand_no = Column(CHAR(16), nullable=True)
    id_line_no = Column(SMALLINT, nullable=True)
    demand_no = Column(CHAR(7), primary_key=True)
    customer_code = Column(CHAR(4), primary_key=True)
    demanded_qty = Column(REAL, nullable=True)
    total_issued_qty = Column(REAL, nullable=True)
    latest_issue_date_time = Column(TIMESTAMP, nullable=True)
    total_released_qty = Column(REAL, nullable=True)
    latest_released_time = Column(TIMESTAMP, nullable=True)
    latest_date_time_taken_over = Column(TIMESTAMP, nullable=True)
    latest_package_date_time_approved = Column(TIMESTAMP, nullable=True)
    latest_package_date_time_taken_over = Column(TIMESTAMP, nullable=True)
    latest_gate_pass_key = Column(TIMESTAMP, nullable=True)
    status_flag = Column(CHAR(2), nullable=True)

    @validates('id_line_no')
    def validate_id_line_no(self, key, value) -> int:
        if isinstance(value, str) or isinstance(value, float):
            return int(value)
        return value

    @validates('customer_code')
    def validate_customer_code(self, key, value) -> str:
        return str(value)


class fob_internal_gate_pass(postgres_session.App_Base):
    __tablename__ = 'fob_internal_gate_pass'
    int_gate_pass_no = Column(VARCHAR(14), primary_key=True)
    int_gate_pass_key = Column(TIMESTAMP, nullable=False)
    authority_ref = Column(VARCHAR(20))
    transportation_mode = Column(VARCHAR(3))
    transport_no = Column(VARCHAR(15))
    destination = Column(VARCHAR(30))
    escort_name = Column(VARCHAR(30))
    remarks = Column(VARCHAR(120))
    initiated_by = Column(VARCHAR(8), nullable=False)
    date_time_approved = Column(TIMESTAMP)
    approved_by = Column(VARCHAR(8))
    station_code = Column(VARCHAR(1), nullable=False)
    customer_code = Column(VARCHAR(4), nullable=False)
    dept_code = Column(VARCHAR(4))
    sub_dept_code = Column(VARCHAR(4))
    # raised_for_customer = Column(VARCHAR(4), nullable=False)


class fob_internal_consumption(postgres_session.App_Base):
    __tablename__ = 'fob_internal_consumption'
    int_consumption_no = Column(Integer, primary_key=True, autoincrement=True)
    customer_code = Column(VARCHAR, primary_key=True)
    int_stock_serial = Column(SMALLINT, primary_key=True)
    consumption_type = Column(VARCHAR, nullable=False)
    item_code = Column(VARCHAR, nullable=False)
    nonmo_item_code = Column(VARCHAR)
    qty = Column(REAL, nullable=False)
    issue_to_customer_code = Column(VARCHAR, nullable=False)
    date_time_issued = Column(TIMESTAMP)
    issued_by = Column(VARCHAR)
    date_time_approved = Column(TIMESTAMP)
    approved_by = Column(VARCHAR)
    station_code = Column(VARCHAR, nullable=False)
    dept_code = Column(VARCHAR, nullable=False)
    sub_dept_code = Column(VARCHAR, nullable=False)
    sh_no = Column(VARCHAR, nullable=False)
    iwo_srl = Column(Integer)
    remarks = Column(VARCHAR(255))
    dart_number = Column(VARCHAR(250))
    location_on_board = Column(VARCHAR(250))
    nomenclature = Column(VARCHAR(50))
    reason = Column(VARCHAR(50))
    download_date_time = Column(TIMESTAMP)
    status_flag = Column(VARCHAR)
    int_gate_pass_no = Column(VARCHAR(12))
    date_time_closed = Column(TIMESTAMP)
    closed_by = Column(VARCHAR(10))


class fob_internal_stock(postgres_session.App_Base):
    __tablename__ = 'fob_internal_stock'
    item_code = Column(VARCHAR(32), primary_key=True)
    station_code = Column(VARCHAR(1), primary_key=True)
    customer_code = Column(VARCHAR(4), primary_key=True)
    int_stock_serial = Column(Integer, primary_key=True)
    nonmo_item_code = Column(VARCHAR(35))
    sh_no = Column(VARCHAR(4), nullable=False)
    condition_code = Column(VARCHAR(4), nullable=False)
    miqp_qty = Column(Numeric)
    location_marking = Column(VARCHAR(16))
    qty = Column(Numeric)
    int_store_receipt_no = Column(VARCHAR(20), nullable=False)
    dept_code = Column(VARCHAR(5), nullable=False)
    sub_dept_code = Column(VARCHAR(5), nullable=False)
    remarks = Column(VARCHAR(255))
    reason = Column(VARCHAR(255))
    download_date_time = Column(TIMESTAMP)
    status_flag = Column(VARCHAR(2))


class fob_internal_item_details(postgres_session.App_Base):
    __tablename__ = 'fob_internal_item_details'
    # table for allowance
    item_code = Column(VARCHAR, nullable=False, primary_key=True)
    hsn_code = Column(VARCHAR, nullable=False)
    allowance_qty = Column(REAL, nullable=False)


class fob_internal_store_receipt(postgres_session.App_Base):
    __tablename__ = 'fob_internal_store_receipt'
    int_store_receipt_no = Column(VARCHAR, primary_key=True)
    item_code = Column(VARCHAR, nullable=False)
    sh_no = Column(VARCHAR, nullable=False)
    date_time_received = Column(TIMESTAMP, nullable=False)
    int_store_receipt_choice = Column(VARCHAR, nullable=False)
    customer_code = Column(VARCHAR, nullable=False)
    mo_demand_no = Column(VARCHAR)
    internal_demand_no = Column(VARCHAR)
    remarks = Column(VARCHAR(250))
    date_time_prepared = Column(TIMESTAMP, nullable=False, default=func.now())
    prepared_by = Column(VARCHAR, nullable=False)
    date_time_approved = Column(TIMESTAMP)
    approved_by = Column(VARCHAR)
    station_code = Column(VARCHAR, nullable=False)
    miqp_qty = Column(REAL)
    pack_type = Column(VARCHAR)
    qty_received = Column(REAL)
    qty_on_charge = Column(REAL)
    date_manufactured = Column(TIMESTAMP)
    date_expiry = Column(TIMESTAMP)
    location_marking = Column(VARCHAR)
    gate_pass_no = Column(VARCHAR)
    int_gate_in_date_time = Column(TIMESTAMP)
    return_id = Column(VARCHAR)
    dept_code = Column(VARCHAR)
    sub_dept_code = Column(VARCHAR)
    nonmo_item_code = Column(VARCHAR)
    refit_customer_code = Column(VARCHAR)
    condition_code = Column(VARCHAR)
    id_line_no = Column(SMALLINT),
    issue_date_time = Column(TIMESTAMP)
    issued_int_stock_serial = Column(Integer),
    reason = Column(VARCHAR)
    download_date_time = Column(TIMESTAMP)
    status_flag = Column(VARCHAR)
    closed_by = Column(VARCHAR)
    date_time_closed = Column(TIMESTAMP)

    @validates('date_time_received')
    def validate_priority_code(self, key, value: datetime) -> datetime:
        if value.year < 97 or value.date() > datetime.now().date():
            raise PostgresError(
                message=f'date_time_received cannot be future date and prior to 1997 (iTrig_fob_internal_store_receipt)!',
                code=96104)
        return value

    @validates('date_manufactured')
    def validate_priority_code(self, key, value: datetime) -> datetime:
        if value is None or value.date() > datetime.now().date():
            raise PostgresError(
                message=f'date_manufactured cannot be future date(iTrig_fob_internal_store_receipt)!',
                code=96126)
        return value

    @validates('date_expiry')
    def validate_priority_code(self, key, value: datetime) -> datetime:
        if value is None or value.date() < datetime.now().date():
            raise PostgresError(
                message=f'date_expiry cannot be past date(iTrig_fob_internal_store_receipt)!',
                code=96127)
        return value

    @validates('item_code', 'customer_code', 'mo_demand_no')
    def validate_priority_code(self, key, value: str) -> str:
        if value is None or 0 == len(value.strip()):
            raise PostgresError(
                message=f'{key} cannot be blank',
                code=96102)
        return value.strip()


class fob_stock_release(postgres_session.App_Base):
    __tablename__ = 'fob_stock_release'
    customer_code = Column(VARCHAR(4), nullable=False, primary_key=True)
    demand_no = Column(VARCHAR(7), nullable=False, primary_key=True)
    issue_date_time = Column(TIMESTAMP, nullable=False, primary_key=True)
    stock_release_serial = Column(VARCHAR(20), nullable=False, primary_key=True)
    stock_release_date_time = Column(TIMESTAMP, nullable=False)
    item_code = Column(VARCHAR(32), nullable=False)
    stock_serial = Column(VARCHAR(20), nullable=False)
    qty = Column(VARCHAR(40), nullable=False)
    handed_over_by = Column(VARCHAR(8), nullable=False)
    date_time_taken_over = Column(TIMESTAMP, nullable=False)
    taken_over_by = Column(VARCHAR(8), nullable=False)
    station_code = Column(VARCHAR(1), nullable=False, primary_key=True)
    download_date_time = Column(TIMESTAMP, nullable=False)
    status_flag = Column(VARCHAR(20), nullable=False)


class fob_internal_demand(postgres_session.App_Base):
    __tablename__ = 'fob_internal_demand'
    customer_code = Column(CHAR(4), nullable=False)
    internal_demand_no = Column(CHAR(16), nullable=False, primary_key=True)
    station_code = Column(CHAR(1), nullable=False)
    internal_demand_type = Column(CHAR(3))
    raised_for_customer = Column(CHAR(4))
    iwo_srl = Column(Integer)
    authority_type = Column(CHAR(3))
    refit_no = Column(CHAR(5))
    role_name = Column(CHAR(15))
    remarks = Column(VARCHAR(255))
    raised_by = Column(CHAR(8))
    date_time_raised = Column(TIMESTAMP)
    authorised_by = Column(CHAR(8))
    date_time_authorised = Column(TIMESTAMP)
    closing_code = Column(CHAR(1))
    closed_by = Column(CHAR(8))
    date_time_closed = Column(TIMESTAMP)
    reason = Column(VARCHAR(255))
    download_date_time = Column(TIMESTAMP)
    date_time_updated = Column(TIMESTAMP)
    status_flag = Column(CHAR(2))
    mo_station_code = Column(CHAR(1))


class fob_internal_demand_line(postgres_session.App_Base):
    __tablename__ = 'fob_internal_demand_line'
    customer_code = Column(CHAR(4), nullable=False)
    internal_demand_no = Column(CHAR(16), nullable=False, primary_key=True)
    id_line_no = Column(SMALLINT, nullable=False, primary_key=True)
    item_code = Column(CHAR(32), nullable=False)
    nonmo_item_code = Column(CHAR(32))
    qty = Column(REAL, nullable=False)
    priority_code = Column(CHAR(1), nullable=False)
    eqpt_item_code = Column(CHAR(32))
    authority_ref = Column(CHAR(20))
    authority_date = Column(TIMESTAMP)
    idl_action_type = Column(CHAR(3), nullable=False)
    station_code = Column(CHAR(1), nullable=False)
    action_by = Column(CHAR(8))
    date_time_action = Column(TIMESTAMP)
    action_remarks = Column(VARCHAR(120))
    closing_code = Column(CHAR(1))
    date_time_closed = Column(TIMESTAMP)
    reason = Column(VARCHAR(255))
    status_flag = Column(VARCHAR(2))
    mo_demand_no = Column(CHAR(7))
    download_date_time = Column(TIMESTAMP)
    date_time_updated = Column(TIMESTAMP)
    int_consumption_no = Column(Integer)


class FobUsers(postgres_session.App_Base):
    __tablename__ = 'fob_users'
    login_id = Column(CHAR(8), primary_key=True)
    id = Column(CHAR(8))
    name = Column(CHAR(30))
    rank = Column(CHAR(10))
    department = Column(CHAR(8))
    station_code = Column(CHAR(1))
    date_time_left = Column(TIMESTAMP)
    date_time_joined = Column(TIMESTAMP, default=func.now())
    download_date_time = Column(TIMESTAMP)
    status_flag = Column(CHAR(2))


class fob_item(postgres_session.App_Base):
    __tablename__ = 'fob_item'
    item_code = Column(VARCHAR(32), primary_key=True)
    section_head = Column(VARCHAR(2), nullable=False)
    item_desc = Column(CHAR(60), nullable=False)
    item_deno = Column(CHAR(3), nullable=False)
    crp_category = Column(CHAR(1), nullable=False)
    abc_category = Column(CHAR(1), nullable=False)
    download_date_time = Column(TIMESTAMP)
    status_flag = Column(CHAR(2))
    country_code = Column(VARCHAR(3))
    months_shelf_life = Column(SMALLINT)
    ved_category = Column(VARCHAR(1))
    date_time_approved = Column(TIMESTAMP)
    approved_by = Column(VARCHAR(8))
    review_sub_section_code = Column(VARCHAR(2))
    incatyn = Column(VARCHAR(1))


class FobGatePass(postgres_session.App_Base):
    __tablename__ = 'fob_gate_pass'
    gate_pass_key = Column(TIMESTAMP, primary_key=True)
    gate_pass_no = Column(VARCHAR, nullable=False)
    transportation_mode = Column(VARCHAR)
    transport_no = Column(VARCHAR)
    destination = Column(VARCHAR)
    escort_name = Column(VARCHAR(30))
    remarks = Column(VARCHAR(255))
    initiated_by = Column(VARCHAR)
    date_time_approved = Column(TIMESTAMP)
    approved_by = Column(VARCHAR)
    date_time_gate_out = Column(TIMESTAMP)
    station_code = Column(VARCHAR)
    flag = Column(VARCHAR)
    download_date_time = Column(VARCHAR)
    status_flag = Column(VARCHAR)
    # @validates('date_time_approved', 'approved_by')
    # def validate_priority_code(self, key, value: str) -> str:
    #     if value is None or 0 == len(value.strip()):
    #         raise PostgresError(
    #             message='CONSTRAINT Demand_PriorityCode: Cannot insert the Demand as PriorityCode has CHECK',
    #             code=1010)
    #     return value.strip()


class FobStockDelivery(postgres_session.App_Base):
    __tablename__ = 'fob_stock_delivery'
    stock_delivery_key = Column(TIMESTAMP, primary_key=True)
    customer_code = Column(VARCHAR)
    demand_no = Column(VARCHAR)
    item_code = Column(VARCHAR(32))
    issue_date_time = Column(TIMESTAMP)
    stock_release_serial = Column(VARCHAR(20))
    qty_carried = Column(FLOAT)
    gate_pass_key = Column(TIMESTAMP)
    marking = Column(VARCHAR(30))
    date_time_delivered = Column(TIMESTAMP)
    station_code = Column(VARCHAR)
    download_date_time = Column(TIMESTAMP)
    status_flag = Column(VARCHAR)
    internal_demand_no = Column(CHAR(16), nullable=False)
    id_line_no = Column(SMALLINT, nullable=False)


class FobInternalGateIn(postgres_session.App_Base):
    __tablename__ = 'fob_internal_gate_in'
    int_gate_in_date_time = Column(TIMESTAMP, primary_key=True, default=func.now())
    gate_pass_key = Column(TIMESTAMP)
    no_of_packages = Column(Integer, nullable=False)
    package_type = Column(VARCHAR(120), nullable=False)
    received_from = Column(VARCHAR(120), nullable=False)
    transport_no = Column(VARCHAR)
    transporter_name = Column(VARCHAR(30))
    date_time_approved = Column(TIMESTAMP)
    approved_by = Column(VARCHAR(120), nullable=False)
    station_code = Column(VARCHAR(120), nullable=False)
    remarks = Column(VARCHAR(120))
    customer_code = Column(VARCHAR(120), nullable=False)
    dept_code = Column(VARCHAR(120), nullable=False)
    sub_dept_code = Column(VARCHAR(120), nullable=False)
    gate_in_type = Column(VARCHAR(120), nullable=False)
    order_ref = Column(VARCHAR(120))
    order_date = Column(TIMESTAMP)
    reason = Column(VARCHAR(50))
    download_date_time = Column(TIMESTAMP)
    status_flag = Column(VARCHAR(120))

    @validates('customer_code'
        , 'gate_in_type'
        , 'approved_by'
        , 'transport_no'
        , 'received_from'
               )
    def validate_priority_code(self, key, value: str) -> str:
        if value is None or 0 == len(value.strip()):
            raise PostgresError(
                message=f'{key} cannot be blank',
                code=1010)
        return value.strip()

    @validates('int_gate_in_date_time')
    def validate_priority_code(self, key, value: datetime) -> datetime:
        if value == datetime.now():
            raise PostgresError(
                message=f'{key} should be current date time',
                code=68816)

        return value


class FobUserRole(postgres_session.App_Base):
    __tablename__ = "fob_user_role"
    login_id = Column(VARCHAR(8), primary_key=True)
    role_name = Column(VARCHAR(15))
    date_time_activated = Column(TIMESTAMP, default=func.now())
    date_time_closed = Column(TIMESTAMP, nullable=True)
    station_code = Column(VARCHAR(1))
    download_date_time = Column(TIMESTAMP, nullable=True)
    status_flag = Column(VARCHAR(2), nullable=True)


class FobInternalCustomerUser(postgres_session.App_Base):
    __tablename__ = "fob_internal_customer_user"
    login_id = Column(VARCHAR(8), primary_key=True)
    role_name = Column(VARCHAR(15))
    customer_code = Column(VARCHAR(4))
    date_time_added = Column(TIMESTAMP,default=func.now())
    added_by = Column(VARCHAR(8))
    date_time_closed = Column(TIMESTAMP, nullable=True)
    closed_by = Column(VARCHAR(8), nullable=True)


class fob_code_table(postgres_session.App_Base):
    __tablename__ = "fob_code_table"
    column_name = Column(VARCHAR(30), primary_key=True)
    code_value = Column(VARCHAR(10), primary_key=True)
    description = Column(VARCHAR(30))


class fob_customer(postgres_session.App_Base):
    __tablename__ = "fob_customer"
    customer_code = Column(VARCHAR, primary_key=True)
    name = Column(VARCHAR(31), nullable=True)
    date_closed = Column(TIMESTAMP, nullable=True)
    customer_type = Column(VARCHAR)
    mother_depot = Column(VARCHAR)
    addressee = Column(VARCHAR)
    address_line1 = Column(VARCHAR)
    address_line2 = Column(VARCHAR)
    address_line3 = Column(VARCHAR)
    city = Column(VARCHAR(30))
    state = Column(VARCHAR)
    pin_code = Column(VARCHAR)
    allowance_annual_rs = Column(VARCHAR)
    date_introduced = Column(TIMESTAMP)
    remarks = Column(VARCHAR)
    admin_authority = Column(VARCHAR)
    station_code = Column(VARCHAR)
    added_by = Column(VARCHAR)
    closed_by = Column(VARCHAR)
    download_date_time = Column(TIMESTAMP)
    status_flag = Column(VARCHAR)


class fob_item_line(postgres_session.App_Base):
    __tablename__ = "fob_item_line"
    item_code = Column(VARCHAR, primary_key=True)
    station_code = Column(VARCHAR, primary_key=True)
    item_line_serial = Column(SMALLINT, primary_key=True)
    date_time_closed = Column(TIMESTAMP, nullable=True)
    sh_no = Column(VARCHAR)
    qty_war_reserve = Column(REAL)
    qty_msl = Column(REAL)
    qty_usl = Column(REAL)
    qty_acl = Column(REAL)
    days_lt_proc = Column(SMALLINT)
    date_time_added = Column(TIMESTAMP)


@listens_for(fob_internal_store_receipt, 'before_insert')
def receive_before_insert(mapper, connection, target):
    """
    -- checks for trigger fob_internal_store_receipt
    """
    sess = postgres_session.get_session()

    # --2.item_code cannot be null for int_store_receipt_choice as I
    if target.item_code is None and 'I' == target.int_store_receipt_choice:
        raise PostgresError(
            message='item_code cannot be null for int_store_receipt_choice as I'
            , code=96113)

    # --4.int_store_receipt_choice not found in fob_code_table
    check_code_table_srv_choice: bool = 0 == sess.query(fob_code_table).filter(
        fob_code_table.column_name == 'StoreReceiptChoice',
        fob_code_table.code_value == target.int_store_receipt_choice).count()
    if check_code_table_srv_choice:
        raise PostgresError(
            message='int_store_receipt_choice not found in fob_code_table'
            , code=96107)

    # --5.internal_demand_no cannot be null for int_store_receipt_choice  as I
    if 'I' == target.int_store_receipt_choice and target.internal_demand_no is None:
        raise PostgresError(
            message='internal_demand_no cannot be null for int_store_receipt_choice  as I'
            , code=96112)
    # --6.item_code cannot be null for int_store_receipt_choice as I
    if 'I' == target.int_store_receipt_choice and target.item_Code is None:
        raise PostgresError(
            message='item_code cannot be null for int_store_receipt_choice as I'
            , code=96113)
    # 7.Item not found in fob_item_line table
    item_line_check: bool = 0 == sess.query(fob_item_line).filter(fob_item_line.item_code == target.item_code,
                                                                  fob_item_line.station_code == target.station_code,
                                                                  fob_item_line.date_time_closed.is_(None)).count()
    if 'O' == target.int_store_receipt_choice and item_line_check:
        raise PostgresError(
            message='Item not found in fob_item_line table'
            , code=96108)
    # --8. mo_demand_no cannot be null for int_store_receipt_choice as X and C
    if target.int_store_receipt_choice in ('X', 'C') and target.mo_demand_no is None:
        raise PostgresError(
            message='mo_demand_no cannot be null for int_store_receipt_choice as X and C'
            , code=96114)
    #   --12. qty_received should be greater than zero
    if target.int_store_receipt_choice not in ('S', 'O') and target.qty_received is None or 0 > target.qty_received:
        raise PostgresError(
            message='qty_received should be greater than zero'
            , code=96128)
    #   --12. qty_on_charge should be greater than zero
    if target.int_store_receipt_choice not in ('S', 'O') and target.qty_on_charge is None or 0 > target.qty_on_charge:
        raise PostgresError(
            message='qty_on_charge should be greater than zero'
            , code=96128)
    # --13.gate_pass_no cannot be blank if mo_demand_no is not blank
    if target.mo_demand_no is not None:
        if 0 == len(target.mo_demand_no.strip()) and (target.gate_pass_no is None):
            raise PostgresError(
                message='gate_pass_no cannot be blank if mo_demand_no is not blank(iTrig_fob_internal_store_receipt)!'
                , code=96128)
    # --15.customer_code not found in Customer Table or is Closed customer
    customer_check: bool = 0 == sess.query(fob_customer).filter(fob_customer.customer_code == target.customer_code,
                                                                fob_customer.date_closed.is_(None)).count()
    if customer_check:
        raise PostgresError(
            message='customer_code not found in Customer Table or is Closed customer(iTrig_fob_internal_store_receipt)!'
            , code=96132)
    # --17.internal_demand_no/mo_demand_no both cannot be null for int_store_receipt_choice as L
    if 'L' == target.int_store_receipt_choice and target.internal_demand_no is None and target.mo_demand_no is None:
        raise PostgresError(
            message='internal_demand_no/mo_demand_no both cannot be null for int_store_receipt_choice as L(iTrig_fob_internal_store_receipt)!'
            , code=96116)

    # fob_internal_store_receipt.
    # --18.prepared_by not found in fob_users Table
    if target.prepared_by is None and (
            0 == sess.query(FobUsers).filter(FobUsers.login_id == target.prepared_by).count()):
        raise PostgresError(message='prepared_by not found in fob_users Table(iTrig_fob_internal_store_receipt)!',
                            code=96138)

    # --19.approved_by not found in fob_users Table
    # if target.approved_by is None and (
    #         0 == sess.query(FobUsers).filter(FobUsers.login_id == target.approved_by).count()):
    #     raise PostgresError(message='approved_by not found in fob_users Table(iTrig_fob_internal_store_receipt)!',
    #                         code=96139)
    #  --20.pack_type not found in fob_code_table
    check_code_table_pack_type: bool = 0 == sess.query(fob_code_table).filter(fob_code_table.column_name == 'PackType',
                                                                              fob_code_table.code_value == target.pack_type).count()
    if check_code_table_pack_type:
        raise PostgresError(message='pack_type not found in fob_code_table(iTrig_fob_internal_store_receipt)!',
                            code=96121)
    # --22.qty_on_charge cannot be greater than qty_received
    if target.qty_on_charge > target.qty_on_charge:
        raise PostgresError(
            message='qty_on_charge cannot be greater than qty_received(iTrig_fob_internal_store_receipt)!', code=96124)
    #   --25. item_code / non_mo_item_code both cannot be blank
    if (target.item_code is None or 0 == len(target.item_code)) and (
            target.nonmo_item_code is None or 0 == len(target.nonmo_item_code)):
        raise PostgresError(message='item_code/non_mo_item_code both cannot be blank(iTrig_fob_internal_store_receipt)!'
                            , code=96103)

    #  26.non_mo_item_code cannot blank for int_store_receipt_choice as N
    if target.int_store_receipt_choice.strip() == 'N' and target.nonmo_item_code is None:
        raise PostgresError(
            message='non_mo_item_code cannot blank for int_store_receipt_choice as N(iTrig_fob_internal_store_receipt)!',
            code=96136)
