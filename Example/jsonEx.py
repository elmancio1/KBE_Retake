from Handler.IOPorters.jsonIn import Json as VarImporter

myImporter = VarImporter(Component='Fuselage',
                         VariableName='fuselage',
                         Default=35.35,
                         filePath='C:\Users\Jacopo\Desktop\Academic\GitHub\KBE_Retake\Input\Files\A3XX.json')

value = VarImporter.finder(myImporter)

print value