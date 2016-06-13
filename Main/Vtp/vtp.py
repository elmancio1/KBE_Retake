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



class Vtp(GeomBase):
    """
    Basic class Vertical tail plane
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
    def aspectRatio(self):
        """
        Wing aspect ratio, b^2 / S
        :Unit: [ ]
        :rtype: float
        """
        return 8.4

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ################################################################################

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

    # ### Attributes ##################################################################################################

    @Attribute
    def maDD(self):
        """
        Aircraft Mach Dive Divergence
        :Unit: [ ]
        :rtype: float
        """
        return self.maCruise + 0.03

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
        Wing root airfoil placed in the final wing position

        :rtype:
        """
        return TranslatedCurve(curve_in=self.curveRoot.crv,
                               displacement=Vector(0, self.vertPos, self.longPos),
                               hidden=True)

    @Part
    def curveTipPos(self):
        """
        Wing tip airfoil placed in the final wing position

        :rtype:
        """
        return TranslatedCurve(curve_in=self.curveTip.crv,
                               displacement=Vector(self.span/2,
                                                   self.vertPos + self.span/2 * tan(radians(self.dihedral)),
                                                   self.longPos + self.span/2 * tan(radians(self.sweepLE))),
                               hidden=True)

#    @Part
#    def curveRootPos2(self):
#        return TransformedCurve(curve_in=self.curveRoot.crv,
#                                from_position=self.curveRoot.position,
#                                to_position=translate(self.curveTip.position,
#                                                      'z', self.longPos,
#                                                      'y', self.vertPos))

    @Part
    def rightWing(self):
        """
        Right wing solid representation

        :rtype:
        """
        return LoftedSolid([self.curveRootPos, self.curveTipPos])

    @Part
    def leftWing(self):
        """
        Right wing solid representation

        :rtype:
        """
        return MirroredShape(shape_in=self.rightWing,
                             reference_point=self.rightWing.position,
                             vector1=self.rightWing.position.Vy,
                             vector2=self.rightWing.position.Vz)

if __name__ == '__main__':
    from parapy.gui import display

    obj = Vtp()
    display(obj)
