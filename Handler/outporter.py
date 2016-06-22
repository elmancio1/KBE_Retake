import os
import Output
from time import gmtime, strftime
import openpyxl
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

    def writeValues(self):
        """

        :return:
        """
        fileExt = self.fileExtension(self.filePath)

        if fileExt == ".xlsx":

            finalString = strftime("%d-%m-%Y %H"+"h %M"+"m %S"+"s", gmtime())

            outputPath = os.path.dirname(Output.__file__) + '\output ' + finalString + '.xlsx'

            wb = openpyxl.Workbook()

            wb.save(outputPath)

            from IOPorters.excelOut import ExcelOut as VarOutporter
            myOutporter = VarOutporter(Component=self.component,
                                       ListValues=self.listValues,
                                       outputPath=outputPath)
            return VarOutporter.writer(myOutporter)

        elif fileExt == '.txt':
            # ToDo: fare txt e magari anche Matlab
            pass

        else:
            #showwarning("Warning","File type is not supported in this application. Please choose a different format")
            print ('LOG:    File type ' + repr(fileExt) + ' is not supported in this application.')