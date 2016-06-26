import os
import Output
from time import gmtime, strftime
import openpyxl
from tkMessageBox import *


class Outporter:


    def __init__(self, ListValues, Path = []):
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
        finalString = strftime("%d-%m-%Y %H" + "h %M" + "m %S" + "s", gmtime())

        if fileExt == ".xlsx":

            outputPath = os.path.dirname(Output.__file__) + '\output ' + finalString + '.xlsx'

            wb = openpyxl.Workbook()

            wb.save(outputPath)

            from IOPorters.excelOut import ExcelOut as VarOutporter

        elif fileExt == '.json':
            from IOPorters.jsonOut import JsonOutOut as VarOutporter

        else:
            print ('Warning:    File type ' + repr(fileExt) + ' is not supported in this application. '
                                                              'The file will be exported in .json format.')
            showwarning("Warning", "File type " + repr(fileExt) + " is not supported in this application."
                                                                  " The file will be exported in .json format.")
            outputPath = os.path.dirname(Output.__file__) + '\output ' + finalString + '.json'

            from IOPorters.jsonOut import JsonOutOut as VarOutporter

        myOutporter = VarOutporter(ListValues=self.listValues,
                                   outputPath=outputPath)

        return VarOutporter.writer(myOutporter)