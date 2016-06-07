import os
from tkFileDialog import askopenfilename
from Tkinter import *
from tkMessageBox import *


class Importer:

    def __init__(self, Component, VariableName, Default):
        self.component = Component
        self.variableName = VariableName
        self.default = Default

    '''
    Handler that takes care of opening different format files.
    Supperted files are :
        *txt
        *excel
        *csv
        *matlab
        *xml
    '''

    def callback():
        """
        GUI to open a desired file and gives back the path to the file.
        """
        name = askopenfilename()
        return name

    filePath = callback()
    filename, file_extension = os.path.splitext(filePath)  # File extension for use in the rest of input file.

    errmsg = 'Error!'
    Button(text='File Open', command=callback).pack(fill=X)

    ##### Importer selection based on file extension #####

    def VariableValue(self):
        """


        :return:
        """
        if self.file_extension == ".xlsx":
            from Importers.excel import Excel as VarImporter
            myImporter = VarImporter(Component=self.component,
                              VariableName=self.variableName,
                              Default=self.default,
                              filePath=self.filePath)
            return VarImporter.finder(myImporter)

        elif self.file_extension == '.txt':
            pass

        elif self.file_extension == '.dat':

            airfoilPath = str(self.filePath)

        else:
            showwarning("File type is not supported in this application. Please choose a different format")
            print ("File type is not supported in this application. Please choose a different format")

