from typing import Final

from fob_postgres.functions import execute_query_with_results, execute_query_with_dictionary
from sqlalchemy import distinct, text, func
from helpers.constants import Check, CustomerCodes
from helpers import exceptions
from fob_postgres.pg_session import postgres_session
from fob_postgres import tables as t
import pandas as pd



def get_customer_code(station_code):
    for code in CustomerCodes:
        if code.name == station_code:
            return code.value

    return CustomerCodes.B.value



def list_closing_codes():
    query: Final[str] = r"""
        SELECT   code_value,description FROM public.fob_code_table
        WHERE  column_name = 'ClosingCode' 

    """
    results = execute_query_with_results(query)
    results_data = [dict(zip(['code_value', 'description'], row)) for row in results]
    return results_data


def list_priority_codes():
    query: Final[str] = r"""
        SELECT   code_value,description FROM public.fob_code_table
        WHERE  column_name = 'PriorityCode' 

    """
    results = execute_query_with_results(query)
    results_data = [dict(zip(['code_value', 'description'], row)) for row in results]
    return results_data


def list_code_values(column_name: str):
    query: Final[str] = f"""
        SELECT   code_value,description FROM public.fob_code_table
        WHERE  column_name = '{column_name}' 

    """
    results = execute_query_with_results(query)
    results_data = [dict(zip(['code_value', 'description'], row)) for row in results]
    return results_data


def list_ship_customers():
    query: Final[str] = r"""
        SELECT customer_code, name 
        FROM public.fob_customer
        WHERE date_closed is null
    """
    results = execute_query_with_results(query)
    results_data = [dict(zip(['customer_code', 'name'], row)) for row in results]
    return results_data


def fetch_user_details(username: str) -> dict:
    user_query = """
                select u.login_id as username, u.name, u.rank, u.department, 
                u.station_code as stationcode, 
                c.customer_code,
                cc.name as customer_name
                from fob_users u
                    join fob_internal_customer_user c on u.login_id = c.login_id
                    join fob_customer cc on cc.customer_code = c.customer_code
                    where u.login_id =  :username
        """
    param = {
        "username": username,
    }

    user_data = execute_query_with_dictionary(user_query, parameters=param)
    if user_data[0] is None:
        raise exceptions.NotFoundAppException("Incorrect password")
    user_data = user_data[0]
    role_query = """
                    select role_name from fob_user_role where login_id = :username
                """
    roles_result = execute_query_with_results(role_query, param)
    roles = []
    for r in roles_result:
        roles.append(r[0])

    user_data["roles"] = roles
    return user_data


def station_code_service():
    query = " select distinct station_code from public.fob_item_line where station_code in ('B','W')"
    data = execute_query_with_results(query)
    result = []
    for d in data:
        result.append(d[0])
    return result


def package_type_service():
    query = " select code_value,description from fob_code_table where column_name = 'PackageType' "
    data = execute_query_with_results(query=query)
    result = []
    for d in data:
        result.append({'code': d[0], 'desc': d[1]})
    return result


def received_from_service():
    query = " select code_value,description from fob_code_table where column_name = 'ConsigneeCode' and code_value like 'CWH%' "
    data = execute_query_with_results(query=query)
    result = []
    for d in data:
        result.append({'code': d[0], 'desc': d[1]})
    return result


def internal_sh():
    query = """
    SELECT customer_code, int_sh_no, int_sh_desc, date_time_added, added_by, date_time_closed, closed_by
	FROM public.fob_internal_sh;
    """
    data = execute_query_with_results(query=query)
    results_data = [dict(
        zip(['customer_code', 'int_sh_no', 'int_sh_desc', 'date_time_added', 'added_by', 'date_time_closed',
             'closed_by'], row)) for row in data]
    return results_data


def customer_address_service(customer_code):
    sess = postgres_session.get_session()
    query = sess.query(
        func.trim(t.fob_customer.customer_code).label("customer_code"),
        func.trim(t.fob_customer.name).label("name"),
        func.trim(t.fob_customer.customer_type).label("customer_type"),
        func.trim(t.fob_customer.mother_depot).label("mother_depot"),
        func.trim(t.fob_customer.address_line1).label("address_line1"),
        func.trim(t.fob_customer.address_line2).label("address_line2"),
        func.trim(t.fob_customer.address_line3).label("address_line3"),
        func.trim(t.fob_customer.city).label("city"),
        func.trim(t.fob_customer.state).label("state"),
        func.trim(t.fob_customer.pin_code).label("pin_code"),
    ).filter(
        t.fob_customer.customer_code == customer_code
    )

    result = pd.read_sql(query.statement, query.session.bind)
    return result.to_dict(orient='records')
