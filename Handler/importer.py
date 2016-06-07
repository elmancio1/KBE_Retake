import os
from tkFileDialog import askopenfilename
from Tkinter import *
from tkMessageBox import *


class ImporterEx:

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

    if file_extension == ".xlsx":
        from Importers.excel import Excel as Importer
        myImporter = Importer(filePath=filePath)

    elif file_extension == '.txt':
        pass

    elif file_extension == '.dat':

        airfoilPath = str(filePath)

    else:
        showwarning("File type is not supported in this application. Please choose a different format")
        print ("File type is not supported in this application. Please choose a different format")

    ###### Fuselage #####

    fuselageLength = Importer.fuselageLength(myImporter)
    fuselageDiameter = Importer.fuselageDiameter(myImporter)
