from src2dsl import src_read
from mapping import *
## Step 1. read src file

src_format = "csv"
csv_file = "samples/csv_test.csv"

# src_format = "sql"
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
        for type in map_src["csv"]["string"]:
            if type.regress(col):
                type_options.append(type)
elif src_format == "sql":


print("end")