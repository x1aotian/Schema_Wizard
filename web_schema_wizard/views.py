from glob import glob
from urllib import request
from attr import attr
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from turtle import screensize
from src2dsl import src_read
from dsl2dest import dest_write
from mapping import *
from DSL import DSL


# file_path = ""
type_options_proto = []
# type_options = []
loop_num = 0
# type_option_temp = None
DSL_0 = None
src_data = None
src_format = ""
dest_format = ""
src_type = None
# csv_dest_file = ""
# sql_dest_file = ""
# sql_table_name_src = ""
# sql_table_name_dest = ""
type_option = None
csv_file = ""
sql_file = ""
csv_dest_file = ""
sql_dest_file = ""
sql_table_name_dest = ""
type_option_name = []
column_name = []

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def form(request):
    return render(request, 'index.html')

def main(request):
    # context = {}
    # context['res'] = "you succeed!"
    # return render(request, 'result.html', context)

    return render(request, 'design.html')

def view2(request, id):
    return HttpResponse("You are navigating the view of %s" %id)

def original_view(request):  # use id when we have form like path('<int:question_id>/original_view')
    return render(request, 'index.html')

def choose_type(request):
    if request.method == 'POST':
        global src_format
        src_format = str(request.POST.get('source'))
        global dest_format
        dest_format = str(request.POST.get('dest'))
        # file_path = str(request.POST.get('myFile'))
        
        global src_data
        global src_type
        global csv_file
        global sql_file  # just for debugging
        src_format = src_format.lower()
        # src_format may be used inside DSL, so use lower case for consistency
        if src_format == "csv":
            # print("\n> Please input source file's path. ex: \"samples/csv_test.csv\".")
            csv_file = str(request.POST.get('csv_src_file')).strip() 
            # csv_file = request.POST.get('csv_src_file') 
            src_data = src_read.read_csv(csv_file)
        elif src_format == "sql":
            # print("\n> Please input source .db's path & table's name, seperated by comma. ex: \"samples/sql_test.db, People\".")
            # sql_file, sql_table = [i.strip() for i in str(input()).split(",")]
            sql_file = str(request.POST.get('sql_src_file')).strip()
            sql_table_name_src = str(request.POST.get('sql_table_name_src'))
            src_data, src_type = src_read.read_sql(sql_file, sql_table_name_src)            

        # do regress
        global type_options_proto
        global column_name
        if src_format == "csv":
            for col in src_data.columns:
                # store column name in a list and pass it to html later
                column_name.append(col)
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
        
        global DSL_0
        DSL_0 = DSL(0)
        # 【！！】xiaotian changed the member var name from names to __names, which leads to bug
        # DSL_0.names = list(src_data.columns)
        DSL_0.setNames(list(src_data.columns))

        # dest_path should be designated here, because 'request' would change when using other html
        dest_format = dest_format.lower()
        if dest_format == "csv":
            # print("\n> Please input dest file's path. ex: \"samples/csv_test_dest.csv\".")
            global csv_dest_file
            csv_dest_file = str(request.POST.get('csv_dest_file'))
            # dest_write.write_csv(csv_dest_file, DSL_0)
        elif dest_format == "sql":
            # print("\n> Please input source .db's path & table's name, seperated by comma. ex: \"samples/sql_test_dest.db, Students\".")
            # sql_file, sql_table = [i.strip() for i in str(input()).split(",")]
            global sql_dest_file
            global sql_table_name_dest
            sql_dest_file = str(request.POST.get('sql_dest_file'))
            sql_table_name_dest = str(request.POST.get('sql_table_name_dest'))
            # dest_write.write_sql(sql_dest_file, sql_table_name_dest, DSL_0

        # context = {'type_options_proto': type_options_proto}
        # return render(request, 'choose_type.html', context)
        
        global type_option
        # 【！！】index should be 0
        type_option = type_options_proto[0]
        global type_option_name
        for type in type_option:
            typeName = type.__class__.__name__
            type_option_name.append(typeName)
        # type_option_temp = type_option
        # not passing the class objects into html, but passing dict containing strings
        # pass all the possible types and their demands into it
        type_list = []
        type_list_demands = []
        for type in type_option:
            typeName = type.__class__.__name__
            attr_keys = type.__dict__['mod_attrs']
            type_list.append(typeName)
            type_list_demands.append(attr_keys)
        context = {'type_list': type_list,
                   'type_list_demands': type_list_demands,
                   'column_name': column_name[0]}
        global loop_num
        loop_num = 0
        return render(request, 'design.html', context)

