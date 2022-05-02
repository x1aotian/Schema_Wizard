from DSL_types.String import *
from DSL_types.Number import *
from DSL_types.DateTime import *

map_src = \
{
    "csv": {"string": [Currency, Phone_Number, Email, Date, Number, String]},
    "sql": {"INT": Number, 
            "INTEGER": Number,
            "VARCHAR": String,
            "CHARACTER": String}, # TODO: impliment.
}