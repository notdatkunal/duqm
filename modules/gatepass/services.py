from typing import Type

import pandas as pd
import numpy as np
from flask import jsonify
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from fob_postgres.pg_session import postgres_session
from fob_postgres.tables import fob_internal_demand_line
from helpers import exceptions , commonn_utils
from fob_postgres import functions as pf
from concurrent.futures import ThreadPoolExecutor

from modules.gatepass.models import FOB_InternalDemandArgs

executor = ThreadPoolExecutor(max_workers=100)


def background_task(item_row: FOB_InternalDemandArgs):
    try:
        print(f'this is background task {item_row.IDLineNo} {item_row.FOBInternalDemandNo} {item_row.MoDemandNo}')
        item_obj: Type[fob_internal_demand_line] = postgres_session.get_session().query(fob_internal_demand_line).filter(fob_internal_demand_line.id_line_no==item_row.IDLineNo,fob_internal_demand_line.internal_demand_no==item_row.FOBInternalDemandNo).one()
        item_obj.mo_demand_no = item_row.MoDemandNo
        item_obj.date_time_updated = datetime.now()
        postgres_session.get_session().commit()
    except DBAPIError as e:
        postgres_session.get_session().rollback()
        print(f'error updating : {item_row} because: {e.args}')


def import_gatepass_service(file,customer_code: int):
    full_df = pd.read_csv(file)
    full_df = full_df[full_df['CustomerCode'] == customer_code]
    seperator_col = "Separator"
    # seperator_value = 'Stock Delivery'
    spe_idx = full_df.columns.get_loc(seperator_col)
    gatepass_df = full_df.iloc[:, :spe_idx]
    stock_delivery_df = full_df.iloc[:, spe_idx + 1:]
    key_cols = ["GatePassKey", "StationCode"]

    unique_gatepass_df = gatepass_df.drop_duplicates(subset=key_cols)

    for key in key_cols:
        if key not in stock_delivery_df.columns:
            stock_delivery_df[key] = gatepass_df[key]

    unique_gatepass_df.rename(columns={
        'ApprovedBy': 'approved_by',
        'AuthorityRef': 'authority_ref',
        'DateTimeApproved': 'date_time_approved',
        'DateTimeGateOut': 'date_time_gate_out',
        'Destination': 'destination',
        'EscortName': 'escort_name',
        'Flag': 'flag',
        'GateOutBy': 'gate_out_by',
        'GatePassKey': 'gate_pass_key',
        'GatePassNo': 'gate_pass_no',
        'InitiatedBy': 'initiated_by',
        'Remarks': 'remarks',
        'StationCode': 'station_code',
        'TransportNo': 'transport_no',
        'TransportationMode': 'transportation_mode',
    }, inplace=True)

    stock_delivery_df.rename(columns={
        "CustomerCode": 'customer_code',
        "DateTimeDelivered": 'date_time_delivered',
        "DemandNo": 'demand_no',
        "GatePassKey.3": 'gate_pass_key',
        # "GatePassKey.1": NaN,
        "IssueDateTime": 'issue_date_time',
        "Marking": 'marking',
        "QtyCarried": 'qty_carried',
        "StationCode": 'station_code',
        "StationCode.1": "B",
        "StockDeliveryKey": 'stock_delivery_key',
        "StockReleaseSerial": 'stock_release_serial',
        "ItemCode": 'item_code',
        "InternalDemandNo": 'internal_demand_no',
        "IDLineNo": 'id_line_no'
    }, inplace=True)
    # breakpoint()
    unique_gatepass_df['date_time_approved'] = unique_gatepass_df['date_time_approved'].apply(format_date)
    unique_gatepass_df['date_time_gate_out'] = unique_gatepass_df['date_time_gate_out'].apply(format_date)
    unique_gatepass_df['gate_pass_key'] = unique_gatepass_df['gate_pass_key'].apply(format_date)
    stock_delivery_df['date_time_delivered'] = stock_delivery_df['date_time_delivered'].apply(format_date)
    stock_delivery_df['issue_date_time'] = stock_delivery_df['issue_date_time'].apply(format_date)
    stock_delivery_df['gate_pass_key'] = stock_delivery_df['gate_pass_key'].apply(format_date)
    stock_delivery_df['stock_delivery_key'] = stock_delivery_df['stock_delivery_key'].apply(format_date)

    # breakpoint()
    gatepass_query = """
                INSERT INTO public.fob_gate_pass(
	                        gate_pass_key, authority_ref, gate_pass_no, transportation_mode, 
                            transport_no, destination, escort_name, remarks, 
                            initiated_by, date_time_approved, approved_by, date_time_gate_out, 
                            gate_out_by, station_code, flag
                        )
	                    VALUES (
                            :gate_pass_key , :authority_ref , :gate_pass_no , :transportation_mode , 
                            :transport_no , :destination , :escort_name , :remarks , 
                            :initiated_by , :date_time_approved , :approved_by , :date_time_gate_out , 
                            :gate_out_by , :station_code , :flag
                        );
        """
    stock_delivery_query = """
                INSERT INTO public.fob_stock_delivery(
	                        stock_delivery_key, customer_code, demand_no, issue_date_time, 
                            stock_release_serial, qty_carried, gate_pass_key, marking, 
                            date_time_delivered, station_code,item_code,internal_demand_no,id_line_no
                        )
	                    VALUES (
                            :stock_delivery_key , :customer_code , :demand_no , :issue_date_time , 
                            :stock_release_serial , :qty_carried , :gate_pass_key , :marking , 
                            :date_time_delivered , :station_code, :item_code,:internal_demand_no,:id_line_no
                        );
        """
    gatepass_data = unique_gatepass_df.replace({np.nan: None}).to_dict(orient='records')
    stock_delivery_data = stock_delivery_df.replace({np.nan: None}).to_dict(orient='records')
    # breakpoint()
    app_session = postgres_session.get_session()
    #TODO: write transaction level logic to commit gatepass insert only when it's stock delivery has values

    try:
        for gd in gatepass_data:
            app_session.execute(text(gatepass_query), gd)
            app_session.commit()
        for sd in stock_delivery_data:
            internal_demand_item = FOB_InternalDemandArgs(FOBInternalDemandNo=sd['internal_demand_no']
                                                          , IDLineNo=sd['id_line_no']
                                                          , MoDemandNo=sd['demand_no']
                                                          )
            app_session.execute(text(stock_delivery_query), sd)
            app_session.commit()
            if internal_demand_item.FOBInternalDemandNo or 0 != len(internal_demand_item.FOBInternalDemandNo.strip()) and internal_demand_item.IDLineNo:
                background_task(internal_demand_item)
            else:
                print(f'cannot import internal demand')

    except DBAPIError as e:
        app_session.rollback()
        print(f'exception : {e.args}')
    return jsonify({'gatepass': gatepass_data, 'stock_del': stock_delivery_data})


