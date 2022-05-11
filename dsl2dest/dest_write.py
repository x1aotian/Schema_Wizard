import csv
import sqlite3

from numpy import insert

def write_csv(dest_file, DSL_):
    with open(dest_file, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(DSL_.names)
        csv_writer.writerows(DSL_.records)
    return

def write_sql(dest_file, table_name, DSL_):
    conn = sqlite3.connect(dest_file)
    cursor = conn.cursor()

    drop_query = "DROP TABLE IF EXISTS %s" % table_name
    cursor.execute(drop_query)

    create_table_query = "CREATE TABLE " + table_name + " ("
    for i in range(len(DSL_.names)):
        create_table_query += DSL_.names[i] + " " + str(DSL_.fields[i].dest_type) + ','
    create_table_query = create_table_query[:-1]
    create_table_query += ');'
    cursor.execute(create_table_query)

    for record in DSL_.records:
        insert_query = "INSERT INTO %s VALUES %s;" % (table_name, tuple(record))
        cursor.execute(insert_query)

    conn.commit()
    cursor.close()
    return