from fob_postgres.tables import fob_demand_status
from fob_postgres.pg_session import postgres_session


def get_demand_status_q(search_type: str, search_param: str):
    fob_q = postgres_session.get_session().query(fob_demand_status)
    if search_type and search_param and 0 < len(search_param):
        if 'internal' not in search_type:
            fob_q = fob_q.filter(fob_demand_status.demand_no.contains(search_param))
        else:
            fob_q = fob_q.filter(fob_demand_status.internal_demand_no.contains(search_param))
    return fob_q
