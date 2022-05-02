import sqlite3
import pandas as pd

def read_csv(src_file):
    return pd.read_csv(src_file)

def read_sql(db_file, table_name=None):
    db_conn = sqlite3.connect(db_file)
    select_str = "SELECT * from %s;" % table_name
    table = pd.read_sql_query(select_str, db_conn)
    return table
    # TODO: 1. all tables. 2. can provide tables option. 3. exception.