def choose_type_mod_loop(request):
    global type_option_name
    if request.method == 'POST':
        field_input = str(request.POST.get('chooseType'))  # 【！！】menu list should set values of different options as indexes (choose nothing leads to 'default' value) —— html can set value for different menu list option
        if field_input != "default":
            index = type_option_name.index(field_input)
            cho = index
        else:
            cho = 0
        global type_option
        type_option_chosen = type_option[cho]

        # modify attributes
        # attr_keys = type_option_chosen.__dict__['mod_attrs']  # attr_keys are "maxLen", "minLen"
        # attr_values = [type_option_chosen.__dict__[i] for i in attr_keys]  # attr_values are 10, 0, etc
        # attr_n = len(attr_keys)
        # attr_input = str(request.POST.get('modify'))  # 【！！】
        # if attr_input:
        #     attr_values_mod = eval(attr_input)
        #     for i, v in enumerate(attr_keys):
        #         type_option_chosen.__dict__[v] = attr_values_mod[i]
        # global DSL_0
        # DSL_0.addField(type_option[cho])

        attr_keys = type_option_chosen.__dict__['mod_attrs']
        for i, demand in enumerate(attr_keys):
            demand_input = request.POST.get(str(demand))
            # demand_input == "" means use default type and attributes (demands) OR choose the type whose attributes can't be modified OR just input nothing in some attributes
            if demand_input != "":
                # eval can't transfer string ['1.5','hey'] to float 1.5 and string hey
                # Another downside of eval is that it will transfer 'USD' to a var named 'USD'
                # solution: use "['USD']" rather than 'USD'
                # 【？？】should not allow users to input float to attributes?
                # demand_input = "['" + demand_input + "']"
                # demand_input_eval = eval(demand_input)  # don't work for 'USD'【？？】
                # isdigit dont work for -5
                if is_number(demand_input):
                    demand_input_eval = int(demand_input)
                else:
                    demand_input_eval = demand_input
                type_option_chosen.__dict__[demand] = demand_input_eval
        global DSL_0
        DSL_0.addField(type_option[cho])


        # repeatedly call the html page
        global loop_num
        global column_name
        if loop_num < len(type_options_proto) - 1:
            total_len = len(type_options_proto)
            type_option = type_options_proto[loop_num+1]
            # renew type_option_name
            type_option_name = []
            for type in type_option:
                typeName = type.__class__.__name__
                type_option_name.append(typeName)
            # generate dict for html page
            type_list = []
            type_list_demands = []
            for type in type_option:
                typeName = type.__class__.__name__
                attr_keys = type.__dict__['mod_attrs']
                type_list.append(typeName)
                type_list_demands.append(attr_keys)
            context = {'type_list': type_list,
                       'type_list_demands': type_list_demands,
                       'column_name': column_name[loop_num+1]}
            loop_num += 1
            return render(request, 'design.html', context)
        
        ## Step 4.2. DSL add records (and process) 
        global src_data
        for idx, row in src_data.iterrows():
            DSL_0.addRecord(row)

        global dest_format
        global csv_dest_file
        global sql_dest_file
        global sql_table_name_dest
        global src_format

        # 【！！】neglect this at first
        for field in DSL_0.getFields():
            field.transform(dest_format)

        if dest_format == "csv":
            # print("\n> Please input dest file's path. ex: \"samples/csv_test_dest.csv\".")
            # csv_dest_file = str(request.POST.get('csv_dest_file'))
            dest_write.write_csv(csv_dest_file, DSL_0)
        elif dest_format == "sql":
            # print("\n> Please input source .db's path & table's name, seperated by comma. ex: \"samples/sql_test_dest.db, Students\".")
            # sql_file, sql_table = [i.strip() for i in str(input()).split(",")]
            # sql_dest_file = str(request.POST.get('sql_dest_file'))
            # sql_table_name_dest = str(request.POST.get('sql_table_name_dest'))
            dest_write.write_sql(sql_dest_file, sql_table_name_dest, DSL_0)
        context = {}
        context['res'] = 'Convert successfully from %s to %s!' % (src_format, dest_format)
        return render(request, 'result.html', context)