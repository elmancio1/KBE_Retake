from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Handler.importer import Importer


class LandingGear(GeomBase):
    """
    Basic class Engine
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
    def wingPosition(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 'low wing'

    @Input(settable=settable)
    def twRatio(self):
        """
        Aircraft thrust to weight ratio
        :Unit: [ ]
        :rtype: float
        """
        return .29145

    @Input(settable=settable)
    def fuselageLength(self):
        """
        Aircraft fuselage length
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Fuselage',
                              VariableName='fuselageLength',
                              Default=30.0).getValue())

    @Input(settable=settable)
    def fuselageDiameter(self):
        """
        Aircraft fuselage diameter
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Fuselage',
                              VariableName='fuselageDiameter',
                              Default=4.0).getValue())

    @Input(settable=settable)
    def wingSpan(self):
        """
        Wing span, b
        :Unit: [m]
        :rtype: float
        """
        return 28.

    @Input(settable=settable)
    def chord35(self):
        """
        Wing chord at 35% of span, used in engines positioning
        :Unit: [m]
        :rtype: float
        """
        return 3.88

    @Input(settable=settable)
    def chord40(self):
        """
        Wing chord at 40% of span, used in engines positioning
        :Unit: [m]
        :rtype: float
        """
        return 3.7

    @Input(settable=settable)
    def chord70(self):
        """
        Wing chord at 70% of span, used in engines positioning
        :Unit: [m]
        :rtype: float
        """
        return 2.62

    @Input(settable=settable)
    def wingVertPos(self):
        """
        Wing root vertical position, depending on the selected aircraft configuration
        :Unit: [m]
        :rtype: float
        """
        return -1.69

    @Input(settable=settable)
    def wingLongPos(self):
        """
        Wing root longitudinal position, depending on the selected aircraft configuration
        :Unit: [m]
        :rtype: float
        """
        return 13.

    @Input(settable=settable)
    def dihedral(self):
        """
        Wing dihedral angle
        :Unit: [deg]
        :rtype: float
        """
        return 2.12

    @Input(settable=settable)
    def sweepLE(self):
        """
        Wing sweep angle at Leading Edge
        :Unit: [deg]
        :rtype: float
        """
        return 31.5

    @Input(settable=settable)
    def noseLength(self):
        """
        Aircraft nose length
        :Unit: [m]
        :rtype: float
        """
        return 5.13

    @Input(settable=settable)
    def cylinderLength(self):
        """
        Aircraft fuselage cylindrical section length
        :Unit: [m]
        :rtype: float
        """
        return 21.

    @Input(settable=settable)
    def tcRatio(self):
        """
        Airfoil profile thickness to chord ratio.
        :Unit: [m]
        :rtype: float
        """
        return 0.15

    # ### Attributes ##################################################################################################

    @Attribute
    def thrustTO(self):
        """
        Engine thrust at Take-Off
        :Unit: [N]
        :rtype: float
        """
        return self.twRatio * self.mTOW

    @Attribute
    def specificGenPower(self):
        """
        Specific gas generator power
        :Unit: [W]
        :rtype: float
        """
        return (self.TIT / 600) - 1.25

    @Attribute
    def massFlow(self):
        """
        Engine mass flow
        :Unit: [kg/s]
        :rtype: float
        """
        return self.thrustTO / (self.nEngine * self.a0) * (1 + self.bypassRatio) /\
            (sqrt(5 * self.etaNozzle * self.specificGenPower * (1 + self.etaMech * self.bypassRatio)))

    @Attribute
    def spinnerInletRatio(self):
        """
        Ratio between spinner and inlet diameter
        :Unit: [ ]
        :rtype: float
        """
        return 0.05 * (1 + 0.1 * self.rho0 * self.a0 / self.massFlow + 3 * self.bypassRatio / (1 + self.bypassRatio))

    @Attribute
    def inletDiameter(self):
        """
        Inlet diameter
        :Unit: [m]
        :rtype: float
        """
        return 1.65 * sqrt((self.massFlow / (self.rho0*self.a0) + 0.005) / (1 - self.spinnerInletRatio**2))

    @Attribute
    def spinnerDiameter(self):
        """
        Spinner diameter
        :Unit: [m]
        :rtype: float
        """
        return self.spinnerInletRatio * self.inletDiameter

    @Attribute
    def cowlLengthPar(self):
        """

        :Unit: [ ]
        :rtype: float
        """
        if self.cowlingType == "full":
            return 9.8
        elif self.cowlingType == "partial":
            return 7.8
        else:
            showwarning("Warning", "Please insert 'full' or 'partial' in cowling type input")
            return "Please insert 'full' or 'partial' in cowling type."

    @Attribute
    def dl(self):
        """

        :Unit: [ ]
        :rtype: float
        """
        if self.cowlingType == "full":
            return 0.05
        elif self.cowlingType == "partial":
            return 0.10
        else:
            return "Please insert 'full' or 'partial' in cowling type."

    @Attribute
    def phi(self):
        """

        :Unit: [ ]
        :rtype: float
        """
        if self.cowlingType == "full":
            return 1
        elif self.cowlingType == "partial":
            return self.cowlingPos
        else:
            return "Please insert 'full' or 'partial' in cowling type."

    @Attribute
    def beta(self):
        """

        :Unit: [ ]
        :rtype: float
        """
        if self.cowlingType == "full":
            return 0.35
        elif self.cowlingType == "partial":
            return 0.20
        else:
            return "Please insert 'full' or 'partial' in cowling type."

    @Attribute
    def nacelleLength(self):
        """
        Length of the engine nacelle
        :Unit: [m]
        :rtype: float
        """
        return self.cowlLengthPar * (self.dl + sqrt(self.massFlow *
                                                    (1 + 0.2 * self.bypassRatio) /
                                                    (self.rho0 * self.a0 * (1 + self.bypassRatio))))

    @Attribute
    def cowlLength(self):
        """
        Length of the engine cowling
        :Unit: [m]
        :rtype: float
        """
        return self.phi * self.nacelleLength

    @Attribute
    def nacelleDiameter(self):
        """
        Diameter of the engine nacelle
        :Unit: [m]
        :rtype: float
        """
        return self.inletDiameter + 0.06 * self.cowlLength + 0.03

    @Attribute
    def bypassDiameter(self):
        """
        Diameter of the engine bypass part
        :Unit: [m]
        :rtype: float
        """
        return self.nacelleDiameter * (1 - (self.phi**2)/3)

    @Attribute
    def generatorDiameter(self):
        """
        Diameter of the engine gas generator part
        :Unit: [m]
        :rtype: float
        """
        return self.bypassDiameter * (((0.089 * self.massFlow * self.bypassRatio / (self.rho0 * self.a0) + 4.5) /
                                       (0.067 * self.massFlow * self.bypassRatio / (self.rho0 * self.a0) + 5.8))**2)

    @Attribute
    def coreDiameter(self):
        """
        Diameter of the engine core
        :Unit: [m]
        :rtype: float
        """
        return self.generatorDiameter * 0.55

    @Attribute
    def nacelleDiameters(self):
        """
        Sequence of diameters of the engine nacelle part
        :Unit: [m]
        :rtype: sequence.float
        """
        return [self.inletDiameter, self.nacelleDiameter, self.bypassDiameter]

    @Attribute
    def nacellePos(self):
        """

        :Unit: [ ]
        :rtype:
        """
        return [0, self.beta * self.nacelleLength, self.cowlLength]

    @Attribute
    def coreDiameters(self):
        """
        Sequence of diameters of the engine core part
        :Unit: [m]
        :rtype: sequence.float
        """
        return [0.01 * self.spinnerDiameter, 0.8 * self.generatorDiameter,
                0.85 * self.generatorDiameter, 0.9 * self.generatorDiameter,
                self.generatorDiameter, 0.95 * self.generatorDiameter,
                0.90 * self.generatorDiameter, 0.85 * self.generatorDiameter,
                self.coreDiameter]

    @Attribute
    def corePos(self):
        """

        :Unit: [ ]
        :rtype:
        """
        return self.nacelleLength / (len(self.coreDiameters))

    @Attribute
    def latPos(self):
        """
        Engine lateral position, depending on the number of engine and their positions
        :Unit: [m]
        :rtype:
        """
        if self.nEngine == 2 and self.enginePos == 'wing':
            return [self.wingSpan/2 * 0.35]
        elif self.nEngine == 4 and self.enginePos == 'wing':
            return [self.wingSpan/2 * 0.4, self.wingSpan/2 * 0.7]
        elif self.nEngine == 2 and self.enginePos == 'fuselage':
            return [0.75 * self.nacelleDiameter + self.fuselageDiameter/2]
        else:
            showwarning("Warning", "Please choose 2 or 4 engines, or 2 engines for the fuselage mounted option")
            return 'Error, choose 2 or 4 engines, or 2 engines for the fuselage mounted option'