import pyodbc

def get_connect(USERNAME, PASSWORD):
    SERVER = '192.168.1.103'
    DATABASE = 'admission'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    return connection_string

def get_admin_connection():
    connection_string = get_connect('aadmin_login','admin@123')
    connect = pyodbc.connect(connection_string)
    return connect

def get_user_connection():
    connection_string = get_connect('aguest_login','guest@456')
    connect = pyodbc.connect(connection_string)
    return connect

def get_faculties_table():
    db = get_admin_connection()

    cursor = db.cursor()

    cursor.execute("SELECT f_id,f_name FROM faculties")
    ret = {}
    for i in cursor.fetchall():
        ret[i[0]] = i[1].strip()

    cursor.close()
    db.close()
    return ret