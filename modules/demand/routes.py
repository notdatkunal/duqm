import ast
from flask import request, jsonify
from flask_restx import Resource, Namespace
from sqlalchemy import text

from helpers.commonn_utils import get_path_from_req
from helpers.exceptions import BadRequestException
from modules.demand.services import create_internal_demand_unique_key, get_demand_data, approve_multi_demands, \
    export_demand
from modules.demand import services
from fob_postgres.functions import get_postgres_con, execute_query_with_dictionary
from datetime import datetime

demand_ns = Namespace('demand', description='duqm demand api')


@demand_ns.route('/status')
class DemandStatus(Resource):
    @demand_ns.param('type', description="""
    there are two type allowed here
    type 1 : mo_demand
    type 2 : internal_demand
    """)
    @demand_ns.param('param', description="""
    this must have data of the content required for search
    """)
    def get(self):
        """
        API for Demand Status data
        """
        search_type: str = request.args.get('type')
        search_param: str = request.args.get('param')
        service_res = services.get_demand_status_data(search_type, search_param)
        return jsonify({'result': service_res})

    def post(self):
        """
        API for import demand status csv
        """
        temp_demand_path: str = get_path_from_req(request)
        customer_code: str = request.form.get('customer_code')
        services.create_status_entries(temp_demand_path, customer_code)
        return jsonify({'response': 'done'})


@demand_ns.route('/items')
class Items(Resource):

    # @global_ns.param(name='station')
    def get(self):
        """
        nr - non russian
        rs - russian
        naval - for naval
        stationcode -
        Returns
        -------

        """
        authority_type = request.args.get('authority_type')
        search_by_item_code = str(request.args.get('search_by_item_code'))
        search_by_description = request.args.get('search_by_description')
        inventory_type = request.args.get('inventory_type')
        stationcode = request.args.get("stationcode")
        if stationcode is None or len(stationcode) != 1:
            return {"message": "stationcode is required or is invalid"}, 400

        print("search_by_item_code", search_by_item_code)

        if inventory_type.lower() == 'nr':
            filter_search_by_inventory_type = f" AND (i.item_code ILIKE 'E%' or i.item_code ILIKE 'K%' or i.item_code ILIKE 'V%') "
        elif inventory_type.lower() == 'rs':
            filter_search_by_inventory_type = f" AND (i.item_code ILIKE 'S%' or i.item_code ILIKE 'G%') "
        elif inventory_type.lower() == 'naval':
            filter_search_by_inventory_type = f" AND i.item_code ILIKE 'N%' "
        else:
            filter_search_by_inventory_type = " AND i.item_code NOT LIKE 'C%' "

        # TODO: we have to take the value as my stock from db

        if search_by_item_code:
            filter_search_by_item_code = f" AND i.item_code ILIKE '%{search_by_item_code}%' "
        else:
            filter_search_by_item_code = ""

        if search_by_description:
            filter_search_by_description = f" AND i.item_desc ILIKE '%{search_by_description}%' "
        else:
            filter_search_by_description = ""

        stationcode_filter = f" l.station_code = \'{stationcode}\' "
        if authority_type == 'REP':
            filter_authority = " AND i.crp_category = 'C' "
        else:
            filter_authority = " AND i.crp_category in ('R','P') "
            pass

        query = f"""
            SELECT
            TRIM(i.item_code),
            i.item_desc as description,
            i.item_deno as deno,
            i.crp_category as crp,
            (select sum(qty) from fob_internal_stock where item_code = i.item_code) as logo_stock
            FROM
            fob_item i
            join fob_item_line l on TRIM(i.item_code) = TRIM(l.item_code) and  l.station_code = \'{stationcode}\'
            WHERE 
            """ + stationcode_filter + filter_authority + filter_search_by_item_code + \
                filter_search_by_description + filter_search_by_inventory_type

        conn = get_postgres_con()
        result = conn.execute(text(query))
        results = result.fetchall()
        if not result:
            return []
        print('results ', result)
        column_names = ['item_code',
                        'description',
                        'deno',
                        'crp',
                        'logo_stock'
                        # 'price',
                        # 'dept_stock',
                        # 'allowance'
                        ]

        items_data = [dict(zip(column_names, row)) for row in results]

        return jsonify(items_data)


