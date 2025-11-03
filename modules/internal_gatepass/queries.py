from fob_postgres.pg_session import postgres_session
from fob_postgres.tables import fob_internal_consumption, fob_internal_gate_pass


def get_pending_internal_gatepass_q(customer_code:str):
    query = postgres_session.get_session().query(fob_internal_consumption)
    query = query.filter(fob_internal_consumption.approved_by.is_not(None)
                         , fob_internal_consumption.int_gate_pass_no.is_(None)
                         , fob_internal_consumption.issue_to_customer_code.startswith(customer_code.strip()),
                         fob_internal_consumption.date_time_closed.is_(None),
                         )
    return query


def get_internal_gatepass_q():
    query = postgres_session.get_session().query(fob_internal_gate_pass)
    return query


def get_cons_from_int_gp_q(int_gate_pass_no, sess):
    return sess.query(fob_internal_consumption).filter(fob_internal_consumption.int_gate_pass_no == int_gate_pass_no)
