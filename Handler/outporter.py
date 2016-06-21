import os

class Outporter:


    def __init__(self, Component, ListValues, Path = []):
        self.component = Component
        self.listValues = ListValues
        self.filePath = Path
    """
    Handler that takes care of opening different format files.
    Supported files are :
        *txt
        *excel
        *csv
        *matlab
        *xml
        """


    def fileName(self):
        """

        :return:
        """
        name, extension = os.path.splitext(self.filePath)
        return str(name)

    def fileExtension(self, filePath):
        # type: (object) -> object
        """

        :return:
        """
        name, extension = os.path.splitext(filePath)
        return str(extension)

    ##### Importer selection based on file extension #####

    def writeValue(self):
        """

        :return:
        """
        fileExt = self.fileExtension(self.filePath)

        if fileExt == ".xlsx":
            from IOPorters.excelOut import ExcelOut as VarOutporter
            myImporter = VarImporter(Component=self.component,
                              VariableName=self.variableName,
                              Default=self.default,
                              filePath=self.filePath)
            return VarOutporter.finder(myImporter)

        elif fileExt == '.txt':
            # ToDo: fare txt e magari anche Matlab
            pass

        elif fileExt == '.dat':

            airfoilPath = str(self.filePath)

        else:
            #showwarning("Warning","File type is not supported in this application. Please choose a different format")
            print ('LOG:    File type ' + repr(fileExt) + ' is not supported in this application. Variable '
                   + repr(self.variableName) + ' will set to the default value: ' + repr(self.default))
            return self.default