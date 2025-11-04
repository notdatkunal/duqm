import numpy as np
import pandas as pd
from sqlalchemy import update

from fob_postgres.pg_session import postgres_session
from fob_postgres.tables import fob_demand_status, fob_internal_demand, fob_internal_demand_line
from fob_postgres.tables import fob_demand_status, fob_internal_demand_line, fob_item
from helpers.commonn_utils import format_date_postgres_timestamp
from helpers.exceptions import BadRequestException
from fob_postgres.functions import execute_query_with_results, execute_query_with_dictionary, convert_date_to_str, \
    exec_query_no_result
from datetime import datetime
import pandas
import os
from sqlalchemy.exc import DBAPIError
from modules.demand.queries import get_demand_status_q
from sqlalchemy import func


def create_internal_demand_unique_key(stationcode, customer_code):
    # Define the station_code
    station_code = stationcode  # Replace with your actual station code

    # Step 1: Get the current year and the max internal demand number
    current_year = str(datetime.now().year)[2:]

    query = f"""
        SELECT internal_demand_no
        FROM fob_internal_demand
        WHERE internal_demand_no LIKE '{current_year}{station_code}{customer_code}G01S%'
        ORDER BY internal_demand_no DESC
        LIMIT 1;
    """
    print(f'query {query}')
    result = execute_query_with_results(query)
    # conn.commit()
    # conn.close()

    if result:
        last_demand_no = str(result[0][0])

        print('last_demand_no')
        print(last_demand_no)
        last_number = int(last_demand_no[-5:])  # Get the last 5 digits
        new_number = last_number + 1
    else:
        new_number = 1  # Starting number

    # internal_demand_no = f"{current_year}{station_code}S{selected_sub_dept_code}RG8{str(new_number).zfill(5)}"
    internal_demand_no = f"{current_year}{station_code}{customer_code}G01S{str(new_number).zfill(5)}"

    print(f"Generated internal demand number: {internal_demand_no}")

    return internal_demand_no


def get_demand_data(internal_demand_number):
    int_dem_no = internal_demand_number.strip().replace('%', '')
    query_string = f'SELECT * \n FROM fob_internal_demand as d \n WHERE d.internal_demand_no = \'{int_dem_no}\' '
    result = execute_query_with_dictionary(query_string)[0]
    result = convert_date_to_str(result)
    result['demand_line'] = get_demand_line_data(internal_demand_number)
    return result


def get_demand_line_data(internal_demand_no: str) -> list:
    query_string = f"""
        SELECT l.* , i.item_desc
        FROM public.fob_internal_demand_line as l
        LEFT JOIN public.fob_item as i on i.item_code = l.item_code
        WHERE l.internal_demand_no = '{internal_demand_no}'
    """
    result = execute_query_with_dictionary(query_string)
    if len(result) == 0:
        return []
    result = [convert_date_to_str(item) for item in result]
    return result


def approve_multi_demands(demand_list: list[str], username: str):
    for item in demand_list:
        approve_demand(item, username)


def approve_demand(int_demand_no: str, username):
    try:
        query = f"""
            UPDATE public.fob_internal_demand
        SET  authorised_by= \'{username.strip()}\' , date_time_authorised= NOW()
        WHERE internal_demand_no = '{int_demand_no.strip().replace("%", "")}' ;
        """
        print(query)
        exec_query_no_result(query)
    except DBAPIError as e:
        raise BadRequestException(message=f'wrong inputs {e.args}')


def export_demand(internal_demands_list: list[str], all_flag=False) -> str:
    sess = postgres_session.get_session()
    query = f"""
            SELECT D.*, 'DEMAND' as separator, L.*, C.QTY AS cons_qty, C.APPROVED_BY AS cons_app
            FROM PUBLIC.FOB_INTERNAL_DEMAND AS D
            JOIN PUBLIC.FOB_INTERNAL_DEMAND_LINE AS L ON L.INTERNAL_DEMAND_NO = D.INTERNAL_DEMAND_NO 
            LEFT JOIN PUBLIC.FOB_INTERNAL_CONSUMPTION AS C ON C.int_consumption_no = L.int_consumption_no            
            WHERE L.mo_demand_no is null AND D.authorised_by is not null 
        """
    if not all_flag:
        where_clause = "\' , \'".join(internal_demands_list)
        query += f"""
                AND D.INTERNAL_DEMAND_NO IN (\'{where_clause}\')  
        """

    result = execute_query_with_dictionary(query)
    df = pandas.DataFrame(result)
    #TODO at the time of export don't export line items which have cons qty
    # and customer code other than duqm

    # if cons is unapproved and customer other than duqm then don't export
    df = df[(df['raised_for_customer'] == df['customer_code']) | (
            (df['raised_for_customer'] != df['customer_code']) & (df['cons_app'].notnull()))].reset_index(drop=True)

    update_demand_statement = (update(fob_internal_demand)
                               .where(
        fob_internal_demand.internal_demand_no.in_(df['internal_demand_no'].unique().tolist()))
                               .values(status_flag='EX', download_date_time=datetime.now())
                               )
    sess.execute(update_demand_statement)
    sess.commit()

    for line_item in df.itertuples(index=False):
        update_demand_statement = (update(fob_internal_demand_line)
                                   .where(fob_internal_demand_line.internal_demand_no == line_item.internal_demand_no
                                          , fob_internal_demand_line.id_line_no == line_item.id_line_no
                                          )
                                   .values(status_flag='EX', download_date_time=datetime.now())
                                   )
        sess.execute(update_demand_statement)
        sess.commit()

    csv = f'demand.csv'
    df.to_csv(csv, index=False)
    return os.path.abspath(csv)


