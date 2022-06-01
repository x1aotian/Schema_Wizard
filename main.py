from src2dsl import src_read
from dsl2dest import dest_write
from mapping import *
from DSL import DSL

## Step 1. read src file

# src_format = "csv"
csv_file = "samples/csv_test.csv"

# src_format = "sql"
sql_file = "samples/sql_test.db"
sql_table = "People"

# src_format = "ggs"
creds_json_file = "samples/creds_wizard.json"
sheets_name = "schema_sample"
sheet_name_ggs = "Read"

# src_format = "sst"
api_token_sst = "hGxVYnqxHE3K4OpZufvauB4eUbLGLmH1IpNkn"
sheet_name_sst = "Read"

src_format = "pdf"
pdf_file = "samples/pdf_test.jpg"

if src_format == "csv":
    src_data = src_read.read_csv(csv_file)
elif src_format == "sql":
    src_data, src_type = src_read.read_sql(sql_file, sql_table)
elif src_format == "ggs":
    src_data = src_read.read_ggs(creds_json_file, sheets_name, sheet_name_ggs)
elif src_format == "sst":
    src_data, src_type = src_read.read_sst(api_token_sst, sheet_name_sst)
elif src_format == "pdf":
    src_data = src_read.read_pdf(pdf_file)

## Step 2. regress

type_options = []

if src_format in ["csv", "ggs", "csv"]:
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

elif src_format == "sst":
    for i in range(len(src_type.columns)):
        type_options.append([])
        for type in map_src["sst"][src_type.iloc[0, i]]:
            type_m = type()
            if type_m.regress(src_data.iloc[:, i]):
                type_options[-1].append(type_m)


## Step 3. Choose DSL types and attributes
## Step 4.1. create DSL, add types
# suppose always choose the first option
type_options = [i[0] for i in type_options]

DSL_0 = DSL(0)
DSL_0.setNames(list(src_data.columns))
for type_option in type_options:
    DSL_0.addField(type_option)


## Step 4.2. DSL add records (and process)
for idx, row in src_data.iterrows():
    DSL_0.addRecord(row)

## Step 5. Output in dest format
# dest_format = "csv"
csv_file = "samples/csv_test_dst.csv"

# dest_format = "csv"
sql_file = "samples/sql_test_dst.db"
table_name = "Students"

# dest_format = "ggs"
sheet_name_ggs = "Write"

dest_format = "sst"
sheet_name_sst = "Write"

for field in DSL_0.getFields():
    field.transform(dest_format)

if dest_format == "csv":
    dest_write.write_csv(csv_file, DSL_0)
elif dest_format == "sql":
    dest_write.write_sql(sql_file, table_name, DSL_0)
elif dest_format == "ggs":
    dest_write.write_ggs(creds_json_file, sheets_name, sheet_name_ggs, DSL_0)
elif dest_format == "sst":
    dest_write.write_sst(api_token_sst, sheet_name_sst, DSL_0)

print("end")