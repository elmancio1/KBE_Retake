from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *


class Fuselage(GeomBase):
    """
    Basic class Fuselage
    """

    @Input
    def fuselageLength(self):
        """
        Aircraft fuselage length
        :Unit: [m]
        :rtype: float
        """
        return 35.

    @Input
    def fuselageDiameter(self):
        """
        Aircraft Diameter
        :Unit: [m]
        :rtype: float
        """
        return 4.

    @Input
    def noseSlenderness(self):
        """
        Aircraft nose slenderness, equal to nose length over fuselage diameter
        :Unit: [ ]
        :rtype: float
        """
        if self.maCruise < 0.65 or self.maCruise > 0.90:
            showwarning("Warning", "Please insert a value between 0.65 and 0.9")
            print("Please insert a value between 0.65 and 0.9")
            return 0.81
        else:
            return 0.0065 * exp(6.6077 * self.maDD)

    @Input
    def tailSlenderness(self):
        """
        Aircraft tail slenderness, equal to tail length over fuselage diameter
        :Unit: [ ]
        :rtype: float
        """
        return 3.

    @Input
    def tailUpAngle(self):
        """
        Aircraft tail angle, positive upward
        :Unit: [deg]
        :rtype: float
        """
        return 5.

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ###

    if __name__ == '__main__':
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def maCruise(self):
        return 0.77

    # ### Attributes ###

    @Attribute
    def maDD(self):
        """
        Aircraft Mach Dive Divergence
        :Unit: [ ]
        :rtype: float
        """
        return self.maCruise + 0.03

    @Attribute
    def noseLength(self):
        """
        Aircraft nose length
        :Unit: [m]
        :rtype: float
        """
        return self.noseSlenderness * self.fuselageDiameter

    @Attribute
    def tailLength(self):
        """
        Aircraft tail length
        :Unit: [m]
        :rtype: float
        """
        return self.tailSlenderness * self.fuselageDiameter

    @Attribute
    def cylinderLength(self):
        """
        Aircraft fuselage cylindrical section length
        :Unit: [m]
        :rtype: float
        """
        return self.fuselageLength - (self.noseLength + self.tailLength)






if __name__ == '__main__':
    from parapy.gui import display

    obj = Fuselage()
    display(obj)