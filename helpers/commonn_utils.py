import base64
import datetime
import json
import os
import time
from datetime import datetime, date, timedelta
from flask import request
from werkzeug.utils import secure_filename

import pandas
import pandas as pd
from sqlalchemy import inspect

from fob_sybase.Connections import ConnectionsElement
from fob_sybase.IVMS_AUDIT.tables import IVMS_Customer
from helpers.exceptions import BadRequestException


def paginate_request(server_req):
    number_of_rows_per_page: int = int(server_req.args.get('rows', default=10))
    page_number: int = int(server_req.args.get('page', default=0))
    if page_number < 0:
        page_number = 0
    return number_of_rows_per_page, page_number


def listination(data: list, page_number, items_per_page) -> list:
    if page_number == 0:
        return data
    start = (page_number - 1) * items_per_page
    end = start + items_per_page
    return data[start:end]


def format_page_number(page_number):
    page_number = page_number - 1
    if page_number < 0:
        page_number = 0
    return page_number


def file_to_base64(file):
    file_data = file.read()
    return base64.b64encode(file_data).decode('utf-8')


def get_n_digit_number(number: str, constant: int) -> str:
    size = len(str(number))
    if size > constant:
        raise ValueError('value greater than expected')
    elif size == constant:
        return number
    else:
        return get_n_digit_number('0' + number, constant)


def get_running_year():
    return str(datetime.now().year)[2:]


def get_active_phase():
    return '1' if 3 < get_active_month() < 10 else '2'


def get_active_month():
    return datetime.now().month


def get_doc_extension(file):
    return file['name'].rsplit('.', 1)[1].lower() if '.' in file['name'] else ''


def get_document_type(file):
    end = file['base64content'].index(';')
    doc_type = file['base64content'].split(':', end)[1].lower() if 'data:' in file['base64content'] else ''
    doc_type = doc_type.split(';', end)[0].lower() if ';base64' in doc_type else ''
    return doc_type


def validate_file(item):
    from helpers.exceptions import AppException
    print(item)
    document_extension = get_doc_extension(item)
    size: int = int(item['size'])
    if document_extension not in ['docs', 'docx', 'doc', 'pdf', 'xlsx', 'txt', 'jpg', 'png', 'jpeg']:
        raise AppException('file type not allowed', 401)
    if size > 200000000:
        raise AppException('not healthy amount', 401)

    pass


def extract_file_data(file_data) -> list:
    # data_type = type(file_data)
    if file_data is not None:
        if isinstance(file_data, list):
            files = file_data
        else:
            files: list = json.loads(file_data)
        [validate_file(item) for item in files]
    else:
        files = list()
    return files


def dictionify(query):
    return [item._asdict() for item in query.all()]


def get_column_names_excluding_id(table_name):
    exclude_column = 'id'
    return [c for c in inspect(table_name).c if c.name != exclude_column]


def pandas_date_time(date_string: str) -> pandas.DatetimeIndex | None:
    """
        :param date_string:
        :return:
        """
    try:
        import pandas as pd
        # return pd.to_datetime(date_string, dayfirst=True)
        return pd.to_datetime(date_string)
    except ValueError:
        print(f'Invalid date format : {date_string}')
        return None


def get_category_by_id(key):
    if int(key) in dict(categories):
        return categories[int(key)]
    raise KeyError(f"Required key with {key} not found in categories")


def get_id_by_category(category):
    for key in dict(categories):
        if category == categories[key]:
            return int(key)


categories: dict = ({
    1: 'All'
    , 2: 'Not Audited'
    , 3: 'Initiated Audits'
    , 4: 'Auditor Audits'
    , 5: 'ANLAO Audits'
})


class AuditRequest:
    def __str__(self):
        return f"AuditRequest(username={self.username},role={self.role},keys={list(string_for_composite_key(item) for item in self.keys)})"

    def __init__(self, username: str, role: str, keys):
        self.username = username
        self.role = role
        self.keys = fetch_keys(keys)


def fetch_keys(data_keys: list) -> list:
    return list(item for item in data_keys)


def extract_flag(request_obj: request, flag_name: str) -> bool:
    return 'true' == request_obj.args.get(flag_name, default='false').lower().strip()


