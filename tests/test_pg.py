def test_pg8000():
    import pg8000
    global cursor
    con = pg8000.connect(user='fob_postgres'
                         , host='localhost'
                         , password='password'
                         , port='5432'
                         , database='duqm')
    cursor = con.cursor()
    cursor.execute('SELECT version();')
    print('this is hello')
    print(cursor.fetchone())
    con.close()




# def get_db_connection():
#     return connect(
#         database="duqm",
#         user="fob_postgres",
#         password="password",
#         host="127.0.0.1",
#         # host="127.0.0.1",
#         port="5432"
#     )


# conn = get_db_connection()
# cur = conn.cursor()
# cur.execute("SELECT version;")
# rowsa = cur.fetchall()
# cur.close()
# conn.close()
# print(f'this is result : {rowsa}')
