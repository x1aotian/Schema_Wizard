from turtle import screensize
from src2dsl import src_read
from dsl2dest import dest_write
from mapping import *
from DSL import DSL

## Step 1. read src file

# src_format = "csv"
# csv_file = "samples/csv_test.csv"
# src_format = "sql"
# sql_file = "samples/sql_test.db"
# sql_table = "People"

print("------------ Welcome to Schema Wizard CLI Demo ------------")

print("\n> Please input source format. Current valid inputs: csv, sql, ggs, sst.")
src_format = str(input())


if src_format == "csv":
    print("\n> Please input source file's path. ex: \"samples/csv_test.csv\".")
    csv_file = str(input())
    src_data = src_read.read_csv(csv_file)
elif src_format == "sql":
    print("\n> Please input source .db's path & table's name, seperated by comma. ex: \"samples/sql_test.db, People\".")
    sql_file, sql_table = [i.strip() for i in str(input()).split(",")]
    src_data, src_type = src_read.read_sql(sql_file, sql_table)
elif src_format == "ggs":
    print("\n> Please input path of creds json file, sheets name and sheet name, seperated by comma. ex: \"samples/creds_wizard.json, schema_sample, Read\".")
    creds_json_file, sheets_name, sheet_name = [i.strip() for i in str(input()).split(",")]
    src_data = src_read.read_ggs(creds_json_file, sheets_name, sheet_name)
elif src_format == "sst":
    print("\n> Please input api token and sheet name, seperated by comma. ex: \"hGxVYnqxHE3K4OpZufvauB4eUbLGLmH1IpNkn, Read\".")
    api_token_sst, sheet_name_sst = [i.strip() for i in str(input()).split(",")]
    src_data, src_type = src_read.read_sst(api_token_sst, sheet_name_sst)

## Step 2. regress

type_options_proto = []

if src_format in ["csv", "ggs"]:
    for col in src_data.columns:
        type_options_proto.append([])
        for type in map_src["csv"]["string"]:
            type_m = type()
            if type_m.regress(src_data[col]):
                type_options_proto[-1].append(type_m)

elif src_format == "sql":
    for i in range(len(src_type)):
        type_options_proto.append([])
        nm = src_type.loc[i, 'name']
        ty = src_type.loc[i, 'type']
        ty = ty.split('(')[0].upper()
        for type in map_src["sql"][ty]:
            type_m = type()
            if type_m.regress(src_data[nm]):
                type_options_proto[-1].append(type_m)

elif src_format == "sst":
    for i in range(len(src_type.columns)):
        type_options_proto.append([])
        for type in map_src["sst"][src_type.iloc[0, i]]:
            type_m = type()
            if type_m.regress(src_data.iloc[:, i]):
                type_options_proto[-1].append(type_m)


## Step 3. Choose DSL types and attributes
## Step 4.1. create DSL, add types
# suppose always choose the first option
DSL_0 = DSL(0)
DSL_0.setNames(list(src_data.columns))
type_options = []

print("\n> Please design your types for each column.")
for idx, type_option in enumerate(type_options_proto):
    # choose type
    print("\n>>>> input index of type you want to choose for column {%s}. Press Enter to use default values.:" % (DSL_0.getNames()[idx]) )
    for i, typee in enumerate(type_option):
        print("    %d. %s" % (i, typee.__class__.__name__))
    field_input = str(input())
    if field_input:
        cho = int(field_input)
    else:
        cho = 0
    type_option_chosen = type_option[cho]

    # modify attributes
    attr_keys = type_option_chosen.__dict__['mod_attrs']
    attr_values = [type_option_chosen.__dict__[i] for i in attr_keys]
    attr_n = len(attr_keys)
    
    # if no attribute need to be provided by users:
    if (attr_n == 0):
        print("\n>> There is no attribute of this field that needs to be assigned.")
    else:
        print("\n>> Provided atrributes: %s. Recommended values: %s." % (str(attr_keys), str(attr_values)))
        print(">> Input your list of values if you want to do modification. Press Enter to use recommened values.")
        attr_input = str(input())
        if attr_input:
            attr_values_mod = eval(attr_input)
            for i, v in enumerate(attr_keys):
                type_option_chosen.__dict__[v] = attr_values_mod[i]

    DSL_0.addField(type_option[cho])

## Step 4.2. DSL add records (and process) 
for idx, row in src_data.iterrows():
    DSL_0.addRecord(row)

## Step 5. Output in dest format

# dst_format = "csv"
# csv_file = "samples/csv_test_dst.csv"
# dst_format = "sql"
# sql_file = "samples/sql_test_dst.db"
# table_name = "Students"

print("\n> Please input destination format. Current valid inputs: csv, sql, ggs, sst.")
dest_format = str(input())

for field in DSL_0.getFields():
    field.transform(dest_format)

if dest_format == "csv":
    print("\n> Please input dest file's path. ex: \"samples/csv_test_dest.csv\".")
    csv_file = str(input())
    dest_write.write_csv(csv_file, DSL_0)

elif dest_format == "sql":
    print("\n> Please input source .db's path & table's name, seperated by comma. ex: \"samples/sql_test_dest.db, Students\".")
    sql_file, sql_table = [i.strip() for i in str(input()).split(",")]
    dest_write.write_sql(sql_file, sql_table, DSL_0)

elif dest_format == "ggs":
    print("\n> Please input path of creds json file, sheets name and sheet name, seperated by comma. ex: \"samples/creds_wizard.json, schema_sample, Write\".")
    creds_json_file, sheets_name, sheet_name = [i.strip() for i in str(input()).split(",")]
    dest_write.write_ggs(creds_json_file, sheets_name, sheet_name, DSL_0)

elif dest_format == "sst":
    print("\n> Please input api token and sheet name, seperated by comma. ex: \"hGxVYnqxHE3K4OpZufvauB4eUbLGLmH1IpNkn, Write\".")
    api_token_sst, sheet_name_sst = [i.strip() for i in str(input()).split(",")]
    dest_write.write_sst(api_token_sst, sheet_name_sst, DSL_0)

print("\n*** Convert schema from %s to %s successfully! ***" % (src_format, dest_format))