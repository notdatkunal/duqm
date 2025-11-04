from fob_postgres.pg_session import postgres_session
from fob_postgres.tables import fob_item_line
#
fob_item_line.__table__.create(postgres_session.__engine__)
print('created table')
