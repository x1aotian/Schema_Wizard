'''
helper function
parse the number from string
'''
def parse(di, cur_prec, change_prec=False):
    isNegative = False
    # negative number
    if (di[0] == '-'):
        di = di[1:]
        isNegative = True
    # decimal point
    partition = di.partition('.')
    
    if di.isdigit():
        if (cur_prec == 0): 
            new_di = int(partition[0])
        else: 
            new_di = float(di)
    elif (partition[0].isdigit() and partition[1] == '.' and partition[2].isdigit()) or (partition[0] == '' and partition[1] == '.' and partition[2].isdigit()) or (partition[0].isdigit() and partition[1] == '.' and partition[2] == ''):
        if (change_prec):
            if (cur_prec == 0): 
                new_di = int(partition[0])
            else:
                new_di = str(round(float(di), cur_prec))
        else: 
            cur_prec = len(partition[2])
            new_di = float(di)
    else:
        return None, None
           
    return (-new_di, cur_prec) if (isNegative) else (new_di, cur_prec)
    

class Number:
    def __init__(self, precision=0, min_val=-100, max_val=100):
        self.prec = precision
        self.minv = min_val
        self.maxv = max_val
        self.dest_form = None
        self.dest_type = ""
        self.mod_attrs = ["prec", "minv", "maxv"]

    # Do regression to fit given data
    # input: data points [] to regress
    # output: If fit: return True, self.xxx modified. Else: return False
    def regress(self, data):
        # TODO
        cur_prec = 0
        for di in data:
            new_di, cur_prec = parse(di, cur_prec)
            if (new_di is None and cur_prec is None): return False
            # update the precision, min_val, and max_val
            if (new_di < self.minv): self.minv = new_di
            if (new_di > self.maxv): self.maxv = new_di
            if (cur_prec > self.prec): self.prec = cur_prec
        return True

    # process string to desired format
    # input: string s
    # output: number num, prec (neglected)
    def process(self, s):
        num, _ = parse(s, self.prec, change_prec = True)
        return num
    
    def getDestType(self, dest_form):
        self.dest_form = dest_form
        if dest_form == "sql":
            if self.prec == 0:
                self.dest_type = "INT"
            else:
                self.dest_type = "DOUBLE"
        elif dest_form == "csv":
            self.dest_type = "string"

    def transform(self, data):
        if self.dest_form == "sql":
            if self.dest_type == "INT":
                # convert the DSL into the int if it's not int
                if (type(data) != int): DSL = int(data)
            elif self.dest_type == "DOUBLE":  # use double 
                if (type(data) == int):
                    data_new = float(int)
                else:
                    data_new = round(data, self.prec)

        elif self.dest_form == "csv":
            data_new = str(data)
        return data_new

class Currency(Number):
    def __init__(self, curr_type='USD', curr_map = {'USD': '$', 'CNY': '¥', 'GBP': '£', 'EUR': '€'},precision=0, min_val=-100, max_val=100):
        self.curr_type = curr_type
        self.curr_map = curr_map
        self.prec = precision
        self.minv = min_val
        self.maxv = max_val
        self.dest_form = None
        self.dest_type = ""
        self.mod_attrs = ["curr_type", "prec", "minv", "maxv"]

    def regress(self, data):
        cur_prec = 0
        for di in data:
            curr_out = False

            if (di[0] == '-'): 
                di = di[1:]
                curr_out = True
    
            if (di[0] in self.curr_map.values()):
                di = di[1:]
            s_new, next_prec = parse(di, cur_prec)
            
            if (s_new is None): 
                return False
            if (curr_out): s_new = -s_new
            
            if (s_new < self.minv): self.minv = s_new
            if (s_new > self.maxv): self.maxv = s_new
            if (next_prec > self.prec): self.prec = next_prec
            cur_prec = next_prec
        return True
    
    def process(self, s):
        curr_out = False

        if (s[0] == '-'): 
            s = s[1:]
            curr_out = True
        if (s[0] in self.curr_map.values()):
            s = s[1:]
        num, _ = parse(s, self.prec, change_prec = True)
        return -num if curr_out else num
    
    def getDestType(self, dest_form):
        self.dest_form = dest_form
        if dest_form == "sql":
            if self.prec == 0:
                self.dest_type = "INT"
            else:
                self.dest_type = "DOUBLE"  # use double 

        elif dest_form == "csv":
            self.dest_type = "string"


    def transform(self, data):
        if self.dest_form == "sql":
            if self.dest_type == "INT":
                # convert the DSL into the int if it's not int
                if (type(data) != int): data_new = int(data)
            else:
                self.dest_type = "DOUBLE"  # use double 
                if (type(data) == int):
                    data_new = float(int)
                else:
                    data_new = round(data, self.prec)

        elif self.dest_form == "csv":
            self.dest_type = "string"
            data_new = self.curr_map[self.curr_type] + str(data)

        return data_new
            