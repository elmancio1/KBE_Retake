from openpyxl import Workbook
from openpyxl import load_workbook

class ExcelOut:

    def __init__(self, Component, ListValues, outputPath):
        self.excelFile = load_workbook(outputPath)
        self.sheet = self.excelFile['Sheet1']
        self.component = Component
        self.listValues = ListValues


    wb = Workbook()

    def writer(self):
        return "Success"
