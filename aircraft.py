from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Main.Wing.wing import Wing
from Main.Fuselage.fuselage import Fuselage
from Main.Engine.engine import Engine
from Main.Vtp.vtp import Vtp
from Main.Htp.htp import Htp
from Handler.importer import Importer


class Aircraft(GeomBase):
    """
    Basic class Aircraft
    """

    @Input
    def variabile(self):
        return 1.0

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

    @Input
    def wingLoading(self):
        """
        Aircraft wing loading
        :Unit: [kg / m^2]
        :rtype: float
        """
        return 4496.946809

    @Input
    def mTOW(self):
        """
        Aircraft maximum take off weight
        :Unit: [N]
        :rtype: float
        """
        return 422713.

    @Input
    def hCruise(self):
        """
        Aircraft cruise altitude
        :Unit: [m]
        :rtype: float
        """
        return 10000.

    @Input
    def tailType(self):
        """
        Tail type, could be "conventional", "cruciform" or "T tail"
        :Unit: [ ]
        :rtype: string
        """
        return 'T tail'

    @Part
    def wingbase(self):
        return Wing(maCruise=self.maCruise,
                    fuselageLength=self.fuselage.fuselageLength,
                    fuselageDiameter=self.fuselage.fuselageDiameter,
                    enginePos=self.enginebase.enginePos,
                    wingLoading=self.wingLoading,
                    mTOW=self.mTOW,
                    hCruise=self.hCruise)

    @Part
    def fuselage(self):
        return Fuselage(maCruise=self.maCruise)

    @Part
    def enginebase(self):
        return Engine(fuselageLength=self.fuselage.fuselageLength,
                      fuselageDiameter=self.fuselage.fuselageDiameter,
                      noseLength=self.fuselage.noseLength,
                      cylinderLength=self.fuselage.cylinderLength,
                      wingSpan=self.wingbase.span,
                      chord35=self.wingbase.chord35,
                      chord40=self.wingbase.chord40,
                      chord70=self.wingbase.chord70,
                      wingVertPos=self.wingbase.vertPos,
                      wingLongPos=self.wingbase.longPos,
                      dihedral=self.wingbase.dihedral,
                      sweepLE=self.wingbase.sweepLE,
                      tcRatio=self.wingbase.tcRatio)

    @Part
    def vtpbase(self):
        return Vtp(tailType=self.tailType,
                   surfaceWing=self.wingbase.surface,
                   cMACWing=self.wingbase.cMAC,
                   spanWing=self.wingbase.span,
                   fuselageLength=self.fuselage.fuselageLength,
                   posFraction=self.wingbase.posFraction,
                   conePos=self.fuselage.tailSectionCurves[1].center.y,
                   coneRadius=self.fuselage.tailSectionCurves[1].radius,
                   tlH=self.htpbase.tl)

    @Part
    def htpbase(self):
        return Htp(tailType=self.tailType,
                   sweep25Wing=self.wingbase.sweep25,
                   surfaceWing=self.wingbase.surface,
                   cMACWing=self.wingbase.cMAC,
                   spanWing=self.wingbase.span,
                   fuselageLength=self.fuselage.fuselageLength,
                   posFraction=self.wingbase.posFraction,
                   conePos=self.fuselage.tailSectionCurves[1].center.y,
                   coneRadius=self.fuselage.tailSectionCurves[1].radius,
                   tlV=self.vtpbase.tl,
                   spanV=self.vtpbase.span,
                   cMACyPosV=self.vtpbase.cMACyPos,
                   sweep25V=self.vtpbase.sweep25,
                   sweepLEV=self.vtpbase.sweepLE,
                   cMACV=self.vtpbase.cMAC)


if __name__ == '__main__':
    from parapy.gui import display

    obj = Aircraft()
    display(obj)