class CompositeKey:
    def __str__(self):
        return f"CompositeKey(item_code={self.item_code},months={self.months},station_code={self.station_code},stock_serial={self.stock_serial},years={self.years})"

    def __init__(self, item_code, months, station_code, stock_serial, years):
        self.item_code = item_code
        self.months = months
        self.station_code = str(station_code)
        self.stock_serial = int(stock_serial)
        self.years = str(years)


def string_for_composite_key(comp_key: CompositeKey) -> str:
    return comp_key.__str__()


def get_financial_year_by_id(key):
    key = int(key)
    if key in financial_years:
        return financial_years[key]
    raise KeyError(f'required key with {key} not found in financial years list ')


phases = ({1: 'APR-SEPT', 2: 'OCT-MAR'})
financial_years = {1: '2023-24', 2: '2022-23', 3: '2024-25', 4: '2025-26'}


def paginate(page_number, rows, query):
    return query.limit(rows).offset(rows * page_number)


def get_path():
    from os import path
    BASE_DIR = path.dirname('C:\\file_services\\')
    return BASE_DIR


def get_file_path(file_type, obs_id):
    from os import path, makedirs
    # from audit_application.helpers.constants imports BASE_DIR
    if file_type is None:
        file_type = 'objectionDocuments'
    DOC_DIR = path.join(get_path(), f'file_storage\\ivms_objection-{obs_id}\\{file_type}')
    if not path.exists(DOC_DIR):
        makedirs(DOC_DIR)
    return DOC_DIR


class ObjectionFile:
    def __init__(self, doc_extension, doc_mime_type, file_name, file_size, file_path, objection_id):
        self.doc_extension = doc_extension
        self.doc_type = doc_mime_type
        self.file_name = file_name
        self.file_size = file_size
        self.file_path = file_path
        self.objection_id: int = int(objection_id)


def generate_year_ranges(start=2022):
    current_year = datetime.now().year
    year_range = []
    for year in range(start, current_year + 1):
        next_year_short = str(year + 1)[-2:]
        year_range.append(f"{year}-{next_year_short}")
    return year_range


YEAR_RANGES = generate_year_ranges()


def get_name_by_customer_code(customer_code):
    if customer_code is None or len(customer_code.strip()) == 0:
        return None
    customer_code__one = ConnectionsElement.get_csilms().app_session.query(IVMS_Customer.Name).filter(
        IVMS_Customer.CustomerCode.startswith(customer_code)).first()
    print(f'customer code {customer_code__one}')
    if customer_code__one is None or len(customer_code__one) == 0:
        return None
    return customer_code__one[0]


def split_list(list_obj, chunk_size: int):
    return [list_obj[int(i):int(int(i) + int(chunk_size))] for i in range(0, len(list_obj), chunk_size)]


def get_date_ranges_util(start_date: date, closing_date: date) -> list[dict[str, datetime.date]]:
    date_ranges: list[dict[str, datetime.date]] = []
    while start_date < closing_date:
        print(start_date)
        print(closing_date)
        end_date = start_date.replace(day=16)
        date_ranges.append({'from': start_date, 'to': end_date})
        start_date = start_date + timedelta(days=31)
        start_date = start_date.replace(day=1)
        date_ranges.append({'from': end_date, 'to': start_date})
    date_ranges = date_ranges[:-2]
    return date_ranges


def format_date_postgres_timestamp(date: datetime):
    if date is None or pd.isnull(date):
        return None
    return date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def model_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}



ALLOWED_EXTENSION = {'csv'}


def get_path_from_req(request):
    if 'file' not in request.files:
        raise BadRequestException('no file part in the request')
    files = request.files.getlist('file')
    if len(files) != 1:
        raise BadRequestException('Exactly one file must be uploaded')
    file = files[0]
    if file.filename == '':
        raise BadRequestException('No selected file')
    if not allowed_file(file.filename):
        raise BadRequestException('only csv file allowed')
    filename = secure_filename(file.filename)
    temp_path = os.path.join(r'\tmp', filename)
    print(f'saved in path {temp_path}')
    os.makedirs(r'\tmp', exist_ok=True)
    file.save(temp_path)
    return temp_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION
