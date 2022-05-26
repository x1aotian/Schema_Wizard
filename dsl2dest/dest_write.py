import csv
import sqlite3

from numpy import insert

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from smartsheet import Smartsheet, models

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
    sheet.clear()
    sheet.append_row(DSL_.getNames())
    for r in DSL_.getRecords():
        sheet.append_row(r)
    return

def write_sst(api_token, sheet_name, DSL_):
    sst_client = Smartsheet(api_token)
    sheet_spec = {}
    sheet_spec['name'] = sheet_name
    sheet_spec['columns'] = []
    titles = DSL_.getNames()
    for i in range(DSL_.lenNames()):
        if i == 0:
            sheet_spec['columns'].append({'title': titles[i], 'primary': True, 'type': str(DSL_.getFields()[i].getDestType())})
        else:
            sheet_spec['columns'].append({'title': titles[i], 'type': str(DSL_.getFields()[i].getDestType())})
    sheet_def = models.Sheet(sheet_spec)
    sheet = sst_client.Home.create_sheet(sheet_def).result
    columns = sheet.get_columns().data
    rows = []
    for r in DSL_.getRecords():
        row_ = models.Row()
        for i, d in enumerate(r):
            row_.cells.append({'column_id': columns[i].id_, 'value': d})
        row_.to_bottom=True
        rows.append(row_)
    sheet.add_rows(rows)
    return