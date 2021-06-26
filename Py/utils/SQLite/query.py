import sqlite3
from sqlite3 import Error

def start_connection(database_name):
    try:
        conn = sqlite3.connect(database_name)
        return conn
    except Error as e:
        print(f'Error: {e}')

def sql_query(database_path, cmd):
    conn = start_connection(database_path)
    if conn:
        cursorObj = conn.cursor()
        cursorObj.execute(cmd)
        if 'LIMIT 1' in cmd.upper():
            data = cursorObj.fetchone()
        else:
            data = cursorObj.fetchall()
        return data
    else:
        print('Failed to start connection...')

def sql_table_columns(database_path, table_name):
    conn = start_connection(database_path)
    if conn:
        cursorObj = conn.cursor()
        cursorObj.execute(f'pragma table_info({table_name})')
        data = cursorObj.fetchall()
        return [val[1] for val in data]
    else:
        print('Failed to start connection...')

if __name__ == '__main__':
    pass
