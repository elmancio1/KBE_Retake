from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Handler.importer import Importer
import Tkinter, Tkconstants, tkFileDialog

class LandingGear(GeomBase):
    """
    Basic class Landing Gear
    """

    @Input
    def gearHeight(self):
        """
        Height of the main landing gear
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='height',
                              Default=3.0).getValue())

    @Input
    def mainGearPos(self):
        """
        Gear position with regard to the fuselage or wing
        depending on high or low wing configuration
        :Unit: []
        :rtype: float
        """
        if self.wingPosition == 'low wing':
            return float(Importer(Component='Landing Gear',
                                  VariableName='gear wing position',
                                  Default=0.5).getValue())
        elif self.wingPosition == 'high wing':
            return float(Importer(Component='Landing Gear',
                                  VariableName='gear fuselage position',
                                  Default=0.6).getValue())

    @Input
    def mainGearLat(self):
        """
        Lateral gear position with regard to the fuselage diameter
        :Unit: []
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='lateral gear position',
                              Default=2.5).getValue())

    @Input
    def noseGearPos(self):
        """
        Gear position with regard to the fuselage
        :Unit: []
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='nose gear position',
                              Default=0.1).getValue())

    @Input
    def mainWheelDiameter(self):
        """
        Height of the main landing gear
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='main wheel diameter',
                              Default=1.5).getValue())

    @Input
    def noseWheelDiameter(self):
        """
        Height of the main landing gear
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='nose wheel diameter',
                              Default=0.5).getValue())

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ################################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from engine
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def filePath(self):
        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        filename = tkFileDialog.askopenfilename()
        return str(filename)

    @Input(settable=settable)
    def wingPosition(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 'low wing'

    @Input(settable=settable)
    def fuselageDiameter(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 5.0

    @Input(settable=settable)
    def fuselageLength(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 30.

    @Input
    def xLEMAC(self):
        """

        :return:
        """
        return 18.0

    @Input(settable=settable)
    def cMAC(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 3.0


    # ### Attributes ##################################################################################################

    @Attribute
    def mainLongPos(self):
        """
        main landing gear longitudinal position.
        :Unit: [m]
        :rtype: float
        """
        return self.xLEMAC


