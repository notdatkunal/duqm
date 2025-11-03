import datetime

import pandas as pd
from typing_extensions import Type

from fob_postgres.functions import format_string_q
from fob_sybase.csilms.tables import InternalDemand, Demand, FOB_ErrorLog, FOB_InternalDemand, FOB_InternalDemandLine
from fob_sybase.Connections import ConnectionsElement
from sqlalchemy import text, Row
from sqlalchemy.exc import DBAPIError

from fob_sybase.exceptions import SybaseError


def import_data(df: pd.DataFrame):
    demand_data = {}
    demand_line_data: list = []
    print(f'length {len(df)} ')
    # print(df.head())
    print(df.keys())
    print(df)
    df['iwo_srl'] = pd.to_numeric(df['iwo_srl'], errors='coerce').fillna(0).astype(int)
    for i in range(len(df)):
        continue_flag_demand = False
        print(f'this is i range {i}')
        print(f'this is df range {df['internal_demand_no'][i]}')
        internal_demand_no = df['internal_demand_no'][i]
        sess = ConnectionsElement.get_csilms().app_session
        internal_demand_check = 0 < sess.query(FOB_InternalDemand).filter(FOB_InternalDemand.InternalDemandNo == internal_demand_no).count()
        if internal_demand_check:
            internal_demand_obj : Type[FOB_InternalDemand] = sess.query(FOB_InternalDemand).filter(
                FOB_InternalDemand.InternalDemandNo == internal_demand_no).one()
            if internal_demand_obj.ClosingCode is None and 0 < len(df['closing_code'][i]):
                internal_demand_obj.ClosingCode = df['closing_code'][i]
                sess.add(internal_demand_obj)
                sess.commit()
            continue_flag_demand = True

        internal_demand_query = None
        #TODO usually when demand is closed on duqm side then in next extract it must be updated on sybase export
        internal_demand_query = f"""
        INSERT INTO FOB_InternalDemand 
        (CustomerCode
        ,InternalDemandNo
        ,StationCode
        ,InternalDemandType
        ,RaisedForCustomer
        ,IWOSrl
        ,AuthorityType
        ,RefitNo
        ,RoleName
        ,Remarks
        ,RaisedBy
        ,DateTimeRaised
        ,AuthorisedBy
        ,DateTimeAuthorised
        ,ClosingCode
        ,ClosedBy
        ,DateTimeClosed
        ,Reason
        ,DownloadDateTime
        , MOStationCode
        ,StatusFlag) 
        VALUES('{df['customer_code'][i]}'
        ,'{df['internal_demand_no'][i]}'
        ,'{df['station_code'][i]}'
        ,'{df['internal_demand_type'][i]}'
        ,'{df['raised_for_customer'][i]}'
        ,{df['iwo_srl'][i]}
        ,'{df['authority_type'][i]}'
        ,'{df['refit_no'][i]}'
        ,'{df['role_name'][i]}'
        ,'{df['remarks'][i]}'
        ,'{df['raised_by'][i]}'
        ,'{df['date_time_raised'][i]}'
        ,'{df['authorised_by'][i]}'
        ,'{df['date_time_authorised'][i]}'
        ,'{df['closing_code'][i]}'
        ,'{df['closed_by'][i]}'
        ,'{df['date_time_closed'][i]}'
        , NULL
        ,'{df['download_date_time'][i]}'
        ,'{df['mo_station_code'][i]}'
        ,'EX')
        """
        internal_demand_query = internal_demand_query.replace('nan', '')
        if not continue_flag_demand:
            demand_data[df['internal_demand_no'][i]] = internal_demand_query

        internal_demand_line_check = 0 < sess.query(FOB_InternalDemandLine).filter(
            FOB_InternalDemandLine.InternalDemandNo == internal_demand_no
            , FOB_InternalDemandLine.IDLineNo == int(df['id_line_no'][i])
        ).count()
        if internal_demand_line_check:
            continue
        # checks for demand line
        if 0 == df['cons_qty'][i] and df['customer_code'][i] != df['raised_for_customer'][i]:
            continue
        if df['customer_code'][i] != df['raised_for_customer'][i] and pd.isnull(df.at[i, 'int_consumption_no']):
            continue
        # only one closing code column is there instead two were expected
        # if df['customer_code'][i] != df['raised_for_customer'][i] and pd.isnull(df.at[i, 'closing_code']):
        #     continue
        #TODO date time closed and closing code is not being inserted because of trigger
        fob_internal_demand_line_q = f"""

            INSERT INTO FOB_InternalDemandLine(CustomerCode, InternalDemandNo
                , IDLineNo
                , ItemCode
                , NONMOItemCode
                , Qty
                , PriorityCode
                , EqptItemCode
                , AuthorityRef
                , AuthorityDate
                , IDLActionType
                , StationCode
                , ActionBy
                , DateTimeAction
                , ActionRemarks
                , Reason
                , DownloadDateTime
                , StatusFlag
                , MODemandNo
                , ConsQty
                )
                VALUES ( '{df['customer_code'][i]}'
                , '{df['internal_demand_no'][i]}'
                , {df['id_line_no'][i]}
                , '{df['item_code'][i]}' 
                , '{df['nonmo_item_code'][i]}' 
                , {df['qty'][i]}
                , '{df['priority_code'][i]}' 
                , '{df['eqpt_item_code'][i]}'  
                , '{df['authority_ref'][i]}'  
                , '{df['authority_date'][i]}'  
                , '{df['idl_action_type'][i]}'  
                , '{df['station_code'][i]}'  
                , '{df['action_by'][i]}'  
                , '{df['date_time_action'][i]}'  
                , '{df['action_remarks'][i]}'
                , '{df['reason'][i]}' 
                , '{df['download_date_time'][i]}'  
                , 'EX'
                , '{df['mo_demand_no'][i]}'
                , {df['cons_qty'][i]}
                );
            """
        demand_line_data.append(fob_internal_demand_line_q)

    print(f'this is all keys {demand_data.keys()}')
    for key_int_dem_no, sq_query in demand_data.items():
        print(key_int_dem_no)
        #TODO here insert make sure that only unique data is inserted into table internal demand
        try:
            sq_query = format_string_q(sq_query)
            ConnectionsElement.get_csilms().app_session.execute(text(sq_query))
            ConnectionsElement.get_csilms().app_session.commit()
        except DBAPIError as e:
            print(f'exception while inserting FOB_InternalDemand {e.args}')
            ConnectionsElement.get_csilms().app_session.commit()
    for demand_line_q in demand_line_data:
        try:
            demand_line_q = format_string_q(demand_line_q)
            print(demand_line_q)
            ConnectionsElement.get_csilms().app_session.execute(text('SET CHAINED OFF'))
            ConnectionsElement.get_csilms().app_session.execute(text(demand_line_q))
            ConnectionsElement.get_csilms().app_session.commit()
            ConnectionsElement.get_csilms().app_session.execute(text('SET CHAINED ON'))
        except DBAPIError as e:
            print(f'Exception while inserting FOB_InternalDemandLine {e.args}')
            ConnectionsElement.get_csilms().app_session.commit()

    call_procedure()
    # print('demand_data has been completely inserted')


