import json


class Json:

    def __init__(self, Component, VariableName, Default, filePath):
        with open(filePath) as data_file:
            self.data = json.load(data_file)
        self.component = Component
        self.variableName = VariableName
        self.default = Default

    def finder(self):

        component = self.data[self.component]
        value = component[self.variableName]

        print component, value
        return value


