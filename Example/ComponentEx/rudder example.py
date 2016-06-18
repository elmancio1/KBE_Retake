from parapy.core import *
from parapy.geom import *

class RudderEx(Base):

    @Attribute
    def pts1(self):
        return [Point(1, 1),
                Point(1, -1),
                Point(-1, -1),
                Point(-1, 1),
                Point(1, 1)]

    @Part
    def quad1(self):
        return PolygonalFace(self.pts1)

    @Attribute
    def pts2(self):
        return [Point(2, 2),
                Point(2, -2),
                Point(-2, -2),
                Point(-2, 2),
                Point(2, 2)]

    @Part
    def quad2(self):
        return PolygonalFace(self.pts2)

    @Attribute
    def pts3(self):
        return [Point(),
                Point(0, 1),
                Point(1, 1),
                Point(1, 0),
                Point()]

    @Part
    def quad3(self):
        return PolygonalFace(self.pts3)

    @Part
    def int(self):
        return Subtracted(shape_in=self.quad1, tool=self.quad3)

    @Attribute
    def prova(self):
        if self.int.faces == []:
            return 13
        else:
            return self.int.faces[0].area

    @Attribute
    def pointsRudder1(self):
        """
        List of points representing the vertical tail rudder
        :Unit: []
        :rtype: Points
        """
        return [Point(0, self.vertPos, self.longPos + (1-self.rcr)*self.chordRoot),
                Point(0, self.vertPos + self.span, self.longPos + self.span * tan(radians(self.sweepLE)) + (1-self.rcr)*self.chordTip),
                Point(0, self.vertPos + self.span, self.longPos + self.span * tan(radians(self.sweepLE)) + self.chordTip),
                Point(0, self.vertPos, self.longPos + self.chordRoot),
                Point(0, self.vertPos, self.longPos + (1-self.rcr)*self.chordRoot)]

    @Part
    def cube1(self):
        return Cube(2)

    @Part
    def cube2(self):
        return Cube(1)

    @Part
    def sottrazione(self):
        return Subtracted(shape_in=self.cube1, tool=self.cube2)


if __name__ == '__main__':
    from parapy.gui import display
    obj = RudderEx()
    display(obj)