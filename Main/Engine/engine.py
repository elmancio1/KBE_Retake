from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Handler.importer import Importer


class Engine(GeomBase):
    """
    Basic class Engine
    """

    @Input
    def bypassRatio(self):
        """
        Engine bypass-Ratio
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='BPR',
                              Default=3.0).getValue())

    @Input
    def a0(self):
        """
        Speed of sound at sea level - standard conditions
        :Unit: [m/s]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='a0',
                              Default=340.3).getValue())

    @Input
    def rho0(self):
        """
        Air density at sea level - standard conditions
        :Unit: [kg/m^3]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='rho0',
                              Default=1.225).getValue())

    @Input
    def TIT(self):
        """
        Temperature at Inlet of Turbine
        :Unit: [K]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='TIT',
                              Default=1375.).getValue())

    @Input
    def nEngine(self):
        """
        Number of engine of the aircraft
        :Unit: [ ]
        :rtype: integer
        """
        return float(Importer(Component='Engine',
                              VariableName='nEngine',
                              Default=2.).getValue())

    @Input
    def etaNozzle(self):
        """
        Efficiency of engine nozzle
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='etaNozzle',
                              Default=.97).getValue())

    @Input
    def etaMech(self):
        """
        Mechanical efficiency of engine
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='etaMech',
                              Default=.75).getValue())

    @Input
    def cowlingType(self):
        """
        Cowling type of the engine, could be either "full" or "partial"
        :Unit: [ ]
        :rtype: string
        """
        return str(Importer(Component='Engine',
                               VariableName='cowling Type',
                               Default='partial').getValue())

    @Input
    def cowlingPos(self):
        """
        Cowling position of the engine, depends on the type of cowling
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='cowling Position',
                              Default=.75).getValue())

    @Input
    def enginePos(self):
        """
        Engine position, could be either "wing" or "fuselage" mounted
        :Unit: [ ]
        :rtype: float
        """
        return str(Importer(Component='Engine',
                               VariableName='engine Position',
                               Default='wing').getValue())

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ################################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from engine
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def mTOW(self):
        """
        Aircraft maximum Take-Off Weight
        :Unit: [N]
        :rtype: float
        """
        return 422713.

    @Input(settable=settable)
    def twRatio(self):
        """
        Aircraft thrust to weight ratio
        :Unit: [ ]
        :rtype: float
        """
        return .29145

    # ### Attributes ##################################################################################################

    @Attribute
    def thrustTO(self):
        """
        Engine thrust at Take-Off
        :Unit: [N]
        :rtype: float
        """
        return self.twRatio * self.mTOW


if __name__ == '__main__':
    from parapy.gui import display

    obj = Engine()
    display(obj)