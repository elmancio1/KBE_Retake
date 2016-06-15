from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Handler.importer import Importer


class Fuselage(GeomBase):
    """
    Basic class Fuselage
    """

    @Input
    def fuselageLength(self):
        """
        Aircraft fuselage length
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Fuselage',
                              VariableName='fuselageLength',
                              Default=30.0).getValue())

    @Input
    def fuselageDiameter(self):
        """
        Aircraft Diameter
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Fuselage',
                              VariableName='fuselageDiameter',
                              Default=4.0).getValue())


    @Input
    def noseSlenderness(self):
        """
        Aircraft nose slenderness, equal to nose length over fuselage diameter
        :Unit: [ ]
        :rtype: float
        """
        if self.maCruise < 0.0 or self.maCruise > 0.9:
            showwarning("Warning", "Please insert a value between 0 and 0.9")
            print("Please insert a value between 0 and 0.9")
            return 0.81
        elif self.maCruise < 0.74:
            return 0.0065 * exp(6.6077 * 0.77)
        else:
            return 0.0065 * exp(6.6077 * self.maDD)

    @Input
    def tailSlenderness(self):
        """
        Aircraft tail slenderness, equal to tail length over fuselage diameter
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Fuselage',
                              VariableName='tailSlenderness',
                              Default=3.0).getValue())

    @Input
    def tailUpAngle(self):
        """
        Aircraft tail angle, positive upward
        :Unit: [deg]
        :rtype: float
        """
        return float(Importer(Component='Fuselage',
                              VariableName='tailUpAngle',
                              Default=5.0).getValue())

    @Input
    def noseSections(self):
        """
        Aircraft nose sections magnitude percentage
        :Unit: [ ]
        :rtype: collections.Sequence[float]
        """
        return [
                    [0.00000, -0.15172, 0.00000, 0.00000],
                    [0.00952, -0.15602, 0.06590, 0.08051],
                    [0.02377, -0.15403, 0.10426, 0.12253],
                    [0.03797, -0.15300, 0.13204, 0.14861],
                    [0.05584, -0.15057, 0.16088, 0.17544],
                    [0.06413, -0.14920, 0.17226, 0.18709],
                    [0.07602, -0.14832, 0.18601, 0.20177],
                    [0.09620, -0.14576, 0.20647, 0.22354],
                    [0.11875, -0.14370, 0.22534, 0.24354],
                    [0.14493, -0.14178, 0.24501, 0.26759],
                    [0.17515, -0.13784, 0.26256, 0.29266],
                    [0.19717, -0.12721, 0.28273, 0.30734],
                    [0.22211, -0.11632, 0.30342, 0.32405],
                    [0.25057, -0.09762, 0.33079, 0.34076],
                    [0.27551, -0.08317, 0.35346, 0.35443],
                    [0.30405, -0.06844, 0.37688, 0.36810],
                    [0.33849, -0.05464, 0.39829, 0.38380],
                    [0.38485, -0.04084, 0.42163, 0.40253],
                    [0.44422, -0.02914, 0.44415, 0.42354],
                    [0.51189, -0.01977, 0.46308, 0.44557],
                    [0.57956, -0.01217, 0.47606, 0.46127],
                    [0.65560, -0.00690, 0.48341, 0.47595],
                    [0.75419, -0.00217, 0.49245, 0.48937],
                    [0.83489, -0.00038, 0.49645, 0.49696],
                    [0.88838, 0.000530, 0.49847, 0.50000],
                    [0.94660, 0.000540, 0.49944, 0.50000],
                    [1.00000, 0.000000, 0.50000, 0.50000]
                ]

    @Input
    def tailSections(self):
        """
        Aircraft tail sections magnitude percentage
        :Unit: [ ]
        :rtype: collections.Sequence[float]
        """
        return [100, 10]

    @Input
    def cylinderSections(self):
        """
        Aircraft cylinder sections magnitude percentage
        :Unit: [ ]
        :rtype: collections.Sequence[float]
        """
        return [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ###################################################################

    if __name__ == '__main__':
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def maCruise(self):
        return float(Importer(Component='Performance',
                              VariableName='M cruise',
                              Default=0.7).getValue())

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
    def noseLength(self):
        """
        Aircraft nose length
        :Unit: [m]
        :rtype: float
        """
        return self.noseSlenderness * self.fuselageDiameter

    @Attribute
    def tailLength(self):
        """
        Aircraft tail length
        :Unit: [m]
        :rtype: float
        """
        return self.tailSlenderness * self.fuselageDiameter

    @Attribute
    def cylinderLength(self):
        """
        Aircraft fuselage cylindrical section length
        :Unit: [m]
        :rtype: float
        """
        return self.fuselageLength - (self.noseLength + self.tailLength)

    @Attribute
    def noseSectionRadius(self):
        """
        Section radius multiplied by the radius distribution
        through the length. Note that the numbers are percentages.
        :Unit: [ ]
        :rtype: collections.Sequence[float]
        """
        if self.noseSections[-1] / 100:
            self.noseSections[-1] = 100

        return [i * self.fuselageDiameter / 2 / 100 for i in self.noseSections]

    @Attribute
    def noseSectionLength(self):
        """
        Section length is determined by dividing the fuselage
        length by the number of fuselage sections.
        :Unit: [ ]
        :rtype: float
        """
        return self.noseLength / (len(self.noseSectionRadius) - 1)

    @Attribute
    def cylinderSectionRadius(self):
        """
        Section radius multiplied by the radius distribution
        through the length. Note that the numbers are percentages.
        :Unit: [ ]
        :rtype: collections.Sequence[float]
        """
        return [i * self.fuselageDiameter / 2 / 100 for i in self.cylinderSections]

    @Attribute
    def cylinderSectionLength(self):
        """
        Section length is determined by dividing the fuselage
        length by the number of fuselage sections.
        :Unit: [ ]
        :rtype: float
        """
        if self.tailSlenderness < 1.0:
            showwarning('Warning', 'Tail slenderness ratios < 1 are detrimental for profile drag.')
        return self.cylinderLength / (len(self.cylinderSections) + 1)

    @Attribute
    def tailSectionRadius(self):
        """
        Section radius multiplied by the radius distribution
        through the length. Note that the numbers are percentages.
        :Unit: [ ]
        :rtype: collections.Sequence[float]
        """
        if self.tailSections[0] / 100:
            self.tailSections[0] = 100
        return [i * self.fuselageDiameter / 2 / 100 for i in self.tailSections]

    @Attribute
    def tailSectionLength(self):
        """
        Section length is determined by dividing the fuselage
        length by the number of fuselage sections.
        :Unit: [ ]
        :rtype: float
        """
        return self.tailLength / (len(self.tailSectionRadius) - 1)

    @Attribute
    def fuselageSectionCurves(self):
        """
        Sequence of curves composing the fuselage
        :Unit: [ ]
        :rtype:
        """
        return self.noseSectionCurves + self.cylinderSectionCurves + self.tailSectionCurves

    @Attribute
    def tailDivergenceAngle(self):
        """
        Aircraft tail divergence angle, evaluated from 4 characteristic points of the tail sections
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(((self.tailSectionCurves[1].center.y - self.tailSectionCurves[1].radius) -
                             (self.tailSectionCurves[0].center.y - self.tailSectionCurves[0].radius)) /
                            (self.tailSectionCurves[1].center.z - self.tailSectionCurves[0].center.z)) -
                       atan(((self.tailSectionCurves[1].center.y + self.tailSectionCurves[1].radius) -
                             (self.tailSectionCurves[0].center.y + self.tailSectionCurves[0].radius)) /
                            (self.tailSectionCurves[1].center.z - self.tailSectionCurves[0].center.z)))

    @Attribute
    def newTailSlenderness(self):
        if self.tailDivergenceAngle > 24:
            if askyesno("Warning",
                        "The tail-cone divergence angle is greater than 24 deg. This is detrimental for form drag. "
                        "Would you like to search for the minimum feasible slenderness ratio? "):

                slendernessIncrement = 0.01
                while self.tailDivergenceAngle > 24:
                    self.tailSlenderness += slendernessIncrement

                return "The new value for tail slenderness is " + repr(self.tailSlenderness)
            else:
                return "Divergence angle is too high."
        else:
            return "No change needed"

