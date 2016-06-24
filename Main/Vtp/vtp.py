from __future__ import division
import os, sys
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import askopenfilename
from Main.Airfoil.airfoil import Airfoil
from Handler.vtpCalc import VtpCalc
from Handler.xFoil import Xfoil
from Input import Airfoils
import Tkinter, Tkconstants, tkFileDialog


class Vtp(GeomBase):
    """
    Basic class Vertical tail plane
    """
    defaultPath = os.path.dirname(Airfoils.__file__) + '\NACA_0012.dat'  # From the Airfoil folder path add name of
    # default File

    @Input
    def xfoilAnalysis(self):
        """
        Boolean input to choose to start the xfoil analysis

        :rtype: boolean
        """
        return True

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
    def rcr(self):
        """
        Rudder chord ratio over root chord
        :Unit: [ ]
        :rtype: float
        source: Raymer
        """
        return .35

    @Input
    def aspectRatio(self):
        """
        Vertical tail plane aspect ratio, b^2 / S
        :Unit: [ ]
        :rtype: float
        source: KBE assignment support material
        """
        if self.tailType == 'conventional':
            return 1.9
        else:
            return 1.35

    @Input
    def taperRatio(self):
        """
        Vertical tail plane taper ratio, tip chord / root chord
        :Unit: [ ]
        :rtype: float
        source: KBE assignment support material
        """
        if self.tailType == 'conventional':
            return 0.3
        else:
            return 0.7

    @Input
    def sweep25(self):
        """
        Vertical tail plane sweep at quarter chord
        :Unit: [deg]
        :rtype: float
        source: KBE assignment support material
        """
        return 37.5

    @Input
    def vc(self):
        """
        Vertical tail volume coefficient, based on type and dimension of designed aircraft
        :Unit: [ ]
        :rtype: float
        source: http://adg.stanford.edu/aa241/stability/taildesign.html
        """
        return 0.0325 + 0.3375 * (self.fuselageDiameter**2 * self.fuselageLength) / (self.surfaceWing * self.spanWing)

    @Input
    def visual(self):
        """
        Define the visualization of the visual checks, it could be either True or False
        :Unit: [ ]
        :rtype: string
        """
        return False

    @Input
    def rudderCheck(self):
        """
        Hidden the visualization of check for rudder blanketing
        :Unit: [ ]
        :rtype: string
        """
        return False

    @Input
    def perc(self):
        """
        Span percentage for xFoil plan, user requested
        :Unit: [ ]
        :rtype: float
        """
        return .5

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
    def fuselageDiameter(self):
        """
        Aircraft fuselage diameter
        :Unit: [m]
        :rtype: float
        """
        return 4.

    @Input(settable=settable)
    def conePos(self):
        """
        Aircraft tail cone most upper point vertical position
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
    def tlH(self):
        """
        Horizontal tail plane arm
        :Unit: [m]
        :rtype: float
        """
        return 17.58

    @Input(settable=settable)
    def crH(self):
        """
        Horizontal tail plane root chord
        :Unit: [m]
        :rtype: float
        """
        return 2.6

    @Input(settable=settable)
    def longPosH(self):
        """
        Horizontal tail plane longitudinal position
        :Unit: [m]
        :rtype: float
        """
        return 33.16

    @Input(settable=settable)
    def vertPosH(self):
        """
        Horizontal tail plane vertical position
        :Unit: [m]
        :rtype: float
        """
        return 1.05

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
        # TODO: creare la funzione esponenziale
        return .0001 * self.fuselageLength

    @Attribute
    def tl(self):
        """
        Vertical tail plane arm
        :Unit: [m]
        :rtype: float
        """

        # TODO: la vertical e veramente enorme... la scia si trova nella posizione corretta?

        if self.tailType == 'conventional':
            tl = self.tlH / 2.  # first guess for vertical tail arm
            check = 0.  # first guess for the rudder area check, to start the cycle
            while check < 2/3:
                tl = tl + self.tlDecrement
                calctail = VtpCalc(tl=tl,
                                   rcr=self.rcr,
                                   vc=self.vc,
                                   tailType=self.tailType,
                                   surfaceWing=self.surfaceWing,
                                   cMACWing=self.cMACWing,
                                   spanWing=self.spanWing,
                                   fuselageLength=self.fuselageLength,
                                   posFraction=self.posFraction,
                                   conePos=self.conePos,
                                   crH=self.crH,
                                   longPosH=self.longPosH,
                                   vertPosH=self.vertPosH)
                check = calctail.rudderBlanketed  # portion of the rudder blanketed
            return tl
        else:
            tl = self.fuselageLength  # first guess for tail arm
            TR = self.taperRatio
            cR = self.cMACWing  # first guess for the tail root chord
            posYMAC = 10.  # first guess for the tail MAC position

            while (self.fuselageLength - (self.wingAC + tl + 0.75*cR - posYMAC * tan(radians(self.sweep25)))) < 0:
                tl = tl - self.tlDecrement
                cR = 2/(1 + TR) * sqrt((self.vc * self.spanWing * self.surfaceWing)/(self.aspectRatio * tl))
                posYMAC = (1+2*TR)/((1+TR)*6) * sqrt((self.aspectRatio * self.vc * self.spanWing * self.surfaceWing)/tl)
            return tl

    @Attribute
    def surface(self):
        """
        Vertical tail reference surface
        :Unit: [m^2]
        :rtype: float
        """
        return self.vc * self.surfaceWing * self.spanWing / self.tl

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
        return self.conePos

    @Attribute
    def rudderFree(self):
        """
        Percentage of rudder area free of Htp wake
        :Unit: [ ]
        :rtype: float
        """
        if self.check.faces == []:
            return 0
        else:
            return self.check.faces[0].area / self.rudder.area

    @Attribute
    def transparency(self):
        """
        Enable transparent tail to see the check on the rudder
        :Unit: [ ]
        :rtype: string
        """
        if self.rudderCheck:
            return 0.6
        else:
            return 0

    @Attribute
    def pointsWakeHtp(self):
        """
        List of points representing the horizontal tail plane wake after separation flow on it
        :Unit: []
        :rtype: Points
        """
        return [Point(0, self.vertPosH, self.longPosH),
                Point(0, self.vertPosH + self.span, self.longPosH + self.span * tan(pi/6)),
                Point(0, self.vertPosH + self.span, self.longPosH + self.crH + self.span * tan(pi/3)),
                Point(0, self.vertPosH, self.longPosH + self.crH),
                Point(0, self.vertPosH, self.longPosH)]

    @Attribute
    def pointsRudder(self):
        """
        List of points representing the vertical tail rudder
        :Unit: []
        :rtype: Points
        """
        return [Point(0, self.vertPos, self.longPos + (1-self.rcr)*self.chordRoot),
                Point(0, self.curveTipPos.position.location.y, self.curveTipPos.position.location.z + (1-self.rcr)*self.chordTip),
                Point(0, self.curveTipPos.position.location.y, self.curveTipPos.position.location.z + self.chordTip),
                Point(0, self.vertPos, self.longPos + self.chordRoot),
                Point(0, self.vertPos, self.longPos + (1-self.rcr)*self.chordRoot)]

    # ###### Parts ####################################################################################################

    @Part
    def curveRoot(self):
        """
        Root airfoil curve

        :rtype:
        """
        return Airfoil(airfoilData=self.airfoilRoot,
                       chord=0.99*self.chordRoot,
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
        Vertical tail root airfoil placed in the final position

        :rtype:
        """
        return TransformedCurve(curve_in=self.curveRoot.crv,
                                from_position=XOY,
                                to_position=translate(rotate90(XOY, 'z_'),
                                                      'x_', self.vertPos,
                                                      'z', self.longPos),
                                hidden=True)

    @Part
    def curveTipPos(self):
        """
        Vertical tail tip airfoil placed in the final position

        :rtype:
        """
        return TransformedCurve(curve_in=self.curveTip.crv,
                                from_position=XOY,
                                to_position=translate(rotate90(XOY, 'z_'),
                                                      'x_', self.vertPos + self.span,
                                                      'z', self.longPos + self.span * tan(radians(self.sweepLE))),
                                hidden=True)

    @Part
    def tail(self):
        """
        Vertical tail solid representation

        :rtype:
        """
        return LoftedSolid([self.curveRootPos, self.curveTipPos],
                           transparency=self.transparency)

    @Part
    def htpWake(self):
        """
        Horizontal tail plane wake 3D representation

        :rtype:
        """
        return PolygonalFace(self.pointsWakeHtp,
                             color='red',
                             transparency=.4,
                             hidden=not self.rudderCheck)

    @Part
    def rudder(self):
        """
        Vertical tail plane rudder 3D representation

        :rtype:
        """
        return PolygonalFace(self.pointsRudder,
                             color='blue',
                             transparency=.5,
                             hidden=not self.rudderCheck)

    @Part
    def check(self):
        """
        Intersection between rudder and htp wake, for the spin resistance check

        :rtype:
        """
        return Subtracted(shape_in=self.rudder, tool=self.htpWake,
                          color='green',
                          transparency=.2,
                          hidden=not self.rudderCheck)

    @Part
    def planeMAC(self):
        """
        Intersecting plane at MAC position on tail plane

        :rtype:
        """
        return Plane(Point(0, self.vertPos + self.cMACyPos, 0), Vector(0, 1, 0),
                     hidden=True)

    @Part
    def MAC(self):
        """
        MAC representation on tail plane

        :rtype:
        """
        return IntersectedShapes(shape_in=self.tail,
                                 tool=self.planeMAC,
                                 color='red',
                                 hidden=not self.visual)

    @Part
    def AC(self):
        """
        Aerodynamic center representation at quarter of MAC on tail plane

        :rtype:
        """
        return Sphere(radius=abs(self.curveRoot.maxY),
                      position=Point(self.MAC.edges[0].point1.x,
                                     self.MAC.edges[0].point1.y,
                                     self.MAC.edges[0].point1.z - 0.75*self.cMAC),
                      color='Red',
                      hidden=not self.visual)

    # ###### xFoil ################################################################################################

    @Part
    def xfoil(self):
        return Xfoil(perc=self.perc,
                     sweepLE=self.sweepLE,
                     chordRoot=self.chordRoot,
                     chordTip=self.chordTip,
                     span=self.span,
                     longPos=self.longPos,
                     vertPos=self.vertPos,
                     loft=self.tail.solids[0],
                     vertical=True,
                     hidden=not self.xfoilAnalysis)

if __name__ == '__main__':
    from parapy.gui import display

    obj = Vtp()
    display(obj)
