import json

## ----- DSL -----

class DSL:

    # init
    def __init__(self, id):
        self.id = id
        self.__names = []
        self.__fields = []
        self.__records = []
        self.n_field = 0
        self.dct = {"fields": {}}   # TODO: update dct when adding records

    # add a field for DSL
    def addField(self, field):
        self.__fields.append(field)
        self.n_field += 1
        return

    # add a single data point for DSL
    # data_points is string[]
    def addRecord(self, record):
        for i in range(self.n_field):
            record[i] = self.__fields[i].process(record[i])
        self.__records.append(list(record))
        return

    # save DSL as a file
    def saveToJson(self, file_name):
        with open(file_name, 'w') as outfile:
            json.dump(json.dumps(self.dct), outfile)
        return
    
    # getter of DSL fields
    def getFields(self):
        return self.__fields
    
    # len of Fields
    def lenFields(self):
        return len(self.__fields)

    # getter of DSL names
    def getNames(self):
        return self.__names
    
    # setter of DSL names
    def setNames(self, names):
        self.__names = names

    # len of Fields
    def lenNames(self):
        return len(self.__names)

    # getter of DSL records
    def getRecords(self):
        return self.__records
    
    def lenRecords(self):
        return len(self.__records)