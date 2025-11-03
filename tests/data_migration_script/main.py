import pandas as pd
from sqlalchemy import text

from fob_postgres.pg_session import postgres_session
from migration_utils import convert_date_cell


def import_internal_customer_user():
    df = pd.read_csv(r'internal_customer_user.csv')
    print(df.keys())
    master_query_string = ""
    for i in range(len(df)):
        query = f"""
                INSERT INTO public.fob_internal_customer_user(
                login_id, role_name, customer_code, date_time_added, added_by, date_time_closed, closed_by)
                VALUES ('{df['LoginId'][i]}', '{df['RoleName'][i]}', '{df['CustomerCode'][i]}', NOW(), '{df['AddedBy'][i]}', {convert_date_cell(df['DateTimeClosed'][i])}, '{df['ClosedBy'][i]}');
            """
        query = format_string_q(query)
        print(query)
        postgres_session.get_session().execute(text(query))
        postgres_session.get_session().commit()


def import_project():
    df = pd.read_csv(r'project.csv')
    print(df.keys())
    master_query_string = ""
    for i in range(len(df)):
        query = f"""
        INSERT INTO public.fob_project(
            project_code, name, country_code, project_date, project_cost_rs, no_of_ships, class_type, date_time_added, added_by)
            VALUES ('{df['ProjectCode'][i]}', '{df['Name'][i]}', '{df['CountryCode'][i]}', {convert_date_cell(df['ProjectDate'][i])}, '{df['ProjectCostRs'][i]}', '{df['NoOfShips'][i]}', '{df['ClassType'][i]}', {convert_date_cell(df['DateTimeAdded'][i])}, '{df['AddedBy'][i]}')
            ;
        """
        query = format_string_q(query)
        print(query)
        postgres_session.get_session().execute(text(query))
        postgres_session.get_session().commit()





def import_ship_class():
    df = pd.read_csv(r'ship_class.csv')
    print(df.keys())
    master_query_string = ""
    for i in range(len(df)):
        query = f"""
        INSERT INTO public.fob_ship_class(
        class_name, class_type, project_code)
        VALUES ('{df['ClassName'][i]}', '{df['ClassType'][i]}', '{df['ProjectCode'][i]}');

        """
        query = format_string_q(query)
        print(query)
        postgres_session.get_session().execute(text(query))
        postgres_session.get_session().commit()


def import_customer():
    df = pd.read_csv(r'customer.csv')
    print(df.keys())
    master_query_string = ""
    for i in range(len(df)):
        query = f"""
                INSERT INTO public.fob_customer(
            customer_code
            , name
            , customer_type
            , mother_depot
            , addressee
            , address_line1
            , address_line2
            , address_line3
            , city
            , state
            , pin_code
            , allowance_annual_rs
            , date_introduced
            , date_closed
            , remarks
            , admin_authority
            , station_code
            , added_by
            , closed_by
            , download_date_time
            , status_flag)
            VALUES (
              '{df['CustomerCode'][i]}'
            , '{df['Name'][i]}'
            , '{df['CustomerType'][i]}'
            , '{df['MotherDepot'][i]}'
            , '{df['Addressee'][i]}'
            , '{df['AddressLine1'][i]}'
            , '{df['AddressLine2'][i]}'
            , '{df['AddressLine3'][i]}'
            , '{df['City'][i]}'
            , '{df['State'][i]}'
            , '{df['PINCode'][i]}'
            , '{df['AllowanceAnnualRs'][i]}'
            , {convert_date_cell(df['DateIntroduced'][i])}
            , {convert_date_cell(df['DateClosed'][i])}
            , '{df['Remarks'][i]}'
            , '{df['AdminAuthority'][i]}'
            , '{df['StationCode'][i]}'
            , '{df['AddedBy'][i]}'
            , '{df['ClosedBy'][i]}'
            , null
            , null
            )
        ON CONFLICT (customer_code) DO NOTHING;
            

            """
        query = format_string_q(query)
        # postgres_session.get_session().execute(text(query))
        # postgres_session.get_session().commit()
        # from threading import main_thread
        # main_thread().
        master_query_string+=query
    with open('fob_customer.sql', 'w') as file:
        file.write(master_query_string)
        print('----------------------')
        print('fob_customer data exported')
        print('----------------------')



def import_ship():
    df = pd.read_csv(r'ship.csv')
    master_query_string = ""
    for i in range(len(df)):
        query = f"""
            INSERT INTO public.fob_ship(
        customer_code, date_commissioning, date_decommissioning, project_code, yard_no, pennant_no, baseport_change_date, base_port_change_authority_ref, base_port_change_authority_date, date_time_added, added_by)
        VALUES ('{df['CustomerCode'][i]}', {convert_date_cell(df['DateCommissioning'][i])}, {convert_date_cell(df['DateDecommissioning'][i])}, '{df['ProjectCode'][i]}', '{df['YardNo'][i]}', '{df['PennantNo'][i]}', '{df['BasePortChangeDate'][i]}', '{df['BasePortChangeAuthorityRef'][i]}', '{df['BasePortChangeAuthorityDate'][i]}', {convert_date_cell(df['DateTimeAdded'][i])}, '{df['AddedBy'][i]}');
            """
        query = format_string_q(query)
        master_query_string += query
    # print(master_query_string)
    with open('fob_ship.sql', 'w') as file:
        file.write(master_query_string)
        print('----------------------')
        print('fob_ship data exported')
        print('----------------------')


def format_string_q(query: str) -> str:
    query = query.replace('\'nan\'', 'null')
    query = query.replace('\'NaT\'', 'null')
    return query


def main():
    # import_ship()
    # import_project()
    # import_ship_class()
    # import_customer()
    # import_internal_customer_user()
    ...


if __name__ == '__main__':
    main()