@demand_ns.route('/demand')
# @demand_ns.doc(security='Bearer Auth')
class DemandRoute(Resource):
    def post(self):
        """
        Returns
        -------
        example
        demand_qty_item_list
        """

        inventory_type = request.form.get('inventory_type')
        print("inventory_type", inventory_type)

        customer_code = request.form.get('customer_code')
        station_code = str(request.form.get('station_code')).replace("\"", "")
        print(f'station code {station_code}')
        authority_type = request.form.get('authority_type')
        remarks = request.form.get('remarks')
        user_id = request.form.get('user_id')
        raised_for_customer = request.form.get('raised_for_customer')
        role_name = request.form.get('role_name')
        mo_station_code = request.form.get('mo_station_code')
        date_time_raised = datetime.now()
        formatted_date_time_raised = date_time_raised.strftime('%Y-%m-%d %H:%M:%S')
        priority = request.form.get('priority')
        demand_qty_item_list = ast.literal_eval(request.form.get('demand_qty_item_list'))

        conn = get_postgres_con()

        # in case raised for customer the 'S' in demand number should be replaced with E
        internal_demand_no = create_internal_demand_unique_key(station_code, customer_code)
        print("here after deno")

        i_query = f'''
                        INSERT INTO fob_internal_demand(
                                    customer_code, internal_demand_no, station_code, internal_demand_type,
                                    raised_for_customer, iwo_srl, authority_type, refit_no, role_name, remarks, raised_by, date_time_raised, 
                                      mo_station_code) 
                        VALUES ( \'{customer_code}\', \'{internal_demand_no}\', \'{station_code}\', \'{'MOI'}\',
            \'{raised_for_customer}\', null, \'{authority_type}\', null , \'{role_name}\', 
            \'{remarks}\', \'{user_id}\', \'{formatted_date_time_raised}\', \'{mo_station_code}\')
                '''
        print(i_query)
        conn.execute(text(i_query))

        for i, dqil in enumerate(demand_qty_item_list, start=1):
            str_index = str(i)
            i_query = f'''
                            INSERT INTO fob_internal_demand_line(
                               customer_code, internal_demand_no, id_line_no, 
                               item_code, nonmo_item_code, qty, priority_code, 
                         authority_ref, authority_date, idl_action_type,  
                        station_code, action_by, date_time_action) 
                            VALUES ( \'{customer_code}\', \'{internal_demand_no}\', \'{str_index}\', 
                            \'{dqil['item_code']}\', null, {dqil['qty']}, \'{priority}\',
                             \'{dqil['authority_ref']}\', 
                            \'{dqil['authority_date']}\', \'{'GND'}\', \'{station_code}\', null, null)
                        '''
            conn.execute(text(i_query))

            print("Data Inserted in Internal Demand Line Table")

        print("Delete data from temp Internal Cart Table")
        conn.commit()

        conn.close()

        return jsonify({"status": "done", 'internal_demand_no': internal_demand_no})


@demand_ns.route('/<internal_demand_number>')
class DemandDetails(Resource):
    def get(self, internal_demand_number):
        """
        API for demand details
        example : 25BS1515RG800007
        Parameters
        ----------
        internal_demand_number

        Returns
        -------

        """
        result = get_demand_data(internal_demand_number)
        return result

    def put(self, internal_demand_number):
        """
        Update demand details
        example : 25BS1515RG800007
        """
        if len(internal_demand_number) != 16:
            return jsonify({"message": "Invalid internal demand no"}), 400
        demand = request.get_json().get("demand")
        loginid = request.get_json().get("loginid")
        services.update_demand(internal_demand_number, demand, loginid)
        return True


