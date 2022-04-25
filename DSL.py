import json

## ----- DSL -----

class DSL:

    # init
    def __init__(self, id):
        self.id = id
        self.fields = []
        self.records = []
        self.dct = {"fields": {}}   # TODO: update dct when adding records

    # add a field for DSL
    def addField(self, field):
        # TODO: check if valid
        self.fields.append(field)
        return

    # add a single data point for DSL
    # data_points is string[]
    def addRecord(self, record):
        # TODO: check if valid
        self.records.append(record)
        return

    # save DSL as a file
    def saveToJson(self, file_name):
        with open(file_name, 'w') as outfile:
            json.dump(json.dumps(self.dct), outfile)
        return
