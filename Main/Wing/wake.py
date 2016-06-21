from __future__ import division
import os, sys
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import askopenfilename
import Tkinter, Tkconstants, tkFileDialog


class Wake(GeomBase):
    """
    Basic class for the wing wake
    """

    window = Tk()
    window.wm_withdraw()

    # ### Input required from wing ################################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from wing
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def cMACWing(self):
        """
        Wing Mean aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return 3.67

    @Input(settable=settable)
    def pointMAC(self):
        """
        Point representing MAC quarter chord
        :Unit: [ ]
        :rtype: Point
        """
        return Point(5.76, -1.46, 17.53)

    # ### Attributes ##################################################################################################

    @Attribute
    def xCoord(self):
        """
        Set of x coordinates to represent the wake wing function
        :Unit: [ ]
        :rtype: float
        """
        return [1.2 + (5 - 1.2) / 100 * i for i in range(101)]

    @Attribute
    def yUp(self):
        """
        Set of y coordinates to represent the upper line of the wake wing function
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_1 = []
        for i in self.xCoord:
            y_1.append(Point(self.pointMAC.x,
                             self.pointMAC.y + float((.0072 * i**3 - .1016 * i**2 + .7088 * i - .0818) * self.cMACWing),
                             self.pointMAC.z + float(i) * self.cMACWing))
        return y_1

    @Attribute
    def yMid(self):
        """
        Set of y coordinates to represent the middle line of the wake wing function
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_2 = []
        for i in self.xCoord:
            y_2.append(Point(self.pointMAC.x,
                             self.pointMAC.y + float((-.0002 * i**3 - .0063 * i**2 + .1939 * i - .094) * self.cMACWing),
                             self.pointMAC.z + float(i) * self.cMACWing))
        return y_2

    @Attribute
    def yMidRev(self):
        """
        Reverse set of y coordinates of the middle line of the wake wing function, to make possible the polygon
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return list(reversed(self.yMid))

    @Attribute
    def yBot(self):
        """
        Set of y coordinates to represent the bottom line of the wake wing function
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_3 = []
        for i in self.xCoord:
            y_3.append(Point(self.pointMAC.x,
                             self.pointMAC.y + float((-.002 * i**3 + .0304 * i**2 - .1642 * i + .0882) * self.cMACWing),
                             self.pointMAC.z + float(i) * self.cMACWing))
        return y_3

    @Attribute
    def pointsDanger(self):
        """
        Points representing the danger part of wing wake
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return self.yUp + self.yMidRev + [self.yUp[0]]

    @Attribute
    def pointsSafer(self):
        """
        Points representing the safer (lower) part of wing wake
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return self.yBot + self.yMidRev + [self.yBot[0]]

    # ###### Parts ####################################################################################################

    @Part
    def curveDanger(self):
        """
        Curve representing the danger part of wing wake
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return PolygonalFace(self.pointsDanger,
                             color='red',
                             transparency=.6,
                             hidden=False)

    @Part
    def curveSafer(self):
        """
        Curve representing the safer (lower) part of wing wake
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return PolygonalFace(self.pointsSafer,
                             color='orange',
                             transparency=.6,
                             hidden=False)


if __name__ == '__main__':
    from parapy.gui import display

    obj = Wake()
    display(obj)
