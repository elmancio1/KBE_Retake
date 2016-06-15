import os
from tkFileDialog import askopenfilename
from Tkinter import *
from tkMessageBox import *


class Importer:

    def __init__(self, Component, VariableName, Default, Path = []):
        self.component = Component
        self.variableName = VariableName
        self.default = Default
        self.filePath = Path
    '''
    Handler that takes care of opening different format files.
    Supported files are :
        *txt
        *excel
        *csv
        *matlab
        *xml
    '''

    #def callback():
     #   """
      #  GUI to open a desired file and gives back the path to the file.
       # """
        #name = askopenfilename()
        #return name

    #filePath = callback()
    #filename, file_extension = os.path.splitext(filePath)  # File extension for use in the rest of input file.


    #errmsg = 'Error!'
    #Button(text='File Open', command=callback).pack(fill=X)

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

    def getValue(self):
        """

        :return:
        """
        fileExt = self.fileExtension(self.filePath)

        if fileExt == ".xlsx":
            from Importers.excel import Excel as VarImporter
            myImporter = VarImporter(Component=self.component,
                              VariableName=self.variableName,
                              Default=self.default,
                              filePath=self.filePath)
            return VarImporter.finder(myImporter)

        elif fileExt == '.txt':
            pass

        elif fileExt == '.dat':

            airfoilPath = str(self.filePath)

        else:
            #showwarning("Warning","File type is not supported in this application. Please choose a different format")
            print ('File type ' + repr(fileExt) + ' is not supported in this application. Variable '
                   + repr(self.variableName) + ' will set to the default value: ' + repr(self.default))
            return self.default

