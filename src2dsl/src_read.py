import sqlite3
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from smartsheet import Smartsheet

import pytesseract
from PIL import Image
import re

# from tesserocr import PyTessBaseAPI

def read_csv(src_file):
    return pd.read_csv(src_file, dtype=str)

def read_sql(db_file, table_name=None):
    db_conn = sqlite3.connect(db_file)
    select_data_query = "SELECT * from %s;" % table_name
    select_type_query = "SELECT name, type from pragma_table_info(\'%s\');" % table_name
    table = pd.read_sql_query(select_data_query, db_conn, dtype=str)
    types = pd.read_sql_query(select_type_query, db_conn)
    return table, types

def read_ggs(creds_json_file, sheets_name, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json_file, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheets_name).worksheet(sheet_name)
    data = pd.DataFrame(sheet.get_all_records(), dtype=str)
    return data

def read_sst(api_token, sheet_name):
    sst_client = Smartsheet(api_token)
    sheet = sst_client.Sheets.get_sheet_by_name(sheet_name)
    titles = [col.title for col in sheet.columns]
    types = [col.type.value.name for col in sheet.columns]
    rows = []
    for row in sheet.rows:
        cells = []
        for cell in row.cells:
            cells.append(cell.value)
        rows.append(cells)

    table = pd.DataFrame(rows, columns=titles, dtype=str)
    types = pd.DataFrame([types], columns=titles, dtype=str)
    return table, types

def read_pdf(pdf_file):
    s = pytesseract.image_to_string(pdf_file, config='-c preserve_interword_spaces=1x1 --psm 1 --oem 3').strip()
    s_list = s.split('\n')
    data_list = [re.split(r" {2,}", i) for i in s_list]
    table = pd.DataFrame(data_list[1:], columns=data_list[0], dtype=str)
    return table