def create_demand_no(customer_code: str, mo_station_code: str) -> str:
    demand_no_call = f""" 
        Declare @DemandNo char(7)
        exec sp_DemandNo \'{customer_code}\',\'{mo_station_code}\',@DemandNo output
        SELECT @DemandNo as DemandNo 
    """
    # ConnectionsElement.get_csilms().app_session.execute(text('SET CHAINED OFF'))
    # result_q = ConnectionsElement.get_csilms().app_session.execute(text(demand_no_call),execution_options={'autocommit':True})
    result_q = ConnectionsElement.get_csilms().autocommit_connection.execute(text(demand_no_call))
    return result_q.first().DemandNo


def call_procedure():
    app_session = ConnectionsElement.get_csilms().app_session
    try:
        procedure_query = """
                
                    select a.CustomerCode,a.InternalDemandNo,a.StationCode,a.RaisedForCustomer,a.AuthorityType,a.RefitNo,a.DateTimeRaised,
            b.IDLineNo,b.ItemCode,b.Qty,b.PriorityCode,b.EqptItemCode,b.AuthorityRef,b.AuthorityDate,b.StatusFlag,a.AuthorisedBy,a.MOStationCode 
            from FOB_InternalDemand a
            join FOB_InternalDemandLine b on
            a.InternalDemandNo=b.InternalDemandNo and
            a.CustomerCode=b.CustomerCode 
            where b.StatusFlag = 'EX' 
            and b.MODemandNo is Null
            and a.Reason is Null
            and a.CustomerCode = a.RaisedForCustomer
            and a.ClosedBy is not NULL
        
                """
        # for reference
        keys = ['CustomerCode', 'InternalDemandNo', 'StationCode', 'RaisedForCustomer', 'AuthorityType', 'RefitNo',
                'DateTimeRaised', 'IDLineNo', 'ItemCode', 'Qty', 'PriorityCode', 'EqptItemCode', 'AuthorityRef',
                'AuthorityDate', 'StatusFlag', 'AuthorisedBy', 'MOStationCode']
        result_q = app_session.execute(text(procedure_query))
        for item in result_q.all():
            try:
                app_session.rollback()
                demand: Demand = create_demand(item)
                app_session.add(demand)
                app_session.commit()
                fob_demand_int: Type[FOB_InternalDemand] = app_session.query(FOB_InternalDemand).filter(FOB_InternalDemand.InternalDemandNo == item.InternalDemandNo).first()
                fob_demand_int.DateTimeUpdated = datetime.datetime.now()
                fob_demand_int.StatusFlag = 'IM'
                app_session.commit()
                if fob_demand_int:
                    query_demand_line: Type[FOB_InternalDemandLine] = app_session.query(FOB_InternalDemandLine).filter(FOB_InternalDemandLine.InternalDemandNo == item.InternalDemandNo, FOB_InternalDemandLine.IDLineNo == item.IDLineNo).one()
                    if query_demand_line:
                        query_demand_line.MODemandNo = demand.DemandNo
                        query_demand_line.StatusFlag = 'IM'
                        app_session.commit()
            except SybaseError as error_sy:
                error_obj = create_error_object(error_sy, item)
                print(error_obj)
                app_session.add(error_obj)
                app_session.commit()
            except DBAPIError as e:
                print(f'this is error code {e.args}')
                app_session.rollback()

                error_obj: FOB_ErrorLog = FOB_ErrorLog()
                error_obj.ErrorCode = 68814
                error_obj.Remarks = f'IDLineNo={item.IDLineNo};InternalDemandNo={item.InternalDemandNo}error={e.args}'
                error_obj.DateTimeLogged = datetime.datetime.now()
                error_obj.TableName = 'FOB_InternalDemand'
                error_obj.PrimaryKeyValue = item.InternalDemandNo
                app_session.add(error_obj)
                app_session.commit()

    except DBAPIError as e:
        app_session.rollback()
        print(f'{e.orig}')
        print(f'exception in procedure call {e.args}')


