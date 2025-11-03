from sqlite3 import connect

import sqlalchemy
from sqlalchemy.orm import sessionmaker,declarative_base

# conn = connect('schedulings.db')
engine = sqlalchemy.create_engine('sqlite:///hello.sqlite')
SQLITE_SESSION = sessionmaker(engine)
sqlite_session = SQLITE_SESSION()
sqlite_md = sqlalchemy.MetaData()
# SQLITE_BASE = declarative_base(sqlite_md)
