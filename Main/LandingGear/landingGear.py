from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Handler.importer import Importer
import Tkinter, Tkconstants, tkFileDialog

class LandingGear(GeomBase):
    """
    Basic class Landing Gear
    """

    @Input
    def visualChecks(self):
        """
        Visualize checks for positioning.
        :type: boolean
        :return:
        """
        return False

    @Input
    def height(self):
        """
        Height of the main landing gear wrt to the belly of the aircraft
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='height',
                              Default=1.5,
                              Path=self.filePath).getValue())

    @Input
    def longPos(self):
        """
        Gear position with regard to the MAC
        :Unit: []
        :rtype: float
        """

        return float(Importer(Component='Landing Gear',
                              VariableName='gearLongPos',
                              Default=0.4,
                              Path=self.filePath).getValue())


    @Input
    def latPos(self):
        """
        Lateral gear position with regard to the fuselage diameter
        :Unit: []
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='gearLatPos',
                              Default=1.3,
                              Path=self.filePath).getValue())

    @Input
    def wheelRadius(self):
        """
        Diameter of the main wheel.
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='main wheel diameter',
                              Default=0.5,
                              Path=self.filePath).getValue())

    @Input
    def tipbackPrecision(self):
        """
        Precision of tipback angle.
        :return:
        """
        return 0.1

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ################################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from engine
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
    def wingPosition(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 'low wing'

    @Input(settable=settable)
    def fuselageDiameter(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 5.0

    @Input(settable=settable)
    def fuselageLength(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 30.

    @Input(settable=settable)
    def posFraction(self):
        """
        Wing position fraction of the fuselage, due to engine position
        :Unit: [m]
        :rtype: float
        """
        return 0.5

    @Input(settable=settable)
    def cMAC(self):
        """
        MAC length
        :Unit: [m]
        :rtype: string
        """
        return 3.0

    @Input(settable=settable)
    def cg(self):
        """
        Center of gravity longitudinal position
        :Unit: [m]
        :rtype: float
        """
        return 14.97

    @Input(settable=settable)
    def fuselage(self):
        """
        Fuselage 3D representation
        :Unit: [ ]
        :rtype: lofted solid
        """
        return

    @Input(settable=settable)
    def wing(self):
        """
        Wing 3D representation
        :Unit: [ ]
        :rtype: lofted solid
        """
        return


    # ### Attributes ##################################################################################################

    @Attribute
    def hubLongPos(self):
        """
        Longitudinal position of the wheel hub
        :Unit: [m]
        :return:
        """
        longPos = self.fuselageLength * self.posFraction + self.longPos * self.cMAC

        if longPos < self.cg:
            print("Warning: the longitudinal position of the gear is less than the cg longitudinal location.")
            showwarning('Warning', 'The main gear is in front of the center of gravity. Please increase the value '
                                   'of the longitudinal gear position.')
            longPos = self.cg + 0.5 * self.cMAC #the position is changed to something possible.

        return longPos

    @Attribute
    def hubHeightPos(self):
        """
        Length of the main landing gear length.
        :Unit: [m]
        :type: float
        :return:
        """
        return self.height + self.fuselageDiameter / 2

    @Attribute
    def hubLatPos(self):
        """
        Lateral position of the wheel hub.
        :Unit: [m]
        :type: float
        :return:
        """
        lat = self.latPos
        if self.latPos < 1.0:
            print("Warning: The lateral distance between the wheels is less than the fuselage diameter.")
            showwarning('Warning', 'The lateral distance between the wheels is less than the fuselage diameter.'
                                   ' Please increase the value of the lateral gear position.')
            lat = 1.1 #ToDo: Harcoded o troviamo qualcosa id meglio?

        return lat * self.fuselageDiameter / 2

    @Attribute
    def maxTipbackAngle(self):
        """
        Angle between cg and wheel hub.
        :return:
        """
        o = self.hubLongPos - self.cg
        a = self.hubHeightPos
        angle = degrees(atan(o / a))

        if angle < 14.0:
            print("Warning: the angle between CG and wheel hub is smaller than 14 deg.")
            showwarning('Warning', 'The angle between CG and wheel hub is smaller than 14 deg.'
                                   'Please increase longitudinal position or decrease the leg length')

        return angle

    @Attribute
    def tipbackAngle(self):
        """


        :return:
        """
        tipback = 0
        x = self.hubLatPos
        y = -1 * self.hubHeightPos
        z = self.hubLongPos
        R = self.wheelRadius
        int = []
        while int == []:
            rotationPoint = Point(x, y - R * cos(radians(tipback)), z + R * sin(radians(tipback)))

            piano = Plane(reference=rotationPoint, normal=Vector(0, cos(radians(tipback)), -sin(radians(tipback))))
            int_shape = IntersectedShapes(shape_in=self.fuselage, tool=piano)
            int = int_shape.edges
            tipback += self.tipbackPrecision #ToDo: la precisione del tpack e settabile. va bene?
        return tipback

    @Attribute
    def lateralAngle(self):
        """


        :return:
        """
        lateral = 0
        x = self.hubLatPos
        y = -1 * self.hubHeightPos
        z = self.hubLongPos
        R = self.wheelRadius
        int = []
        while int == []:
            rotationPoint = Point(x, y - R, z)

            piano = Plane(reference=rotationPoint, normal=Vector(-sin(radians(lateral)), cos(radians(lateral)), 0))
            int_shape = IntersectedShapes(shape_in=self.wing, tool=piano)
            int = int_shape.edges
            lateral += self.tipbackPrecision #ToDo: la precisione del tpack e settabile. va bene?
        return lateral


################

    @Part
    def rotationPoint(self):
        return Sphere(radius=0.04,
                      position=Point(self.hubLatPos, -1 * self.hubHeightPos - self.wheelRadius * cos(radians(self.tipbackAngle)),
                     self.hubLongPos + self.wheelRadius * sin(radians(self.tipbackAngle))),
                      color='red',
                      hidden=not self.visualChecks)

    @Part
    def tipbackPlane(self):
        return Plane(reference=Point(self.hubLatPos, -1 * self.hubHeightPos - self.wheelRadius * cos(radians(self.tipbackAngle)),
                     self.hubLongPos + self.wheelRadius * sin(radians(self.tipbackAngle))),
                     normal=Vector(0, cos(radians(self.tipbackAngle)), -sin(radians(self.tipbackAngle))),
                     hidden=not self.visualChecks)

    @Part
    def tailStrikeArea(self):
        return IntersectedShapes(shape_in=self.fuselage,
                                 tool=self.tipbackPlane,
                                 color='red',
                                 hidden=not self.visualChecks)

    @Part
    def lateralPoint(self):
        return Sphere(radius=0.04,
                      position=Point(self.hubLatPos, -1 * self.hubHeightPos - self.wheelRadius,
                     self.hubLongPos),
                      color='blue',
                      hidden=not self.visualChecks)

    @Part
    def lateralPlane(self):
        return Plane(reference=Point(self.hubLatPos, -1 * self.hubHeightPos - self.wheelRadius,
                     self.hubLongPos),
                     normal=Vector(-sin(radians(self.lateralAngle)), cos(radians(self.lateralAngle)), 0),
                     hidden=not self.visualChecks)

    @Part
    def lateralStrikeArea(self):
        return IntersectedShapes(shape_in=self.wing,
                                 tool=self.lateralPlane,
                                 color='red',
                                 hidden=not self.visualChecks) #ToDO: al momento si interseca con la win, ma deve farlo anche con i motori

    @Attribute
    def tipbackControl(self):
        if self.tipbackAngle < self.maxTipbackAngle:
            showwarning("Warning", "Tip back angle is smaller than the angle between the CG anf wheel hub."
                                   " Please increase the gear height or increase the longitudinal position.")
            return "Please increase height"
        else:
            return "No changes needed"

    #######################

    @Part
    def wheelCircle(self):
        """
        Wheel part.
        :return:
        """

        return Circle(radius=self.wheelRadius,
                      position=rotate(translate(self.position,
                                                'x', self.hubLatPos,
                                                'y', -1 * self.hubHeightPos,
                                                'z', self.hubLongPos),
                                      Vector(0, 1, 0), radians(90)),
                      hidden=False)



if __name__ == '__main__':
    from parapy.gui import display

    obj = LandingGear()
    display(obj)