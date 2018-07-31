__author__ = 'somnath'

import os, sys


class Point:

    def __init__(self, coordinate=[]):
        self.coordinates = coordinate
        self.type = str(len(coordinate)) + "D"

    def getCoordinates(self):
        return self.coordinates

    def getType(self):
        return self.type

    def display(self):
        coordinates = [ str(c) for c in self.coordinates ]
        #print("({})".format(",".join(coordinates)))
        return ",".join(coordinates)





