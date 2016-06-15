from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Handler.importer import Importer
class AircaftCoG(GeomBase):

    """
    Basic class for the airplane center of gravity
    """

    @Input
    def wingCoef(self):
        """
        Coefficent for estimating wing mass
        :return:
        """

