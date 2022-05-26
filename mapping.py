from DSL_types.String import *
from DSL_types.Number import *
from DSL_types.DateTime import *

# if some type in sql can't find itself (i.e. the key) in this dict, then means we are not able to support that type
map_src = \
{
    "csv": {"string": [Number, Currency, Date, Time, DateTime, Email, Phone_Number, URL, String]}, # phone number with no -
    "sql": {"INT": [Number, Currency],  # don't allow Currency here?
            "INTEGER": [Number, Currency],  # phone number here?
            "FLOAT": [Number, Currency],
            "DOUBLE": [Number, Currency],  # no need to turn into String; if sql want phone number, they should use char/varchar rather than float/double/int/integer, the same to URL
            "VARCHAR": [Number, Currency, Date, Time, DateTime, Email, Phone_Number, URL, String],   # varchar can contain letters, numbers and special characters
            "CHAR": [Number, Currency, Date, Time, DateTime, Email, Phone_Number, URL,  String], 
            "DATE": [Date],
            "DATETIME":[DateTime],
            "TIMESTAMP":[DateTime]},
            # TODO: we don't have YEAR type in dsl model
    # airtable docu: https://support.airtable.com/hc/en-us/articles/202624179-The-primary-field
    # airtable detailed def on type: https://support.airtable.com/hc/en-us/categories/360003084953-Fields
    "airtable": {"Single line text": [Number, Currency, Date, Time, DateTime, Email, Phone_Number, URL, String],
                 "Long Text": [Number, Currency, Date, Time, DateTime, Email, Phone_Number, URL, String],
                 "Currency": [Currency],  # 【？？】if src is Currency. then it should be Currency in DSL, that users have no access to change to other type?
                 "Number": [Number, Currency],  # phone number not necessary here, since at has Phone Number type
                 "Percent": [Number, String],  # percent to either number (remove %) or string (have %) —— TODO: or make a percent type in DSL
                 "URL": [URL],
                 "Email": [Email],
                 "Phone number": [Phone_Number],
                 "Date": [Date, DateTime]},
    # nintex docu: https://help.nintex.com/en-us/nwc/Content/Designer/FormControls/FormControls.htm
    "nintex": {"Text - Long": [Number, Currency, Date, Time, DateTime, Email, Phone_Number, URL, String],
               "Text - Short": [Number, Currency, Date, Time, DateTime, Email, Phone_Number, URL, String],
               "Currency": [Currency],
               "Number": [Number, Currency],
               "Email": [Email],
               "Date/time": [Date, DateTime], # 【？？】no idea on the regex of Date/time type of nintex
               "Yes/no": [String]},  # TODO: define a boolean type in DSL

    # smartsheet doc: 
    "sst": {"TEXT_NUMBER": [Number, Currency, Date, Time, DateTime, Email, Phone_Number, URL, String],
            "DATE": [Date],
            "PICKLIST": [Number, Currency, Date, Time, DateTime, Email, Phone_Number, URL, String],
            "CHECKBOX": [Number, Currency, Date, Time, DateTime, Email, Phone_Number, URL, String]}
}