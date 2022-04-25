class Number:
    def __init__(self, precision=2, min_val=-100, max_val=100):
        self.prec = precision
        self.minv = min_val
        self.maxv = max_val

    # Do regression to fit given data
    # input: data points [] to regress
    # output: If fit: return True, self.xxx modified. Else: return False
    def regress(self, data):
        # TODO
        return

    # process string to desired format
    # input: string s
    # output: number num
    def process(self, s):
        # TODO
        num = float(s)
        return num

class Currency(Number):
    def __init__(self, cur='USD'):
        self.cur = cur