def update_demand(internal_demand_no: str, demand, loginid: str):
    demand_details = get_demand_data(internal_demand_no)
    # if demand_details.raised_by != loginid:
    #     return

    if demand_details['authorised_by'] is None:
        # pre approval

        for item in demand["demand_line"]:
            if int(item['qty']) < 1:
                return {"message": "invalid qty"}, 400
            demand_line_query = f"""
                        UPDATE public.fob_internal_demand_line
	                        SET  qty= {item['qty']}, priority_code= \'{item['priority_code']}\',  
                            authority_ref= \'{item['authority_ref']}\', authority_date= \'{item['authority_date']}\'
	                        WHERE internal_demand_no = \'{internal_demand_no}\';
                """
            exec_query_no_result(demand_line_query)

        exec_query_no_result(f"""
            UPDATE public.fob_internal_demand
	SET    raised_for_customer= \'{demand['raised_for_customer']}\',  remarks= \'{demand['remarks']}\'
	WHERE internal_demand_no = \'{internal_demand_no}\';
        """)
    else:
        # post approval
        exec_query_no_result(f"""
            UPDATE public.fob_internal_demand
	SET closing_code= \'{demand['closing_code']}\', closed_by= \'{loginid}\'
	WHERE internal_demand_no = \'{internal_demand_no}\', date_time_closed= \'{datetime.now()}\';
        """)


def close_demand_service(internal_demand_no: str, closing_code: str, loginid: str):
    demand_details = get_demand_data(internal_demand_no)
    if demand_details['closed_by'] is not None:
        return [{"message": "invalid request, Demand already closed"}, 400]
    if demand_details['status_flag'] is None:
        status_flag = 'null'
    else:
        status_flag = '\'IM\''
    query = f"""
            UPDATE public.fob_internal_demand
	            SET  status_flag= {status_flag} , closing_code= \'{closing_code}\', closed_by= \'{loginid}\', date_time_closed= \'{datetime.now()}\'
	            WHERE internal_demand_no = \'{internal_demand_no}\';
            """
    exec_query_no_result(query)
    return [{"message": "Success"}, 200]


def get_demand_status_data(search_type: str, search_param: str):
    dem_stat_q = get_demand_status_q(search_type, search_param)
    df_data = pandas.read_sql(dem_stat_q.statement, dem_stat_q.session.bind)
    for column in df_data.columns:
        if 'time' in column or 'gate_pass_key' in column:
            df_data[column] = df_data[column].apply(format_date_postgres_timestamp)

    df_data = df_data.replace({pd.NaT: None, np.nan: None})
    return df_data.to_dict(orient="records")


