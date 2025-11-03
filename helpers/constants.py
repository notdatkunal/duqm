from enum import Enum
from socket import gethostname, gethostbyname

commands_list: dict = {
    'NHQ': 'Naval HeadQuarter'
    , 'WNC': 'Western Naval Command'
    , 'ENC': 'Eastern Naval Command'
    , 'SNC': 'Southern Naval Command'
    , 'ANC': 'Andaman & Nicobar Command'
}


class roles(Enum):
    auditor = 'audit'
    nlao = 'nlao'
    anlao = 'anlao'


allowed_roles = [item.value for item in roles]

ops_auth_list: dict = {
    # 'D': 'DockYard'
    # , 'G': 'General Manager Tech'
    # , 'M': 'Material Organization'
    'B': 'BVY'
}


class CustomerCodes(Enum):
    B = '1440'
    K = '2352'
    G = '2300'
    W = '2444'
    P = '2378'
    V = '2323'


class Check(Enum):
    VALID = True
    INVALID = False


PUBLIC_ENDPOINTS = ['/globals/login', '/'
    , '/swaggerui/droid-sans.css'
    , '/swaggerui/swagger-ui-standalone-preset.js'
    , '/swaggerui/swagger-ui-bundle.js'
    , '/swaggerui/swagger-ui.css'
    , '/swaggerui/favicon-32x32.png'
    , '/swaggerui/favicon-16x16.png'
    , '/swagger.json'
    , '/download'
    , '/globals/download'
    , '/globals/import'
    , '/ledger_pdf'
    , '/gatepass/pdf', '/srv/pdf/scheduling', '/ledger/reports/half-yearly/pdf',
                    '/scheduling/reports/store-receipt/pdf', '/scheduling/reports/gatepass/pdf']


def is_dev() -> bool:
    ip_address: str = gethostbyname(gethostname()).strip()
    return '160.12.158.20'.startswith(ip_address) or '160.12.158.9'.startswith(ip_address)


def fetch_origins():
    https__ = ['https://wnc-momb-audit.hq.indiannavy.mil', 'https://training.wnc-momb-audit.hq.indiannavy.mil',
               'https://160.12.152.4']
    if is_dev():
        dev_ips = ['http://160.16.1.53:5173', 'http://localhost:5050', 'http://localhost', 'https://160.16.1.53:5050',
                   'http://160.16.1.53', 'http://160.12.158.20:5050', 'http://160.12.158.20', 'http://160.12.158.9']
        https__.extend(dev_ips)
    return https__


class roles(Enum):
    auditor = 'audit'
    nlao = 'nlao'
    anlao = 'anlao'


phases = ({1: 'APR-SEPT', 2: 'OCT-MAR'})
