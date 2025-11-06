from pgserver import get_server
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def get_db_uri() -> str:
    my_data_dir = os.path.join(os.getcwd(), "data")
    db = get_server(my_data_dir)
    db_uri = db.get_uri()
    print("PostgreSQL URI:", db_uri)
    if db_uri.startswith("postgresql://"):
        db_uri = db_uri.replace("postgresql://", "postgresql+pg8000://", 1)
    return db_uri


uri = get_db_uri()

engine = create_engine(uri, echo=True)
sess = sessionmaker(engine)()

result = sess.execute(text(f'select 1')).all()
print(result)
print(f'hello world')


