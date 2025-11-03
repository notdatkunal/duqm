import sqlite3
from fob_sqlite.sqlite_conn import conn


def create_table_gatepass():
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedulings_g (
            scheduling_no CHAR(13) PRIMARY KEY,
            updated_at CHAR(10)
            )
        ''')
        print('table created or already exists')
    except sqlite3.Error as e:
        print(f'error creating table {e}')


def insert_scheduling_gatepass(sch_no: str):
    try:
        create_table_gatepass()
        import datetime
        cursor = conn.cursor()
        v_cursor = conn.cursor()
        current_date: str = str(datetime.date.today())
        v_cursor.execute('SELECT count(*) FROM schedulings_g WHERE scheduling_no = ?', (sch_no,))
        if v_cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO schedulings_g (scheduling_no,updated_at) VALUES (?,?) ', (sch_no, current_date))
            conn.commit()
        else:
            print('scheduling already exists')
    except sqlite3.Error as e:
        print(f'Error inserting data: {e}')


def update_scheduling_gatepass(sch_no: str):
    try:
        import datetime
        cursor = conn.cursor()
        current_date: str = str(datetime.date.today())
        cursor.execute('UPDATE schedulings_g SET updated_at = ? where scheduling_no = ? ', (current_date, sch_no))
        conn.commit()
    except sqlite3.Error as e:
        print(f'Error updating data: {e}')


def pop_gatepass_sch():
    cursor = conn.cursor()
    cursor.execute('''
        SELECT scheduling_no from schedulings_g limit 16
    ''')
    result = [item[0] for item in cursor.fetchall()]
    for item in result:
        delete_gatepass_sch(item)
    return result


def delete_gatepass_sch(sch_no: str):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM schedulings_g where scheduling_no = ? ', (sch_no,))
        conn.commit()
    except sqlite3.Error as e:
        print(f'error deleting data {e} ')


def create_table_srv():
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedulings_s (
            scheduling_no CHAR(13) PRIMARY KEY,
            updated_at CHAR(10)
            )
        ''')
        print('table created or already exists')
    except sqlite3.Error as e:
        print(f'error creating table {e}')


def insert_scheduling_srv(sch_no: str):
    try:
        create_table_srv()
        import datetime
        cursor = conn.cursor()
        v_cursor = conn.cursor()
        current_date: str = str(datetime.date.today())
        v_cursor.execute('SELECT count(*) FROM schedulings_s WHERE scheduling_no = ?', (sch_no,))
        if v_cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO schedulings_s (scheduling_no,updated_at) VALUES (?,?) ', (sch_no, current_date))
            conn.commit()
        else:
            print('scheduling already exists')
    except sqlite3.Error as e:
        print(f'Error inserting data: {e}')


def update_scheduling_srv(sch_no: str):
    try:
        import datetime
        cursor = conn.cursor()
        current_date: str = str(datetime.date.today())
        cursor.execute('UPDATE schedulings_s SET updated_at = ? where scheduling_no = ? ', (current_date, sch_no))
        conn.commit()
    except sqlite3.Error as e:
        print(f'Error updating data: {e}')


def pop_srv_sch():
    cursor = conn.cursor()
    cursor.execute('''
        SELECT scheduling_no from schedulings_s limit 16
    ''')
    result = [item[0] for item in cursor.fetchall()]
    for item in result:
        delete_srv_sch(item)
    return result


def delete_srv_sch(sch_no: str):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM schedulings_s where scheduling_no = ? ', (sch_no,))
        conn.commit()
    except sqlite3.Error as e:
        print(f'error deleting data {e} ')
