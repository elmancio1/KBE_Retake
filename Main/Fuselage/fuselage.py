from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *


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
        return 35.

    @Input
    def fuselageDiameter(self):
        """
        Aircraft Diameter
        :Unit: [m]
        :rtype: float
        """
        return 4.

    @Input
    def noseSlenderness(self):
        """
        Aircraft nose slenderness, equal to nose length over fuselage diameter
        :Unit: [ ]
        :rtype: float
        """
        if self.maCruise < 0.65 or self.maCruise > 0.90:
            showwarning("Warning", "Please insert a value between 0.65 and 0.9")
            print("Please insert a value between 0.65 and 0.9")
            return 0.81
        else:
            return 0.0065 * exp(6.6077 * self.maDD)

    @Input
    def tailSlenderness(self):
        """
        Aircraft tail slenderness, equal to tail length over fuselage diameter
        :Unit: [ ]
        :rtype: float
        """
        return 3.

    @Input
    def tailUpAngle(self):
        """
        Aircraft tail angle, positive upward
        :Unit: [deg]
        :rtype: float
        """
        return 5.

    @Input
    def noseSections(self):
        """
        Aircraft nose sections magnitude percentage
        :Unit: [ ]
        :rtype: collections.Sequence[float]
        """
        return [10, 90, 100]

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
        return 0.77

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

    @Part
    def noseSectionCurves(self):
        """
        Sequence of curves composing the nose section of fuselage
        :Unit: [ ]
        :rtype:
        """
        return Circle(quantify=len(self.noseSections),
                      radius=self.noseSectionRadius[child.index],
                      position=self.position.translate('z',
                                                       child.index *
                                                       self.noseSectionLength))

    @Part
    def noseCap(self):
        """
        Extreme point of fuselage nose, represented by a sphere
        :Unit: [ ]
        :rtype:
        """
        return Sphere(radius=self.noseSectionRadius[0],
                      position=self.position.translate('z',
                                                       0))

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
        return self.cylinderLength / (len(self.cylinderSections) - 1)

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
                                                       child.index * self.cylinderSectionLength + self.noseLength))

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
                                                       self.cylinderLength))

    @Attribute
    def fuselageSectionCurves(self):
        """
        Sequence of curves composing the fuselage
        :Unit: [ ]
        :rtype:
        """
        return self.noseSectionCurves + self.cylinderSectionCurves + self.tailSectionCurves

    @Part
    def loft(self):
        """
        3D solid representation of the fuselage
        :Unit: [ ]
        :rtype:
        """
        return LoftedSolid(profiles=self.fuselageSectionCurves, color="yellow")

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
                        "The tailcone divergence angle is greater than 24 deg. This is detrimental for form drag. "
                        "Would you like to search for the minimum feasible slenderness ratio ? "):

                slendernessIncrement = 0.01
                while self.tailDivergenceAngle > 24:
                    self.tailSlenderness += slendernessIncrement

                return "The new value for tail slenderness is " + repr(self.tailSlenderness)
            else:
                return "Divergence angle is too high."
        else:
            return "No change needed"

if __name__ == '__main__':
    from parapy.gui import display

    obj = Fuselage()
    display(obj)