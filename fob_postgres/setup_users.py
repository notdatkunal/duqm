


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
        internal_customer_user: FobInternalCustomerUser = FobInternalCustomerUser()
        internal_customer_user.added_by = 'system'
        internal_customer_user.login_id = user.login_id
        internal_customer_user.role_name = user_role.role_name
        internal_customer_user.customer_code = '2096'
        sess.add(internal_customer_user)
        customer:fob_customer = fob_customer()
        customer.customer_code = internal_customer_user.customer_code
        customer.name = 'MLC DUQM'
        customer.customer_type = 'EST'
        customer.mother_depot = 'MO(MB)'
        sess.add(customer)
        sess.commit()



