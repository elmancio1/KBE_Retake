from time import gmtime, strftime
import os
import Output
finalString = strftime("%Y-%m-%d %H:%M:%S", gmtime())

outputPath = os.path.dirname(Output.__file__) + '\output ' + finalString + '.xlsx'

print outputPath