from datetime import datetime
from typing import Sequence
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError
#TODO to be deprecated

from dotenv import load_dotenv
from config.config import config


def exec_query_no_result(query,parameters=None):
    """
    in case of transactions like update or insert or delete
    Parameters
    ----------
    query

    Returns
    -------

    """
    print(f"\n{query}\n")
    engine = create_engine(get_postgres_conn_string())
    with engine.connect() as conn:
        try:
            conn.begin()
            conn.execute(text(query),parameters=parameters)
            conn.commit()
            conn.close()

        except DBAPIError as e:
            print(f'exception {e.args}')
            conn.close()
        return


def execute_query_with_dictionary(query: str, parameters=None) -> list[dict]:
    """

    Parameters
    ----------
    query

    Returns
    -------

    """
    print(f"\n{query}\n")
    if parameters:
        print(f"{parameters}\n")
    engine = create_engine(get_postgres_conn_string())
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        data = result.fetchall()
        result_data = [dict(zip(result.keys(), row)) for row in data]
        conn.close()
        return result_data


def execute_query_with_results(query: str, params=None,as_dict:bool=False) -> Sequence:
    """

    Parameters
    ----------
    query

    Returns
    -------

    """
    print(f"\n{query}\n")
    if params:
        print(f"{params}\n")
    engine = create_engine(get_postgres_conn_string())
    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        if as_dict:
            data = [dict(row._mapping) for row in result]
        else:
            data = result.fetchall()
        conn.commit()
        conn.close()
        return data


def get_postgres_con():
    engine = create_engine(get_postgres_conn_string())
    return engine.connect()


def get_postgres_conn_string():
    from fob_postgres.pg_admin import init_or_get_pgserver
    return init_or_get_pgserver()
    # return f'postgresql+pg8000://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}'


def concatenate_to_where(master_string: str, table_name: str, column_name: str, data, operator: str = '=') -> str:
    if data is not None and len(str(data)) > 0:
        if data is str:
            data = data.strip().replace('%', '')
        if len(master_string.strip()) > 7:
            master_string += 'AND '
        master_string += f'{table_name}.{column_name} {operator} \'{data}\' '
    return master_string


def convert_date_to_str(result: dict) -> dict:
    """
    works in case of dictionary only
    Parameters
    ----------
    result

    Returns
    -------

    """
    return {k: (str(v.date()) if isinstance(v, datetime) else v) for k, v in result.items()}


def format_string_q(query: str) -> str:
    query = query.replace('\'nan\'', 'null')
    query = query.replace('nan', 'null')
    query = query.replace('\'NaT\'', 'null')
    return query
