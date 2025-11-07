from sqlalchemy import create_engine, QueuePool, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fob_postgres.pg_admin import init_or_get_pgserver


class __PostgresSession__:
    def __init__(self):
        self.__engine__ = create_engine(init_or_get_pgserver(), pool_size=20, poolclass=QueuePool, echo=True)
        self.__AppSession__ = sessionmaker(self.__engine__)
        self.__app_session__ = self.__AppSession__()
        self.app_sybase_metadata = MetaData()
        self.App_Base = declarative_base(metadata=self.app_sybase_metadata)

    def get_session(self) -> Session:
        return self.__app_session__


postgres_session = __PostgresSession__()
