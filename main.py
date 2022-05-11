from src2dsl import src_read
from dsl2dest import dest_write
from mapping import *
from DSL import DSL

## Step 1. read src file

# src_format = "csv"
csv_file = "samples/csv_test.csv"

src_format = "sql"
sql_file = "samples/sql_test.db"
sql_table = "People"

if src_format == "csv":
    src_data = src_read.read_csv(csv_file)
elif src_format == "sql":
    src_data, src_type = src_read.read_sql(sql_file, sql_table)


## Step 2. regress

type_options = []

if src_format == "csv":
    for col in src_data.columns:
        type_options.append([])
        for type in map_src["csv"]["string"]:
            type_m = type()
            if type_m.regress(src_data[col]):
                type_options[-1].append(type_m)

elif src_format == "sql":
    for i in range(len(src_type)):
        type_options.append([])
        nm = src_type.loc[i, 'name']
        ty = src_type.loc[i, 'type']
        ty = ty.split('(')[0].upper()
        for type in map_src["sql"][ty]:
            type_m = type()
            if type_m.regress(src_data[nm]):
                type_options[-1].append(type_m)


## Step 3. Choose DSL types and attributes
## Step 4.1. create DSL, add types
# suppose always choose the first option
type_options = [i[0] for i in type_options]

DSL_0 = DSL(0)
DSL_0.names = list(src_data.columns)
for type_option in type_options:
    DSL_0.addField(type_option)


## Step 4.2. DSL add records (and process)
for idx, row in src_data.iterrows():
    DSL_0.addRecord(row)

## Step 5. Output in dest format
# dst_format = "csv"
csv_file = "samples/csv_test_dst.csv"

dst_format = "sql"
sql_file = "samples/sql_test_dst.db"
table_name = "Students"

if dst_format == "csv":
    dest_write.write_csv(csv_file, DSL_0)
elif dst_format == "sql":
    dest_write.write_sql(sql_file, table_name, DSL_0)

print("end")