def format_date(ts: str | None):
    print(f'this is {type(ts)} {ts}')
    if ts is None or float == type(ts):
        return None
    try:
        ts = str(ts)
        original_format = "%d/%m/%Y %H:%M:%S:%f"
        if str(ts).count(':') == 2:
            ts = f'{ts}:000'

        parsed_date = datetime.strptime(ts, original_format)
        new_format = "%Y-%m-%d %H:%M:%S.%f"
        formatted_date = str(parsed_date.strftime(new_format))

        return formatted_date
    except Exception as e:
        print("error ", e)
        return None



def gatein_not_made_service():
    query = """
        select * from fob_gate_pass where gate_pass_key not in ( select gate_pass_key from fob_internal_gate_in )
    """
    result = pf.execute_query_with_results(query=query,as_dict=True)
    for i in range(len(result)):
        result[i-1]["gate_pass_key"] = commonn_utils.format_date_postgres_timestamp(result[i-1]["gate_pass_key"])
        result[i-1]["date_time_approved"] = commonn_utils.format_date_postgres_timestamp(result[i-1]["date_time_approved"])
    return result


def gatepass_list_service(from_date:str, to_date:str, gate_pass_key:str):
    query = " select * from fob_gate_pass "

    where =" where true "
    if from_date is not None:
        where += f" and gate_pass_key >= \'{from_date}\' "
    if to_date is not None:
        where += f" and gate_pass_key >= \'{to_date}\' "
    if gate_pass_key is not None:
        where += f" and gate_pass_key = \'{gate_pass_key}\' "
    query += where
    result = pf.execute_query_with_results(query=query,as_dict=True)
    for i in range(len(result)):
        result[i-1]["gate_pass_key"] = commonn_utils.format_date_postgres_timestamp(result[i-1]["gate_pass_key"])
        result[i-1]["date_time_approved"] = commonn_utils.format_date_postgres_timestamp(result[i-1]["date_time_approved"])
    return result

def gate_pass_by_gatepass_key(gate_pass_key:str):
    gk = gate_pass_key.lower().replace("and","").replace("%","").replace("or","")
    if len(gk) != len(gate_pass_key):
        raise exceptions.BadRequestException("invalid gatepass key")
    query = f""" 
                select * from fob_gate_pass g 
                        where g.gate_pass_key = \'{gate_pass_key}\' 
            """
    stock_delivery_query = f"""
                select * from fob_stock_delivery where gate_pass_key = \'{gate_pass_key}\'
    """
    stock_delivery_result = pf.execute_query_with_results(query=stock_delivery_query,as_dict=True)

    result = pf.execute_query_with_results(query=query,as_dict=True)
    for i in range(len(result)):
        result[i-1]["gate_pass_key"] = commonn_utils.format_date_postgres_timestamp(result[i-1]["gate_pass_key"])
        result[i-1]["date_time_approved"] = commonn_utils.format_date_postgres_timestamp(result[i-1]["date_time_approved"])

    for i in range(len(stock_delivery_result)):
        stock_delivery_result[i-1]["gate_pass_key"] = commonn_utils.format_date_postgres_timestamp(stock_delivery_result[i-1]["gate_pass_key"])
        stock_delivery_result[i-1]["stock_delivery_key"] = commonn_utils.format_date_postgres_timestamp(stock_delivery_result[i-1]["stock_delivery_key"])

    result[0]['stock_delivery_delivery'] = stock_delivery_result
    return result