def create_error_object(error_sy: SybaseError, item):
    error_obj: FOB_ErrorLog = FOB_ErrorLog()
    error_obj.ErrorCode = error_sy.code
    error_obj.Remarks = f'IDLineNo={item.IDLineNo};InternalDemandNo={item.InternalDemandNo}error={error_sy.message}'
    error_obj.DateTimeLogged = datetime.datetime.now()
    error_obj.TableName = 'FOB_InternalDemand'
    # error_obj.StatusFlag = item.StatusFlag
    error_obj.PrimaryKeyValue = item.InternalDemandNo
    return error_obj


def create_demand(item) -> Demand:
    demand = Demand()
    demand.VettedBy = None
    demand.StationCode = item.MOStationCode
    no_demand = create_demand_no(item.CustomerCode, item.MOStationCode)
    demand.RemarksVetting = None
    demand.DateVetted = None
    demand.UrgencyRef = item.RefitNo
    demand.DateTimeClosed = None
    demand.ClosingCode = None
    demand.PersonalNo = item.AuthorisedBy
    demand.AuthorityDate = item.AuthorityDate
    demand.AuthorityRef = item.AuthorityRef
    demand.AuthorityType = item.AuthorityType
    demand.EqptItemCode = item.EqptItemCode
    from datetime import timedelta
    demand.DTRB = datetime.datetime.now() + timedelta(days=1)
    demand.Qty = item.Qty
    demand.ItemCode = item.ItemCode.strip()
    demand.DateTimeRegistered = datetime.datetime.now()
    demand.DateRaised = item.DateTimeRaised
    demand.PriorityCode = item.PriorityCode
    demand.CustomerCode = item.CustomerCode
    demand.DemandNo = no_demand
    return demand
