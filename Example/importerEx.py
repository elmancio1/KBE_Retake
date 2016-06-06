import os
from Tkinter import *
from tkFileDialog import askopenfilename
from Importers.excelImporter import ExcelImporter

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
        '''
        GUI to open a desired file.
        '''
        name = askopenfilename()
        return name

    filePath = callback()
    filename, file_extension = os.path.splitext(filePath)  # File extension for use in the rest of input file.

    errmsg = 'Error!'
    Button(text='File Open', command=callback).pack(fill=X)

    if file_extension == ".xlsx":

        importer = ExcelImporter(filePath = filePath)

        ###### Fuselage ######

        fuselageLength = ExcelImporter.fuselageLength(importer)
        fuselageRadius = ExcelImporter.fuselageRadius(importer)
        fuselageRadius2 = ExcelImporter.fuselageRadius2(importer)

    elif file_extension == '.txt':
        pass

    elif file_extension == '.dat':

        airfoilPath = str(filePath)

    else:
        print ("File type is not supported in this application. Please choose a different format")