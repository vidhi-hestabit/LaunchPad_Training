import sqlite3

def execute_sql(db_path: str, sql: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.executescript(sql)  
        cursor.execute(sql.split(";")[0])
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
    finally:
        conn.close()

    return columns, rows
