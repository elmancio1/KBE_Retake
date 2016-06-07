from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Main.Airfoil.airfoil import Airfoil
from tkFileDialog import askopenfilename


class WingEx(GeomBase):
    """
    Basic class Wing
    """


    @Input
    def newAirfoil(self):
        """
        Boolean input to choose between default path or user chosen.

        :rtype: boolean
        """
        return False

    @Attribute
    def airfoilRoot(self):
        """
        Path to airfoil file for wing root. It can either use a default path or letting the user choose the airfoil file.

        :rtype: string
        """

        if not self.newAirfoil:

            return '..\Input\Airfoils\NACA_0012.dat'
        else:
            def callback():
                name = askopenfilename()
                return name
            filePath = callback()
            errmsg = 'Error!'
            Button(text='File Open', command=callback).pack(fill=X)

            return str(filePath)

    @Attribute
    def airfoilTip(self):
        """
        Path to airfoil file for wing tip. It can either use a default path or letting the user choose the airfoil file.

        :rtype: string
        """

        if not self.newAirfoil:

            return '..\Input\Airfoils\NACA_0012.dat'
        else:
            def callback():
                name = askopenfilename()
                return name

            filePath = callback()
            errmsg = 'Error!'
            Button(text='File Open', command=callback).pack(fill=X)

            return str(filePath)

    @Input
    def aspectRatio(self):
        """
        Wing aspect ratio, b^2 / S
        :Unit: [ ]
        :rtype: float
        """
        return 8.4

    @Input
    def maTechnology(self):
        """
        Wing airfoil Mach technology parameter, higher values mean higher possible Mach
        :Unit: [ ]
        :rtype: float
        """
        return 0.935

    @Input
    def sweep25(self):
        """
        Wing sweep angle calculated at quarter chord
        :Unit: [deg]
        :rtype: float
        """
        if self.maCruise <= 0.7:
            return acos(1.0)
        else:
            return degrees(acos(0.75 * self.maTechnology / self.maDD))

    @Input
    def wingPosition(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 'low wing'

    @Input
    def dihedral(self):
        """
        Wing dihedral angle
        :Unit: [deg]
        :rtype: float
        """
        if self.wingPosition == 'low wing':
            return 3 - self.sweep25 / 10 + 2
        elif self.wing_position == 'high wing':
            return 3 - self.sweep25 / 10 - 2

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ###################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from wing
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def maCruise(self):
        """
        Aircraft Mach cruise number
        :Unit: [ ]
        :rtype: float
        """
        return 0.77

    @Input(settable=settable)
    def wingLoading(self):
        """
        Aircraft wing loading
        :Unit: [kg / m^2]
        :rtype: float
        """
        return 4496.946809

    @Input(settable=settable)
    def mTOW(self):
        """
        Aircraft maximum take off weight
        :Unit: [N]
        :rtype: float
        """
        return 422713.

    @Input(settable=settable)
    def hCruise(self):
        """
        Aircraft cruise altitude
        :Unit: [m]
        :rtype: float
        """
        return 10000.

    # ### Attributes ####################################################################################

    @Attribute
    def maDD(self):
        """
        Aircraft Mach Dive Divergence
        :Unit: [ ]
        :rtype: float
        """
        return self.maCruise + 0.03

    @Attribute
    def surface(self):
        """
        Wing reference area
        :Unit: [m^2]
        :rtype: float
        """
        return self.mTOW / self.wingLoading

    @Attribute
    def taperRatio(self):
        """
        Wing taper ratio, tip chord over root chord
        :Unit: [ ]
        :rtype: float
        """
        return 0.2 * (2 - radians(self.sweep25))

    @Attribute
    def sweep50(self):
        """
        Wing sweep angle calculated at half chord
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((0.5 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def sweepLE(self):
        """
        Wing sweep angle calculated at Leading Edge
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((0 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def sweepTE(self):
        """
        Wing sweep angle calculated at Trailing Edge
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((1 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def span(self):
        """
        Wing span, b
        :Unit: [m]
        :rtype: float
        """
        return sqrt(self.surface * self.aspectRatio)

    @Attribute
    def chordRoot(self):
        """
        Wing root chord
        :Unit: [m]
        :rtype: float
        """
        return 2 * self.surface / ((1 + self.taperRatio) * self.span)

    @Attribute
    def chordTip(self):
        """
        Wing tip chord
        :Unit: [m]
        :rtype: float
        """
        return self.taperRatio * self.chordRoot

    @Attribute
    def cMAC(self):
        """
        Wing Mean aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return (2/3) * self.chordRoot * (1 + self.taperRatio + self.taperRatio**2) / (1 + self.taperRatio)

    @Attribute
    def cMACyPos(self):
        """
        Wing Mean aerodynamic Chord span position
        :Unit: [m]
        :rtype: float
        """
        return self.span * (1 + 2*self.taperRatio) / ((1 + self.taperRatio)*6)

    @Attribute
    def pressureCruise(self):
        """
        Static pressure at cruise altitude
        :Unit: [Pa]
        :rtype: float
        """
        p0 = 101325.  # static pressure at sea level, [Pa]
        a = 0.0065  # temperature gradient, [K/m]
        T0 = 288.  # temperature at sea level, [K]
        g = 9.81  # gravitational acceleration, [m/s^2]
        R = 287.  # specific gas constant, [J/kg K]
        return p0 * (1 - a * self.hCruise / T0)**(g / (R * a))

    @Attribute
    def dynamicPressure(self):
        """
        Dynamic pressure at aircraft speed and altitude
        :Unit: [Pa]
        :rtype: float
        """
        k = 1.4  # heat capacity ratio for air, [-]
        return 0.5 * self.pressureCruise * self.maCruise**2 * k

    @Attribute
    def clCruise(self):
        """
        Lift coefficient of aircraft in cruise condition
        :Unit: [ ]
        :rtype: float
        """
        return self.wingLoading / self.dynamicPressure

    @Attribute
    def tcRatio(self):
        """
        Wing average thickness to chord ratio
        :Unit: [ ]
        :rtype: float
        """
        return min(0.18, (((cos(radians(self.sweep50))**3) * (self.maTechnology - self.maDD *
                            cos(radians(self.sweep50)))) - 0.115 * self.clCruise**1.5) /
                            cos(radians(self.sweep50))**2)

    @Part
    def curveRoot(self):
        """
        Root airfoil curve
        :Unit: [ ]
        :rtype:
        """
        return Airfoil(airfoilData=self.airfoilRoot,
                       chord=self.chordRoot,
                       position=self.location.translate('x',
                                                        self.cMAC))

    @Part
    def curveTip(self):
        """
        Tip airfoil curve
        :Unit: [ ]
        :rtype:
        """
        return Airfoil(airfoilData=self.airfoilTip,
                       chord=self.chordTip)

if __name__ == '__main__':
    from parapy.gui import display

    obj = WingEx()
    display(obj)
