class String:
    def __init__(self, min_len=0, max_len=100, pattern=None):
        self.minl = min_len
        self.maxl = max_len
        self.ptrn = pattern
    
    # Notice: must consider pattern match here.
    def regress(self, data):
        # TODO
        return
    
    def process(self, s):
        # TODO
        s_ = s
        return s_

class Email(String):
    def __init__(self, pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'):
        self.pattern = pattern

class Phone_Number(String):
    # for reference: https://softhints.com/regex-phone-number-find-validation-python/
    def __init__(self, pattern=[r'{3}-[\d]{3}-[\d]{3}', r'[\d]{3} [\d]{3} [\d]{3}']):
        self.pattern = pattern