def create_status_entries(temp_demand_path, customer_code:str):
    REQUIRED_COLUMNS_DEMAND = {
        'InternalDemandNo'
        , 'IDLineNo'
        , 'DemandNo'
        , 'DemandedQty'
        , 'TotalIssuedQty'
        , 'LatestIssueDateTime'
        , 'TotalReleasedQty'
        , 'LatestReleasedTime'
        , 'LatestDateTimeTakenOver'
        , 'LatestPackageDateTimeApproved'
        , 'LatestPackageDateTimeTakenOver'
        , 'LatestGatePassKey'}
    with (postgres_session.get_session() as sess):
        try:
            df = pd.read_csv(temp_demand_path)
            missing_cols = REQUIRED_COLUMNS_DEMAND - set(df.columns)
            if missing_cols:
                raise BadRequestException(f'missing required columns {missing_cols} ')
            df.rename(columns={
                'InternalDemandNo': 'internal_demand_no'
                , 'IDLineNo': 'id_line_no'
                , 'CustomerCode': 'customer_code'
                , 'DemandNo': 'demand_no'
                , 'DemandedQty': 'demanded_qty'
                , 'TotalIssuedQty': 'total_issued_qty'
                , 'LatestIssueDateTime': 'latest_issue_date_time'
                , 'TotalReleasedQty': 'total_released_qty'
                , 'LatestReleasedTime': 'latest_released_time'
                , 'LatestDateTimeTakenOver': 'latest_date_time_taken_over'
                , 'LatestPackageDateTimeApproved': 'latest_package_date_time_approved'
                , 'LatestPackageDateTimeTakenOver': 'latest_package_date_time_taken_over'
                , 'LatestGatePassKey': 'latest_gate_pass_key'
            }, inplace=True)
            print(df)

            for col in df.columns:
                if 'date' in col.lower() and col.lower().strip() not in ['latest_gate_pass_key']:
                    df[col] = pd.to_datetime(df[col], errors='coerce').dt.tz_localize(None)
            df['latest_gate_pass_key'] = pd.to_datetime(
                df['latest_gate_pass_key'].str.replace(r':(\d{1,3})$', r'.\1', regex=True), errors='coerce',
                format='%d/%m/%Y %H:%M:%S.%f')
            from dateutil.parser import parse
            df['latest_released_time'] = df['latest_released_time'].apply(
                lambda x: parse(x) if str(x) != 'nan' else None)
            # df['latest_package_date_time_taken_over'] = df['latest_package_date_time_taken_over'].apply(format_date_postgres_timestamp)
            # df['latest_package_date_time_approved'] = df['latest_package_date_time_approved'].apply(format_date_postgres_timestamp)
            # df['latest_date_time_taken_over'] = df['latest_date_time_taken_over'].apply(format_date_postgres_timestamp)
            # df['latest_released_time'] = df['latest_released_time'].apply(format_date_postgres_timestamp)
            # df['latest_issue_date_time'] = df['latest_issue_date_time'].apply(format_date_postgres_timestamp)
            print(df)
            print(df.dtypes)
            print(f'this is length of df {len(df)}')
            print(f'this is length of df dict {len(df.to_dict('records'))}')

            # df.to_sql(fob_demand_status.__tablename__, con=postgres_session.__engine__, if_exists='append', index=False,
            #           chunksize=1)
            df = df.replace({pd.NaT: None, np.nan: None})
            for item in df.to_dict(orient='records'):
                #TODO : (StatusFlagCheck) check for the closing code and if it exists then skip the insert
                if customer_code not in str(item.get('customer_code')):
                    continue
                closing_code_check = 0 < sess.query(fob_internal_demand_line).filter(
                    fob_internal_demand_line.closing_code.is_not(None),
                    fob_internal_demand_line.mo_demand_no == item.get('demand_no')).count()
                if closing_code_check:
                    continue
                if 'ClosingCode' in item.keys() and not pd.isnull(item.get('ClosingCode')):
                    continue
                with sess.begin_nested():
                    demand_s_obj = fob_demand_status(**item)
                    print(f'this is demand object {demand_s_obj.id_line_no}')
                    flag_check = 0 < sess.query(fob_demand_status).filter(fob_demand_status.demand_no == demand_s_obj.demand_no, fob_demand_status.customer_code == demand_s_obj.customer_code).count()

                    if flag_check:
                        object_demand_s = sess.query(fob_demand_status).filter(
                            fob_demand_status.demand_no == demand_s_obj.demand_no,fob_demand_status.customer_code == demand_s_obj.customer_code).one()
                        sess.delete(object_demand_s)
                        sess.flush()
                    # if check if exists
                    #     delete if exists
                    print(f'this id demand_s_obj = {demand_s_obj.latest_released_time}')
                    sess.add(demand_s_obj)
                    sess.commit()

        finally:
            # sess.commit()
            if os.path.exists(temp_demand_path):
                os.remove(temp_demand_path)


def get_demand_line_by_demand_no(int_demand_no: str) -> list[dict]:
    sess = postgres_session.get_session()
    query = sess.query(
        fob_internal_demand_line,
        func.trim(fob_item.item_desc).label("item_desc")
    ).join(
        fob_item, func.trim(fob_item.item_code) == func.trim(fob_internal_demand_line.item_code)
    ).filter(
        fob_internal_demand_line.internal_demand_no == int_demand_no
    )
    result = pd.read_sql(query.statement, query.session.bind)
    lst = result.to_dict(orient='records')
    return lst
