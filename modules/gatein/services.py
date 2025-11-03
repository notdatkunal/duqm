from datetime import datetime

from sqlalchemy import func, DateTime

from fob_postgres import functions
from fob_postgres.tables import FobInternalGateIn
from helpers import commonn_utils


def gatein_list_service(from_date: str, to_date: str, approved: bool):
    query = " select * from fob_internal_gate_in where "
    where = " true "
    if from_date is not None:
        where += f" and int_gate_in_date_time >= \'{from_date}\'"
    if to_date is not None:
        where += f" and int_gate_in_date_time < \'{to_date}\'"
    if approved is not None:
        if approved == 'true':
            where += f" and approved_by is not null "
        else:
            where += f" and approved_by is null "

    query = query + where

    result = functions.execute_query_with_results(query=query, as_dict=True)
    for i in range(len(result)):
        result[i - 1]["gate_pass_key"] = commonn_utils.format_date_postgres_timestamp(result[i - 1]["gate_pass_key"])
        result[i - 1]["int_gate_in_date_time"] = commonn_utils.format_date_postgres_timestamp(
            result[i - 1]["int_gate_in_date_time"])
    return result


def gate_in_insert_service(gate_in_details: dict):
    from fob_postgres.pg_session import postgres_session
    with postgres_session.get_session() as sess:
        print(gate_in_details.keys())
        gate_in_details.pop('int_gate_in_date_time', None)
        print(gate_in_details.keys())
        gate_in_obj = FobInternalGateIn(**gate_in_details)
        sess.add(gate_in_obj)
        sess.commit()
        sess.refresh(gate_in_obj)
        this_var = commonn_utils.format_date_postgres_timestamp(gate_in_obj.int_gate_in_date_time)
        return this_var

    # query = f"""
    #     INSERT INTO public.fob_internal_gate_in(
	#             int_gate_in_date_time, gate_pass_key, no_of_packages, package_type,
    #             received_from, transport_no, transporter_name,
    #             station_code, remarks, customer_code,
    #             gate_in_type, reason)
	#         VALUES (
    #             \'{curr_date}\', \'{gate_in_details['gate_pass_key']}\', \'{gate_in_details['no_of_packages']}\', \'{gate_in_details['package_type']}\',
    #             \'{gate_in_details['received_from']}\', \'{gate_in_details['transport_no']}\', \'{gate_in_details['transporter_name']}\',
    #              \'{gate_in_details['station_code']}\', \'{gate_in_details['remarks']}\', \'{gate_in_details['customer_code']}\',
    #              \'{gate_in_details['gate_in_type']}\',  \'{gate_in_details['reason']}\'
    #         )
    #         RETURNING *;
    # """
    # result = functions.execute_query_with_results(query, as_dict=True)


def approve_gate_in_service(gatein_date: str, approved_by: str):
    query = f"""
            UPDATE public.fob_internal_gate_in
	            SET date_time_approved= \'{datetime.now()}\', approved_by= \'{approved_by}\'
	                WHERE int_gate_in_date_time = \'{gatein_date}\'
                    RETURNING *;
    """
    data = functions.execute_query_with_results(query=query, as_dict=True)
    return data


def update_gate_in_service(gatein_date: str, json_body):
    query = f"""
            UPDATE public.fob_internal_gate_in
	            SET no_of_packages= \'{json_body["no_of_packages"]}\', package_type= \'{json_body["package_type"]}\' , 
                    received_from= \'{json_body["received_from"]}\' , transporter_name= \'{json_body["transporter_name"]}\' , 
                    remarks= \'{json_body["remarks"]}\'
	                WHERE int_gate_in_date_time = \'{gatein_date}\'
                    RETURNING *;
    """
    data = functions.execute_query_with_results(query=query, as_dict=True)
    return data


def get_int_gate_obj(int_gate_in_time):
    from sqlalchemy import func, TIMESTAMP
    print(f"-------------\n {int_gate_in_time}")
    query = f""" select * from  fob_internal_gate_in where  int_gate_in_date_time = \'{int_gate_in_time}\' """
    result = functions.execute_query_with_results(query=query, as_dict=True)
    result[0]["int_gate_in_date_time"] = commonn_utils.format_date_postgres_timestamp(
        result[0]["int_gate_in_date_time"])
    result[0]["gate_pass_key"] = commonn_utils.format_date_postgres_timestamp(result[0]["gate_pass_key"])
    return result[0]
    # return postgres_session.get_session().query(FobInternalGateIn).filter(FobInternalGateIn.int_gate_in_date_time == func.cast(int_gate_in_time, TIMESTAMP)).one().to_dict()
