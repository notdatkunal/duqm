from sqlalchemy import text


def insert_data():
    from fob_postgres.check_data import item_sql, item_line_sql
    from fob_postgres.data import customer_table_sql, code_table_sql,internal_customer_user
    from fob_postgres.pg_session import postgres_session
    from fob_postgres.tables import fob_item, fob_item_line, FobInternalCustomerUser, FobUserRole, fob_customer, fob_code_table

    with postgres_session.get_session() as sess:
        if 0 == sess.query(fob_item).count():
            sess.execute(text(item_sql))
            sess.commit()
        if 0 == sess.query(fob_item_line).count():
            sess.execute(text(item_line_sql))
            sess.commit()
        if 0 == sess.query(fob_customer).count():
            for stmt in customer_table_sql.strip().split(';'):
                if stmt.strip():
                    sess.execute(text(stmt))
                    sess.commit()
        if 0 == sess.query(fob_code_table).count():
            sess.execute(text(code_table_sql))
            sess.commit()
        if sess.query(FobInternalCustomerUser).count()<5:
            sess.execute(text(internal_customer_user))
            sess.commit()



def create_users():
    from fob_postgres.tables import FobUsers, FobUserRole, FobInternalCustomerUser, fob_customer
    from fob_postgres.pg_session import postgres_session
    with postgres_session.get_session() as sess:
        if 0 < sess.query(FobUsers).count():
            return
        user: FobUsers = FobUsers()
        user.id = 'EST'
        user.name = 'User'
        user.rank = 'cdr'
        user.station_code = 'B'
        user.login_id = '10971h'
        user.department = 'LOGO'
        sess.add(user)
        user_role: FobUserRole = FobUserRole()
        user_role.login_id = user.login_id
        user_role.role_name = 'LOGO'
        user_role.station_code = user.station_code
        sess.add(user_role)
        # internal_customer_user: FobInternalCustomerUser = FobInternalCustomerUser()
        # internal_customer_user.added_by = 'system'
        # internal_customer_user.login_id = user.login_id
        # internal_customer_user.role_name = user_role.role_name
        # internal_customer_user.customer_code = '2096'
        # sess.add(internal_customer_user)
        # customer:fob_customer = fob_customer()
        # customer.customer_code = internal_customer_user.customer_code
        # customer.name = 'MLC DUQM'
        # customer.customer_type = 'EST'
        # customer.mother_depot = 'MO(MB)'
        # sess.add(customer)
        sess.commit()



