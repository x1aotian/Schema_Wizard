import re

class String:
    """
    Initialize the String class
    
    Args:
        int min_len: The minimum length for current String class
        int max_len: The maximum length for current String class
        string pattern: The regex pattern of String class
        
        "(.*?)" matches anything
    """
    def __init__(self, min_len=0, max_len=100, pattern="(.*?)"):
        self.minl = min_len
        self.maxl = max_len
        self.pattern = pattern
        self.dest_type = ""
    
    # Notice: must consider pattern match here.
    # data is a list.
    # src, src_data_type are checked in map_src.py
    def regress(self, data):
        '''
        see if data can regress to current type (class)
        '''
        for di in data:
            if (len(di) < self.minl): self.minl = len(di)
            if (len(di) > self.maxl): self.maxl = len(di)
            if self.pattern != "(.*?)":
                re_match = re.match(self.pattern, di)
                if not re_match:
                    return False
        return True

    def process(self, s):
        '''
        process the string according to attributes
        '''
        # TODO
        if len(s) > self.maxl:
            s = s[:self.maxl]
        return s

    def transform(self, dest_form):
        if dest_form == "sql":
            # use varchar
            self.dest_type = "VARCHAR"
        elif dest_form == "csv":
            self.dest_type = "string"
            

class Email(String):
    def __init__(self, min_len = 0, max_len = 100, pattern=r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$'):
        self.minl = min_len
        self.maxl = max_len
        self.pattern = pattern
        self.dest_type = ""

    # completely reuse the super method (so not explicitly writing is ok)
    def transform(self, dest_form):
        return super().transform(dest_form)
    
        

class Phone_Number(String):
    # for reference: https://softhints.com/regex-phone-number-find-validation-python/
    def __init__(self, min_len = 0, max_len = 100, pattern=[r'^[\d]{3}-[\d]{3}-[\d]{4}$', r'^[\d]{3} [\d]{3} [\d]{4}$', r'^\([\d]{3}\) [\d]{3}-[\d]{4}$']):
        '''
        Initialize a Phone Number class: e.g. 123 456 7890, 123-456-7890, (123) 456-7890
        '''
        self.minl = min_len
        self.maxl = max_len
        self.pattern = pattern
        self.dest_type = ""
    
    def regress(self, data):
        for di in data:
            if (len(di) < self.minl): self.minl = len(di)
            if (len(di) > self.maxl): self.maxl = len(di)
            if self.pattern != "(.*?)":
                re_match = None
                # pattern: a list of regex pattern
                for p in self.pattern:
                    if (re_match is not None): continue
                    re_match = re.match(p, di)

                if not re_match:
                    return False
        return True
    
    def process(self, s):
        """
        process all the phone number to the same format
        """
        # '(123) 456-7890' => '1234567890'
        if (re.match(r'^\([\d]{3}\)[\d]{3}-[\d]{4}$', s) is not None):
            digits_section = re.split(r'[^0-9]',s)[1:]
        
        # '123 456 7890' => '1234567890'
        # '123-456-7890'  => '1234567890'
        # ‘1234567890’  => '1234567890'
        else:
            digits_section = re.split(r'[^0-9]',s)
        
        s_ = ""
        for digits in digits_section:
            s_ += digits
        
        return s_
    
    def transform(self, dest_form):
        return super().transform(dest_form)

class URL(String):
    def __init__(self, min_len = 0, max_len = 100, pattern="((?<=[^a-zA-Z0-9])(?:https?\:\/\/|[a-zA-Z0-9]{1,}\.{1}|\b)(?:\w{1,}\.{1}){1,5}(?:com|org|edu|gov|uk|net|ca|de|jp|fr|au|us|ru|ch|it|nl|se|no|es|mil|iq|io|ac|ly|sm){1}(?:\/[a-zA-Z0-9]{1,})*)"):
        self.minl = min_len
        self.maxl = max_len
        self.pattern = pattern
        self.dest_type = ""
    
    def transform(self, dest_form):
        return super().transform(dest_form)
