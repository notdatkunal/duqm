from enum import Enum
from sqlalchemy import create_engine, QueuePool, MetaData, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

from fob_sybase.DBConfigs import config as database_configuration, _URLStore


class DatabaseNames(Enum):
    CSILMS: str = 'csilms'
    IVMS_AUDIT: str = 'IVMS_AUDIT'
    IVMS: str = 'ivms'
    MASTERS: str = 'masters'
    SMMS: str = 'smms'
    ILMSIMAGES: str = 'ilmsimages'


class App:
    def __init__(self, config_element: _URLStore, database_name: str):
        self.db_url = config_element.get_db_url(db_name=database_name)
        self.app_engine = create_engine(self.db_url, pool_size=20, poolclass=QueuePool, echo=True)
        # self.app_connection = self.app_engine.connect()
        self.autocommit_connection = self.app_engine.connect().execution_options(isolation_level='AUTOCOMMIT')
        self.__App_Session__ = sessionmaker(bind=self.app_engine)
        self.app_session = self.__App_Session__()
        self.app_sybase_metadata = MetaData()
        self.App_Base = declarative_base(metadata=self.app_sybase_metadata)
        # self.app_inspector = inspect(self.app_engine)
        # self.app_session.execute(text('select 1'))
        print(f'this is db url: {self.db_url}')
        print(f'{database_name} created')


class Connections:
    def __init__(self, config_element: _URLStore):
        self.__csilms = None
        # self.__ilms_images = None
        self.__ivms = None
        # self.__smms = None
        self.config_element = config_element
        self.assign_connections()

    def assign_connections(self):
        # ...
        if self.config_element is None:
            raise Exception('config element does not exist')

        # self.__ilms_images: App = App(self.config_element, DatabaseNames.ILMSIMAGES.value)
        self.__csilms: App = App(self.config_element, DatabaseNames.CSILMS.value)
        # self.__ivms: App = App(self.config_element, DatabaseNames.IVMS.value)
        # self.__smms: App = App(self.config_element, DatabaseNames.SMMS.value)

    # def reset_connection(self):
    #     self.__csilms.app_session.close()
    #     self.__ilms_images.app_session.close()
    #     self.__ivms.app_session.close()
    #     self.__smms.app_session.close()
    #     self.__csilms.app_engine.dispose()
    #     self.__ilms_images.app_engine.dispose()
    #     self.__ivms.app_engine.dispose()
    #     self.__smms.app_engine.dispose()
    #     self.assign_connections()

    def get_csilms(self) -> App:
        return self.__csilms

    # def get_ilms_images(self):
    #     return self.__ilms_images
    def get_ivms(self):
        return self.__ivms


ConnectionsElement = Connections(database_configuration)

# print('hello w')
# result = ConnectionsElement.get_ilms_images().app_session.execute(text('select 1')).all()
# result_csilms = ConnectionsElement.get_csilms().app_session.execute(text('select 1')).all()
# result = ConnectionsElement.get_csilms().app_session.execute(text('select top 3 *  from AuditLedger')).all()

# for item in result:
#     print(item)



