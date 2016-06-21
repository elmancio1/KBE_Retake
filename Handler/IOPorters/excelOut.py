from openpyxl import Workbook
from openpyxl import load_workbook

class ExcelOut:

    def __init__(self, Component, ListValues, outputPath):
        self.excelFile = load_workbook(outputPath)
        self.sheet = self.excelFile['Sheet']
        self.component = Component
        self.listValues = ListValues




    def writer(self):
        row = 0
        column = 0
        for line in self.listValues:

            for value in line:
                self.sheet(row=row, column=column, value=value)
                column+=1

            row += 1

        wb.save()

        return "Output file correctly generated"
