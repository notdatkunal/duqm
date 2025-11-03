from _socket import gethostname, gethostbyname


def is_dev() -> bool:
    ip_address: str = gethostbyname(gethostname()).strip()
    return '160.12.158.20'.startswith(ip_address) or '160.12.158.9'.startswith(ip_address)


class Credentials:
    username: str = None
    port_number: int = None
    host_name: str = None
    server: str = None
    password: str = None


class _HPUNIXCredentials(Credentials):
    def __init__(self):
        print(f'HPUNIX server is running')

    username = 'sa'
    port_number = 8082
    host_name = '0.0.0.0'
    server = '160.16.2.175'
    password = 'password'


class _Dev13Credentials(Credentials):
    def __init__(self):
        print(f'DEV server is running')

    # username = 'auditdba'
    username = 'mlcadmin'
    # username = 'dbab'
    port_number = 8082
    host_name = '0.0.0.0'
    server = '160.12.152.13'
    # server = '160.12.152.10'
    password = 'password'
    # password = 'Tarahb@#$2025luj'


class _LiveCredential(Credentials):
    def __init__(self):
        print(f'Live server is running')

    port_number = 8082
    host_name = '0.0.0.0'
    username = 'auditdba'
    password = 'Password1'
    server = '160.12.152.1'


class _Dev10DatabaseServer(Credentials):
    def __init__(self):
        print(f'development 10 server is running')

    port_number = 8082
    host_name = '0.0.0.0'
    username = 'auditdba'
    password = 'password'
    server = '160.12.152.10'


class _URLStore:

    def get_db_url(self, db_name=None):
        return f'sybase+pyodbc://{self.cred.username}:{self.cred.password}@{self.cred.server}/{db_name}?driver=Adaptive Server Enterprise&port=5000'

    def get_validated_url(self, user_name: str, pass_word: str):
        # return f'DRIVER=Adaptive Server Enterprise;SERVER={self.server};DATABASE=csilms;UID={user_name};PWD={pass_word};PORT=5000;pwdialog=0;PacketSize=1024;Host=\'{gethostbyname(gethostname()).strip()}-2024.09.01\';PacketSize=1024;AppName=\'^1513cS:Lm$u*Gr@4e01042301\';'
        return f'DRIVER=Adaptive Server Enterprise;SERVER={self.cred.server};DATABASE=csilms;UID={user_name};PWD={pass_word};PORT=5000;Host=\'{gethostbyname(gethostname()).strip()}-2024.09.01\';'

    def __init__(self, username: str, password: str,
                 server: str, cred: Credentials):
        self.username = username
        self.password = password
        self.server = server
        self.cred = cred


def __get_env(env: Credentials = None) -> _URLStore:
    if env is None:
        env = _Dev13Credentials()
        # env = _LiveCredential()
        # env = _HPUNIXCredentials()
        # env = _Dev10DatabaseServer()
    return _URLStore(username=env.username, password=env.password, server=env.server, cred=env)


config: _URLStore = __get_env()
# config: _URLStore = __get_env() if is_dev() else __get_env(_LiveCredential())
