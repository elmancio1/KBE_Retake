from __future__ import division
import os, sys
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import askopenfilename
from Main.Airfoil.airfoil import Airfoil
from Input import Airfoils
import Tkinter, Tkconstants, tkFileDialog


class Htp(GeomBase):
    """
    Basic class horizontal tail plane
    """
    defaultPath = os.path.dirname(Airfoils.__file__) + '\NACA_0012.dat'  # From the Airfoil folder path add name of
    # default File

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
        Path to airfoil file for wing root. It can either use a default path or letting the user choose the airfoil file

        :rtype: string
        """

        if not self.newAirfoil:

            return self.defaultPath
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

            return self.defaultPath
        else:
            def callback():
                name = askopenfilename()
                return name

            filePath = callback()
            errmsg = 'Error!'
            Button(text='File Open', command=callback).pack(fill=X)

            return str(filePath)

    @Input
    def hVertPerc(self):
        """
        Horizontal height of htp in percentage with respect to vtp span
        :Unit: [ ]
        :rtype: float
        """
        if self.tailType == 'T tail':
            return 1.
        else:
            return .75

    @Input
    def aspectRatio(self):
        """
        Horizontal tail plane aspect ratio, b^2 / S
        :Unit: [ ]
        :rtype: float
        source: KBE assignment support material
        """
        return 5.

    @Input
    def taperRatio(self):
        """
        Horizontal tail plane taper ratio, tip chord / root chord
        :Unit: [ ]
        :rtype: float
        source: KBE assignment support material
        """
        return .4

    @Input
    def sweep25(self):
        """
        Horizontal tail plane sweep at quarter chord
        :Unit: [deg]
        :rtype: float
        source: KBE assignment support material
        """
        return 10 + self.sweep25Wing

    @Input
    def vc(self):
        """
        Horizontal tail volume coefficient
        :Unit: [ ]
        :rtype: float
        source: KBE assignment support material
        """
        return 1.

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ################################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from wing
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
    def tailType(self):
        """
        Tail type, could be "conventional", "cruciform" or "T tail"
        :Unit: [ ]
        :rtype: string
        """
        return 'T tail'

    @Input(settable=settable)
    def sweep25Wing(self):
        """
        Wing sweep angle calculated at quarter chord
        :Unit: [deg]
        :rtype: float
        """
        return 28.75

    @Input(settable=settable)
    def surfaceWing(self):
        """
        Wing reference area
        :Unit: [m^2]
        :rtype: float
        """
        return 94.

    @Input(settable=settable)
    def cMACWing(self):
        """
        Wing Mean aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return 3.67

    @Input(settable=settable)
    def spanWing(self):
        """
        Wing span, b
        :Unit: [m]
        :rtype: float
        """
        return 28.

    @Input(settable=settable)
    def fuselageLength(self):
        """
        Aircraft fuselage length
        :Unit: [m]
        :rtype: float
        """
        return 36.

    @Input(settable=settable)
    def conePos(self):
        """
        Aircraft tail cone vertical position
        :Unit: [m]
        :rtype: float
        """
        return 2.

    @Input(settable=settable)
    def posFraction(self):
        """
        Wing position fraction of the fuselage, due to engine position
        :Unit: [m]
        :rtype: float
        """
        return .5

    @Input(settable=settable)
    def tlV(self):
        """
        Vertical tail arm
        :Unit: [m]
        :rtype: float
        """
        return 15.96

    @Input(settable=settable)
    def spanV(self):
        """
        Vertical tail span
        :Unit: [m]
        :rtype: float
        """
        return 4.3

    @Input(settable=settable)
    def cMACyPosV(self):
        """
        Vertical tail MAC position
        :Unit: [m]
        :rtype: float
        """
        return 1.

    @Input(settable=settable)
    def sweep25V(self):
        """
        Vertical tail sweep, evaluated at quarter chord
        :Unit: [deg]
        :rtype: float
        """
        return 37.5

    @Input(settable=settable)
    def sweepLEV(self):
        """
        Vertical tail sweep, evaluated at leading edge
        :Unit: [deg]
        :rtype: float
        """
        return 42.

    @Input(settable=settable)
    def cMACV(self):
        """
        Vertical tail Mean Aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return 3.2

    # ### Attributes ##################################################################################################

    @Attribute
    def wingAC(self):
        """
        Wing aerodynamic center position, with respect to the fuselage nose
        :Unit: [m]
        :rtype: float
        """
        return self.posFraction * self.fuselageLength

    @Attribute
    def tlDecrement(self):
        """
        Tail arm decrement
        :Unit: [m]
        :rtype: float
        """
        return .0001 * self.fuselageLength

    @Attribute
    def tl(self):
        """
        Vertical tail arm
        :Unit: [m]
        :rtype: float
        """
        if self.tailType == 'conventional':
            tl = self.fuselageLength  # first guess for tail arm
            TR = self.taperRatio
            cR = self.cMACWing  # first guess for the tail root chord
            posYMAC = 10.  # first guess for the tail MAC position

            while (self.fuselageLength - (self.wingAC + tl + 0.75*cR - posYMAC * tan(radians(self.sweep25)))) < 0:
                tl = tl - self.tlDecrement
                cR = 2/(1 + TR) * sqrt((self.vc * self.cMACWing * self.surfaceWing)/(self.aspectRatio * tl))
                posYMAC = (1+2*TR)/((1+TR)*6) * sqrt((self.aspectRatio * self.vc * self.cMACWing * self.surfaceWing)/tl)
            return tl

        else:
            res = 1  # first guess for residual, to start the cycle
            TR = self.taperRatio
            tl = self.tlV  # first guess for horizontal tail arm
            while res > 0.001:

                cR = 2 / (1 + TR) * sqrt((self.vc * self.cMACWing * self.surfaceWing) / (self.aspectRatio * tl))
                posYMAC = (1 + 2 * TR) / ((1 + TR) * 6) * \
                          sqrt((self.aspectRatio * self.vc * self.cMACWing * self.surfaceWing) / tl)
                tlNew = self.tlV - .25*self.cMACV + 0.25*cR + posYMAC * tan(radians(self.sweep25)) + \
                       (self.hVertPerc * self.spanV - self.cMACyPosV) * tan(radians(self.sweepLEV))
                res = (tlNew - tl)**2
                tl = tlNew

            return tl

    @Attribute
    def surface(self):
        """
        Vertical tail reference surface
        :Unit: [m^2]
        :rtype: float
        """
        return self.vc * self.surfaceWing * self.cMACWing / self.tl

    @Attribute
    def span(self):
        """
        Vertical tail span, b
        :Unit: [m]
        :rtype: float
        """
        return sqrt(self.surface * self.aspectRatio)

    @Attribute
    def chordRoot(self):
        """
        Vertical tail root chord
        :Unit: [m]
        :rtype: float
        """
        return 2 * self.surface / ((1 + self.taperRatio) * self.span)

    @Attribute
    def chordTip(self):
        """
        Vertical tail tip chord
        :Unit: [m]
        :rtype: float
        """
        return self.taperRatio * self.chordRoot

    @Attribute
    def cMAC(self):
        """
        Vertical tail Mean Aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return (2/3) * self.chordRoot * (1 + self.taperRatio + self.taperRatio**2) / (1 + self.taperRatio)

    @Attribute
    def cMACyPos(self):
        """
        Vertical tail Mean Aerodynamic Chord position
        :Unit: [m]
        :rtype: float
        """
        return self.span * (1 + 2*self.taperRatio) / ((1 + self.taperRatio)*6)

    @Attribute
    def sweep50(self):
        """
        Vertical tail sweep angle calculated at half chord
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((0.5 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def sweepLE(self):
        """
        Vertical tail sweep angle calculated at Leading Edge
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((0 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def sweepTE(self):
        """
        Vertical tail sweep angle calculated at Trailing Edge
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((1 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def longPos(self):
        """
        Vertical tail root longitudinal position, in order to have the calculated tail arm
        :Unit: [m]
        :rtype: float
        """
        return self.wingAC + self.tl - .25*self.chordRoot - self.cMACyPos * tan(radians(self.sweep25))

    @Attribute
    def vertPos(self):
        """
        Vertical tail root vertical position
        :Unit: [m]
        :rtype: float
        """
        if self.tailType == 'conventional':
            return self.conePos
        else:
            return self.conePos + self.spanV * self.hVertPerc

    # ###### Parts ####################################################################################################

    @Part
    def curveRoot(self):
        """
        Root airfoil curve

        :rtype:
        """
        return Airfoil(airfoilData=self.airfoilRoot,
                       chord=self.chordRoot,
                       hidden=True)

    @Part
    def curveTip(self):
        """
        Tip airfoil curve

        :rtype:
        """
        return Airfoil(airfoilData=self.airfoilTip,
                       chord=self.chordTip,
                       hidden=True)

    @Part
    def curveRootPos(self):
        """
        Horizontal tail root airfoil placed in the final position

        :rtype:
        """
        return TranslatedCurve(curve_in=self.curveRoot.crv,
                               displacement=Vector(0, self.vertPos, self.longPos),
                               hidden=True)

    @Part
    def curveTipPos(self):
        """
        Horizontal tail tip airfoil placed in the final position

        :rtype:
        """
        return TranslatedCurve(curve_in=self.curveTip.crv,
                               displacement=Vector(self.span / 2,
                                                   self.vertPos,
                                                   self.longPos + self.span / 2 * tan(radians(self.sweepLE))),
                               hidden=True)

#    @Part
#    def curveRootPos2(self):
#        return TransformedCurve(curve_in=self.curveRoot.crv,
#                                from_position=self.curveRoot.position,
#                                to_position=translate(self.curveTip.position,
#                                                      'z', self.longPos,
#                                                      'y', self.vertPos))

    @Part
    def rightTail(self):
        """
        Right horizontal tail solid representation

        :rtype:
        """
        return LoftedSolid([self.curveRootPos, self.curveTipPos])

    @Part
    def leftTail(self):
        """
        Left horizontal tail solid representation

        :rtype:
        """
        return MirroredShape(shape_in=self.rightTail,
                             reference_point=self.rightTail.position,
                             vector1=self.rightTail.position.Vy,
                             vector2=self.rightTail.position.Vz)

if __name__ == '__main__':
    from parapy.gui import display

    obj = Htp()
    display(obj)
