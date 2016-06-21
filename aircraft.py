from __future__ import division
from parapy.geom import *
from parapy.core import *
from Handler.importer import Importer
from Input import Files
from math import *
import Tkinter
import tkMessageBox
from tkMessageBox import *
from Main.Wing.wing import Wing
from Main.Fuselage.fuselage import Fuselage
from Main.Engine.engine import Engine
from Main.Vtp.vtp import Vtp
from Main.Htp.htp import Htp
from Main.LandingGear.landingGear import LandingGear
from Main.Analysis.evaluations import Evaluations
import tkFileDialog
import os


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
                              VariableName='M cruise',
                              Default=0.77,
                              Path=self.filePath).getValue())

    @Input
    def wingLoading(self):
        """
        Aircraft wing loading
        :Unit: [kg / m^2]
        :rtype: float
        """
        return float(Importer(Component='Performance',
                              VariableName='wingLoading',
                              Default=5000.,
                              Path=self.filePath).getValue())

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
        tailType = askyesnocancel(title="Tail type selection", message="Yes = T tail, No = cruciform, Cancel = conventional")

        if tailType:
            return 'T tail'
        elif tailType is None:
            return 'conventional'
        else:
            return 'cruciform'

    #### Attributes ###

    @Attribute
    def filePath(self):
        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """
        defaultPath = os.path.dirname(Files.__file__)
        defaultFile = os.path.dirname(Files.__file__) + '\input.xlsx'
        file_opt = options = {}
        options['initialdir'] = defaultPath
        options['initialfile'] = defaultFile
        # get filename
        filename = tkFileDialog.askopenfilename(**file_opt)
        return str(filename)

    @Part
    def wingbase(self):
        return Wing(maCruise=self.maCruise,
                    fuselageLength=self.fuselage.fuselageLength,
                    fuselageDiameter=self.fuselage.fuselageDiameter,
                    enginePos=self.enginebase.enginePos,
                    wingLoading=self.wingLoading,
                    mTOW=self.mTOW,
                    hCruise=self.hCruise,
                    filePath=self.filePath,
                    cg=self.evaluations.cg,
                    ac=self.evaluations.ac)

    @Part
    def fuselage(self):
        return Fuselage(maCruise=self.maCruise,
                        filePath=self.filePath)

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
                      tcRatio=self.wingbase.tcRatio,
                      filePath=self.filePath)

    @Part
    def vtpbase(self):
        return Vtp(tailType=self.tailType,
                   surfaceWing=self.wingbase.surface,
                   cMACWing=self.wingbase.cMAC,
                   spanWing=self.wingbase.span,
                   fuselageLength=self.fuselage.fuselageLength,
                   posFraction=self.wingbase.posFraction,
                   conePos=self.fuselage.tailSectionCurves[1].center.y,
                   tlH=self.htpbase.tl,
                   filePath=self.filePath,
                   crH=self.htpbase.chordRoot,
                   longPosH=self.htpbase.longPos,
                   vertPosH=self.htpbase.vertPos)

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
                   tlV=self.vtpbase.tl,
                   spanV=self.vtpbase.span,
                   cMACyPosV=self.vtpbase.cMACyPos,
                   sweep25V=self.vtpbase.sweep25,
                   sweepLEV=self.vtpbase.sweepLE,
                   cMACV=self.vtpbase.cMAC,
                   filePath=self.filePath,
                   chordRootV=self.vtpbase.chordRoot,
                   chordTipV=self.vtpbase.chordTip,
                   longPosV=self.vtpbase.longPos,
                   vertPosV=self.vtpbase.vertPos,
                   rcr=self.vtpbase.rcr)

    @Part
    def landingGear(self):
        return LandingGear(filePath=self.filePath,
                           wingPosition=self.wingbase.wingPosition,
                           fuselageDiameter=self.fuselage.fuselageDiameter,
                           fuselageLength=self.fuselage.fuselageLength,
                           posFraction=self.wingbase.posFraction,
                           cMAC=self.wingbase.cMAC,
                           cg=self.evaluations.cg,
                           fuselage=self.fuselage.loft,
                           wing=self.wingbase.rightWing,
                           engines=self.enginebase.engineSolid)

    @Part
    def evaluations(self):
        return Evaluations(maCruise=self.maCruise,
                           tailType=self.tailType,
                           vertPosW=self.wingbase.vertPos,
                           aspectRatioW=self.wingbase.aspectRatio,
                           sweep50W=self.wingbase.sweep50,
                           sweep25W=self.wingbase.sweep25,
                           spanW=self.wingbase.span,
                           surfaceW=self.wingbase.surface,
                           taperRatioW=self.wingbase.taperRatio,
                           cMACW=self.wingbase.cMAC,
                           chordRootW=self.wingbase.chordRoot,
                           longPosW=self.wingbase.longPos,
                           posFraction=self.wingbase.posFraction,
                           vertPosT=self.htpbase.vertPos,
                           sweep50T=self.htpbase.sweep50,
                           aspectRatioT=self.htpbase.aspectRatio,
                           surfaceT=self.htpbase.surface,
                           tlH=self.htpbase.tl,
                           fuselageDiameter=self.fuselage.fuselageDiameter,
                           fuselageLength=self.fuselage.fuselageLength,
                           longPosE=self.enginebase.longPos,
                           nacelleDiameter=self.enginebase.nacelleDiameter,
                           nacelleLength=self.enginebase.nacelleLength,
                           fuselage=self.fuselage.loft,
                           wing=self.wingbase.rightWing)


if __name__ == '__main__':
    from parapy.gui import display

    obj = Aircraft()
    display(obj)