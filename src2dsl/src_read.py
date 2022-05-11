import sqlite3
import pandas as pd

def read_csv(src_file):
    return pd.read_csv(src_file, dtype=str)

def read_sql(db_file, table_name=None):
    db_conn = sqlite3.connect(db_file)
    select_data_query = "SELECT * from %s;" % table_name
    select_type_query = "SELECT name, type from pragma_table_info(\'%s\');" % table_name
    table = pd.read_sql_query(select_data_query, db_conn, dtype=str)
    types = pd.read_sql_query(select_type_query, db_conn)
    return table, types