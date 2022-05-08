import datetime

import datetime
class Date:
    # possible formats: 'YYYY-MM-DD', 'DD/MM/YYYY', 'DD.MM.YYYY', 'MM.DD.YYYY'
    def __init__(self, format_list=['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%m/%d/%Y']):
        self.fmt_list = format_list
        now = datetime.datetime.now()
        self.max_year = now.year
        self.min_year = now.year
    
    def regress(self, data):
        '''
        list: [Year, Month, Day, Hour, Minute, Second, Day of Week, Day of Year, Daylight savings time]

        try different format for different data. if all format fail to regre
        '''
        for di in data:
            date = None
            for fmt in self.fmt_list:
                try:
                    date = datetime.datetime.strptime(di, fmt)
                except ValueError:
                    pass
            if (date is None): return False
            if (date.year > self.max_year): self.max_year = date.year
            if (date.year < self.min_year): self.min_year = date.year
        return True
    
    def process(self, s):
        date = None
        for fmt in  self.fmt_list:
            try:
                date = datetime.datetime.strptime(s, fmt)
                self.fmt = fmt
            except:
                pass
        try:
            date_list = list(date.timetuple())
            # check the max_year, min_year
            if (date_list[0] > self.max_year): date_list[0] = self.max_year
            if (date_list[0] < self.min_year): date_list[0] = self.min_year
            return date_list
        except:
            print("Error!: incorrect formats, Please check the format of the input you need to process")

class Time:
    '''
    Initialize the Time class
    Args:
        int formats: 'HH:MM:SS XM' or 'HH:MM:SS'
    '''
    def __init__(self, format_list = ['%H:%M:%S AM', '%H:%M:%S PM', '%H:%M:%S']):
        now = datetime.datetime.now()
        self.year = now.year
        self.month = now.month
        self.day = now.day
        self.fmt_list = format_list
    
    def regress(self, data):
        for di in data:
            date = None
            for fmt in self.fmt_list:
                try:
                    date = datetime.datetime.strptime(di, fmt)
                except ValueError:
                    pass
            if (date is None): return False
            print(date)
        return True
    
    def process(self, s):
        '''
        list: [Year, Month, Day, Hour, Minute, Second, Day of Week, Day of Year, Daylight savings time]
        process all the time to the same format
        '''
        need_add_12 = False
        if (s[-2] == 'A' or s[-2] == 'P'):
            if (s[-2] == 'P'): need_add_12 = True
            s = s[:-3]
        
        try:
            date = datetime.datetime.strptime(s, '%H:%M:%S')
            date_list = list(date.timetuple())
            date_list[0] = self.year
            date_list[1] = self.month
            date_list[2] = self.day
            if (need_add_12): date_list[3] += 12
            return date_list
        except:
            print("Error!: incorrect formats, Please check the format of the input you need to process")


class DateTime(Date):
    def __init__(self, format_list=["%Y-%m-%d %H:%M:%S"]):
        self.fmt_list = format_list
        now = datetime.datetime.now()
        self.max_year = now.year
        self.min_year = now.year