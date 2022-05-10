import json

## ----- DSL -----

class DSL:

    # init
    def __init__(self, id):
        self.id = id
        self.fields = []
        self.records = []
        self.n_field = 0
        self.dct = {"fields": {}}   # TODO: update dct when adding records

    # add a field for DSL
    def addField(self, field):
        self.fields.append(field)
        self.n_field += 1
        return

    # add a single data point for DSL
    # data_points is string[]
    def addRecord(self, record):
        for i in range(self.n_field):
            record[i] = self.fields[i].process(record[i])
        self.records.append(list(record))
        return

    # save DSL as a file
    def saveToJson(self, file_name):
        with open(file_name, 'w') as outfile:
            json.dump(json.dumps(self.dct), outfile)
        return
