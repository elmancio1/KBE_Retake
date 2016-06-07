from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Main.Wing.wing import Wing
from Main.Fuselage.fuselage import Fuselage


class Aircraft(GeomBase):
    """
    Basic class Aircraft
    """

    @Part
    def wingbase(self):
        return Wing(fuselageLength=self.fuselagebase.fuselageLength,
                    fuselageDiameter=self.fuselagebase.fuselageDiameter)

    @Part
    def fuselagebase(self):
        return Fuselage()




if __name__ == '__main__':
    from parapy.gui import display

    obj = Aircraft()
    display(obj)

