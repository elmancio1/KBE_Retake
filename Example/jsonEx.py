from Handler.IOPorters.jsonIn import JsonIn as VarImporter
import json

myImporter = VarImporter(Component='Fuselage',
                         VariableName='fuselage',
                         Default=35.35,
                         filePath='C:\Users\Jacopo\Desktop\Academic\GitHub\KBE_Retake\Input\Files\A3XX.json')

value = VarImporter.finder(myImporter)

Performance = {  "Performance":
  {
    "Mach cruise": {"value": 0.77, "unit": ""},
    "Wing Loading": 5000.0,
    "MTOW": 422713.0,
    "Cruise Altitude": 10000.0}
}

Configuration = {   "Configuration":
  {
    "Tail Type": "T tail",
    "Engine Position": "wing",
    "Wing Position": "low wing"
  }
}

fileJ = {}

fileJ.update(Performance)
fileJ.update(Configuration)

fout = open('C:\Users\Jacopo\Desktop\Academic\GitHub\KBE_Retake\Output\jsonfile.json', 'w')

json.dump(fileJ, fout, indent=4, sort_keys=True)