@demand_ns.route('/list')
class DemandList(Resource):
    def post(self):
        """
        expected data
        {
        "int_demand_list":[]
        }
        Returns
        -------

        """
        demand_list = request.get_json().get('int_demand_list')
        return jsonify({'path': export_demand(demand_list)})

    def put(self):
        """
        API for approval of internal demands

        -------------------------
        expected data
        -------------------------
        {
            "int_demand_list" : ["25BS1515RG800007","25BS1515RG800008"]
            "username" : "username"
        }


        """
        username = request.get_json().get('username')
        int_demand_list = request.get_json().get('int_demand_list')
        approve_multi_demands(demand_list=int_demand_list, username=username)
        return jsonify({'status': 'approved'})

    @demand_ns.param('internal_demand_no', default='23BSE004RG000002', description='input for internal demand number')
    @demand_ns.param('from_date', description='input for from date')
    @demand_ns.param('to_date', default='', description='input for to date')
    @demand_ns.param('rows', default='10', description='number of rows')
    @demand_ns.param('page', default='1', description='page number')
    def get(self):
        """
        Fetch and Filter Internal Demand list
        query params 
        `int_demand_no`
         `from_date` 
        `status_flag` ("EX",)
        `authorized` (true,false)
        `closed` (true,false)
        `to_date`
        `page` (starting from 1)
        `for_forward` (null,true,false)
        -------

        """
        int_demand_no = request.args.get('internal_demand_no')
        from_date = request.args.get('from_date')
        status_flag = request.args.get('status_flag')
        authorized = request.args.get('authorized')
        closed = request.args.get('closed')
        to_date = request.args.get('to_date')
        for_forward = request.args.get('for_forward')
        limit: int = int(request.args.get('rows', default='10').replace('%', ''))
        page: int = int(request.args.get('page', default='0').replace('%', '')) - 1
        page = 0 if page < 0 else page
        pagination = f'LIMIT {limit} OFFSET {page} '

        where = ""

        if int_demand_no is not None:
            where += f" and internal_demand_no ILIKE \'{int_demand_no}%\' "
        if from_date is not None and from_date != "":
            where += f" and date_time_raised >= \'{from_date}\'"

        if to_date is not None and to_date != "":
            where += f" and date_time_raised < \'{to_date}\'"

        if status_flag is not None:
            if status_flag == "EX":
                where += f" and status_flag = \'{status_flag}\'"
            elif status_flag == 'false':
                where += f" and (status_flag is null or status_flag = 'IM')"
            else:
                where += " and status_flag is not null"

        if authorized is not None:
            if authorized == 'true':
                where += " and date_time_authorised is not null"
            else:
                where += " and date_time_authorised is null"

        if closed is not None:
            if closed == 'true':
                where += " and date_time_closed is not null"
            elif closed == 'false':
                where += " and true "
            else:
                where += " and date_time_closed is null "

        if for_forward is not None:
            if for_forward == 'true':
                where += " and raised_for_customer = customer_code"

        query_string = 'SELECT * \n FROM fob_internal_demand \n'
        if len(where) > 2:
            where = where.replace("and", "", 1)
            where = f"where {where}"
        query_string = query_string + where

        query_string += ' ORDER BY fob_internal_demand.date_time_raised DESC '
        query_string += pagination
        print(f"\n{query_string}\n")
        result = {'InternalDemandList': execute_query_with_dictionary(query_string)}
        return jsonify(result)


@demand_ns.route('/list/count')
class DemandListCount(Resource):
    @demand_ns.param('internal_demand_no', default='', description='input for internal demand number')
    @demand_ns.param('from_date', default='', description='input for from date')
    @demand_ns.param('to_date', default='', description='input for to date')
    def get(self):
        """

        Returns
        -------

        """
        int_demand_no = request.args.get('internal_demand_no')
        from_date = request.args.get('from_date')
        status_flag = request.args.get('status_flag')
        authorized = request.args.get('authorized')
        closed = request.args.get('closed')
        to_date = request.args.get('to_date')
        where = ""
        if int_demand_no is not None:
            where += f" and internal_demand_no ILIKE \'{int_demand_no}%\' "
        if from_date is not None and from_date != "":
            where += f" and date_time_raised >= \'{from_date}\'"

        if to_date is not None and to_date != "":
            where += f" and date_time_raised < \'{to_date}\'"

        if status_flag is not None:
            if status_flag == "EX":
                where += f" and status_flag = \'{status_flag}\'"
            else:
                where += " and status_flag is null"
        if authorized is not None:
            if authorized == 'true':
                where += " and date_time_authorised is not null"
            else:
                where += " and date_time_authorised is null"

        if closed is not None:
            if closed == 'true':
                where += " and date_time_closed is not null"
            else:
                where += " and date_time_closed is null"

        query = 'select count(*) from fob_internal_demand '
        if len(where) > 2:
            where = where.replace("and", "", 1)
            where = f"where {where}"
        query_string = query + where
        result = {'InternalDemandList': execute_query_with_dictionary(query_string)}
        return jsonify(result)


@demand_ns.route('/close/<internal_demand_number>')
class CloseDemand(Resource):
    def post(self, internal_demand_number):
        """
            Close Demand post request
            query param `closing_code` , `loginid`

        """
        closing_code = request.args.get('closing_code')
        if closing_code is None or len(closing_code) != 1:
            return {"message": "closing_code is required query params or is invalid"}, 400
        loginid = request.args.get("loginid")
        if loginid is None:
            return {"message": "loginid is required query params or is invalid"}, 400
        result = services.close_demand_service(internal_demand_number, closing_code, loginid)
        print("result ", result)
        c = jsonify(result[0])
        c.status = result[1]
        return c


# get_demand_line_by_demand_no

@demand_ns.route('/line/<int_demand_no>')
class DemandLineByDemandNo(Resource):
    def get(self, int_demand_no):
        if int_demand_no is None or len(int_demand_no) != 16:
            return jsonify({"message": "invalid int_demand_no"}), 400
        result = services.get_demand_line_by_demand_no(int_demand_no)
        return jsonify(result)