# #### part ############################################################################################

    @Part
    def noseSectionCurves(self):
        """
        Sequence of curves composing the nose section of fuselage
        :Unit: [ ]
        :rtype:
        """
        return Ellipse(quantify=len(self.noseSections),
                       major_radius=self.noseSections[child.index][2] * self.fuselageDiameter,
                       minor_radius=self.noseSections[child.index][2] * self.fuselageDiameter,
                      position=self.position.translate('z', self.noseLength * self.noseSections[child.index][0],
                                                       'y', self.fuselageDiameter * self.noseSections[child.index][1]),
                      hidden=True)
    @Part
    def cylinderSectionCurves(self):
        """
        Sequence of curves composing the cylindrical section of fuselage
        :Unit: [ ]
        :rtype:
        """
        return Circle(quantify=len(self.cylinderSections),
                      radius=self.cylinderSectionRadius[child.index],
                      position=self.position.translate('z',
                                                       (child.index + 1) * self.cylinderSectionLength + self.noseLength),
                      hidden=True)

    @Part
    def tailSectionCurves(self):
        """
        Sequence of curves composing the tail section of fuselage
        :Unit: [ ]
        :rtype:
        """
        return Circle(quantify=len(self.tailSections),
                      radius=self.tailSectionRadius[child.index],
                      position=self.position.translate('y', child.index * self.tailSectionLength *
                                                       tan(radians(self.tailUpAngle)),
                                                       'z',
                                                       child.index * self.tailSectionLength + self.noseLength +
                                                       self.cylinderLength),
                      hidden=True)

    @Part
    def loft(self):
        """
        3D solid representation of the fuselage
        :Unit: [ ]
        :rtype:
        """
        return LoftedSolid(profiles=self.fuselageSectionCurves, color="yellow", tolerance=1e-2)


if __name__ == '__main__':
    from parapy.gui import display

    obj = Fuselage()
    display(obj)