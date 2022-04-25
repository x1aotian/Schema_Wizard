class Date:
    # possible formats: 'YYYY-MM-DD', 'MM/DD/YYYY', 'YYYY.MM.DD', 'MMM DD, YYYY'...
    def __init__(self, format='YYYY-MM-DD'):
        self.fmt = format


class Time:
    # possible formats: 12 'HH:MM:SS XM', 24 'HH:MM:SS '
    def __init__(self, format=12):
        self.fmt = format

class DateTime:
    def __init__(self):
        return