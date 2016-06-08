from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Main.Wing.wing import Wing
from Main.Fuselage.fuselage import Fuselage
from Main.Engine.engine import Engine
from Handler.importer import Importer


class Aircraft(GeomBase):
    """
    Basic class Aircraft
    """

    @Input
    def maCruise(self):
        """
        Cruise Mach number
        :Unit: []
        :rtype: float
        """
        return float(Importer(Component='Performance',
                              VariableName='Mach Cruise',
                              Default=0.77).getValue())

    @Part
    def wingbase(self):
        return Wing(maCruise=self.maCruise,
                    fuselageLength=self.fuselagebase.fuselageLength,
                    fuselageDiameter=self.fuselagebase.fuselageDiameter,
                    enginePos=self.enginebase.enginePos)

    @Part
    def fuselagebase(self):
        return Fuselage(maCruise=self.maCruise,
                        )

    @Part
    def enginebase(self):
        return Engine(fuselageLength=self.fuselagebase.fuselageLength,
                      fuselageDiameter=self.fuselagebase.fuselageDiameter,
                      noseLength=self.fuselagebase.noseLength,
                      cylinderLength=self.fuselagebase.cylinderLength,
                      wingSpan=self.wingbase.span,
                      chord35=self.wingbase.chord35,
                      chord40=self.wingbase.chord40,
                      chord70=self.wingbase.chord70,
                      wingVertPos=self.wingbase.vertPos,
                      wingLongPos=self.wingbase.longPos,
                      dihedral=self.wingbase.dihedral,
                      sweepLE=self.wingbase.sweepLE,
                      tcRatio=self.wingbase.tcRatio)




if __name__ == '__main__':
    from parapy.gui import display

    obj = Aircraft()
    display(obj)

