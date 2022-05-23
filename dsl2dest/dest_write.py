import csv
import sqlite3

from numpy import insert

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def write_csv(dest_file, DSL_):
    with open(dest_file, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(DSL_.getNames())
        csv_writer.writerows(DSL_.getRecords())
    return

def write_sql(dest_file, table_name, DSL_):
    conn = sqlite3.connect(dest_file)
    cursor = conn.cursor()

    drop_query = "DROP TABLE IF EXISTS %s" % table_name
    cursor.execute(drop_query)

    create_table_query = "CREATE TABLE " + table_name + " ("
    for i in range(DSL_.lenNames()):
        create_table_query += DSL_.getNames()[i] + " " + str(DSL_.getFields()[i].getDestType()) + ','
    create_table_query = create_table_query[:-1]
    create_table_query += ');'
    cursor.execute(create_table_query)

    for record in DSL_.getRecords():
        insert_query = "INSERT INTO %s VALUES %s;" % (table_name, tuple(record))
        cursor.execute(insert_query)

    conn.commit()
    cursor.close()
    return

def write_ggs(creds_json_file, sheets_name, sheet_name, DSL_):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json_file, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheets_name).worksheet(sheet_name)
    sheet.append_row(DSL_.getNames())
    for r in DSL_.getRecords():
        sheet.append_row(r)
    return